"""Namespace-tolerant decoding of Publishing XML, not STEP-XML documents."""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Type, TypeVar

from pydantic import ValidationError

from .exceptions import PublishingError
from .models import (
    ActualPage, PlannedPage, Publication, PublicationGroup,
    PublicationSection, PublishingNode, Revision,
)

N = TypeVar("N", bound=PublishingNode)


def local_tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def root(data: bytes, expected: str) -> ET.Element:
    # Publishing responses do not need DTDs or entity expansion, even in UTF-16.
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)\b", data.replace(b"\x00", b""), re.I):
        raise PublishingError("DTD and entity declarations are not supported")
    try:
        element = ET.fromstring(data)
    except (ET.ParseError, LookupError, ValueError) as error:
        raise PublishingError("Invalid Publishing XML") from error
    if local_tag(element) != expected:
        raise PublishingError(f"Expected Publishing XML root {expected}")
    return element


def children(element: ET.Element, tag: str) -> List[ET.Element]:
    return [child for child in element if local_tag(child) == tag]


def nested(element: ET.Element, container: str, tag: str) -> List[ET.Element]:
    return [item for group in children(element, container) for item in children(group, tag)]


def decode(element: ET.Element, model: Type[N]) -> N:
    attrs = element.attrib
    values: Dict[str, object] = {
        "id": attrs.get("ID"),
        "title": attrs.get("title"),
        "name": next((child.text for child in children(element, "Name")), None),
        "user_type_id": attrs.get("UserTypeId", attrs.get("UserTypeID")),
        "context": attrs.get("Context"),
        "workspace": attrs.get("Workspace"),
        "attributes": dict(attrs),
        "raw_xml": ET.tostring(element, encoding="unicode"),
    }
    revisions = children(element, "Revision")
    if revisions:
        r = revisions[0].attrib
        try:
            values["revision"] = Revision.model_validate({
                "created": r.get("Created"), "last_modified": r.get("LastModified"),
                "modified_by": r.get("ModifiedBy"), "number": r.get("RevisionNumber"),
                "is_major": r.get("IsMajor"),
            })
        except ValidationError as error:
            raise PublishingError("Invalid Publishing revision") from error
    if model is Publication:
        values.update(
            parent_id=attrs.get("ParentID"), dtp_system=attrs.get("DTPSystem"),
            pages_per_spread=attrs.get("PagesPerSpread"),
            versions=[decode(e, PublishingNode) for e in
                      nested(element, "Versions", "Version") + children(element, "Version")],
            page_templates=[decode(e, PublishingNode) for e in
                            nested(element, "PageTemplates", "PageTemplate")],
            product_templates=[decode(e, PublishingNode) for e in
                               nested(element, "ProductTemplates", "ProductTemplate")],
            publication_template=next(
                (decode(e, PublishingNode) for e in children(element, "PublicationTemplate")), None),
        )
    elif model is PublicationGroup:
        values["publications"] = [decode(e, Publication) for e in
                                  children(element, "Publication")
                                  + nested(element, "Publications", "Publication")]
    elif model is ActualPage:
        values.update(page_number=attrs.get("PageNumber"), status=attrs.get("Status"),
                      dtp_document_id=attrs.get("DTPDocumentID"))
    elif model is PlannedPage:
        values.update(page_number=attrs.get("PageNumber"), status=attrs.get("Status"),
                      section_id=attrs.get("SectionID"))
    elif model is PublicationSection:
        values.update(
            publication=next(
                (decode(e, Publication) for e in children(element, "Publication")), None),
            master_version=next(
                (decode(e, PublishingNode) for e in children(element, "MasterVersion")), None),
            pages=[decode(e, ActualPage) for e in nested(element, "Pages", "Page")],
            children=[decode(e, PublicationSection) for e in nested(element, "Children", "Section")],
        )
    try:
        return model.model_validate(values)
    except ValidationError as error:
        raise PublishingError(f"Invalid fields in Publishing {local_tag(element)}") from error
