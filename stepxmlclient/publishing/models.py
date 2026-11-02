"""Publishing response models, independent of STEP REST v2 payloads."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Revision(BaseModel):
    created: Optional[str] = None
    last_modified: Optional[str] = None
    modified_by: Optional[str] = None
    number: Optional[str] = None
    is_major: Optional[bool] = None


class PublishingNode(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    name: Optional[str] = None
    user_type_id: Optional[str] = None
    context: Optional[str] = None
    workspace: Optional[str] = None
    revision: Optional[Revision] = None
    attributes: Dict[str, str] = Field(default_factory=dict)
    raw_xml: str = ""


class Publication(PublishingNode):
    parent_id: Optional[str] = None
    dtp_system: Optional[str] = None
    pages_per_spread: Optional[str] = None
    versions: List[PublishingNode] = Field(default_factory=list)
    page_templates: List[PublishingNode] = Field(default_factory=list)
    product_templates: List[PublishingNode] = Field(default_factory=list)
    publication_template: Optional[PublishingNode] = None


class PublicationGroup(PublishingNode):
    publications: List[Publication] = Field(default_factory=list)


class ActualPage(PublishingNode):
    page_number: Optional[str] = None
    status: Optional[str] = None
    dtp_document_id: Optional[str] = None


class PlannedPage(PublishingNode):
    page_number: Optional[str] = None
    status: Optional[str] = None
    section_id: Optional[str] = None


class PublicationSection(PublishingNode):
    publication: Optional[Publication] = None
    master_version: Optional[PublishingNode] = None
    pages: List[ActualPage] = Field(default_factory=list)
    children: List["PublicationSection"] = Field(default_factory=list)


class PublishingJob(BaseModel):
    process_id: str
    location: str
    result_field: Optional[str] = None


class JobStatus(BaseModel):
    process_id: str
    status: str
    progress: Optional[int] = None
    number_of_errors: Optional[int] = None
    number_of_warnings: Optional[int] = None


class JobFile(BaseModel):
    id: str
    name: Optional[str] = None
    mime_type: Optional[str] = None
    original_attachment_id: Optional[str] = None


class DocumentDeletion(BaseModel):
    deleted: bool
    status_code: int
