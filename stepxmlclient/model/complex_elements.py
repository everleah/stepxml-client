"""Complex reusable STEP XML child element models.

These classes are intended for payloads that are too complex or too easy to
mis-shape as plain dictionaries. They can be passed directly to Product/Asset
helper methods as pre-built objects.
"""

from typing import List, Optional
from . import BaseObject


class STEPWorkflowStateBind(BaseObject):
    """Workflow binding for Product.

    Required attributes (STEP.xsd STEPWorkflowStateBindType):
    - WorkflowID
    - StateID
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "STEPWorkflowStateBind"
    _ATTRIBUTE_NAMES: List[str] = ["WorkflowID", "StateID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []


class SequenceProduct(BaseObject):
    """Sequence information for a child product.

    Required/optional fields (SequenceProductType):
    - ID (required)
    - Changed (optional)
    - KeyValue (optional, repeatable)
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "SequenceProduct"
    _ATTRIBUTE_NAMES: List[str] = ["ID", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue"]


class OverrideSubProduct(BaseObject):
    """Product override link.

    Fields (OverrideSubProductType):
    - ProductID (required)
    - AnalyzerResult (optional, deprecated in XSD)
    - Product (optional embedded object list)
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "OverrideSubProduct"
    _ATTRIBUTE_NAMES: List[str] = ["ProductID", "AnalyzerResult"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["Product"]


class PackagingReference(BaseObject):
    """Packaging link with quantity.

    Required fields (PackagingReferenceType):
    - ProductID
    - Quantity
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "PackagingReference"
    _ATTRIBUTE_NAMES: List[str] = ["ProductID", "Quantity"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []


class AssetPushLocation(BaseObject):
    """Push status information for an asset.

    Fields (AssetPushLocationType, mixed content):
    - ConfigurationID (required)
    - Status (optional)
    - QualifierID (optional)
    - value/text (optional element text)
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "AssetPushLocation"
    _ATTRIBUTE_NAMES: List[str] = ["Status", "ConfigurationID", "QualifierID"]
    _TEXT_NAMES: List[str] = []
    _VALUE_NAME: str = "value"
    _CHILDREN_NAMES: List[str] = []


class AssetContentSpecification(BaseObject):
    """Single asset conversion descriptor.

    Fields (AssetContentSpecificationType):
    - ImageConversionConfigurationID (optional)
    - IncludesBinaryContent (optional)
    - RelativeURL (optional)
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "AssetContentSpecification"
    _ATTRIBUTE_NAMES: List[str] = [
        "ImageConversionConfigurationID",
        "IncludesBinaryContent",
        "RelativeURL",
    ]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []


class AssetContent(BaseObject):
    """Container for conversion metadata.

    Fields (AssetContentType):
    - QualifierID (optional)
    - AssetContentSpecification (optional, repeatable)
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "AssetContent"
    _ATTRIBUTE_NAMES: List[str] = ["QualifierID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["AssetContentSpecification"]


class BinaryContent(BaseObject):
    """Binary content payload wrapper.

    ``BinaryContent`` is a ``ConfigurationType`` element and is represented as
    element text in this client.
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "BinaryContent"
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _VALUE_NAME: str = "value"
    _CHILDREN_NAMES: List[str] = []


class AssetBinaryContent(BaseObject):
    """Container for base64/binary source content metadata.

    Fields (AssetBinaryContentType):
    - QualifierID (optional)
    - ImageConversionConfigurationID (optional)
    - MIMEType (optional)
    - Checksum (optional)
    - Filename (optional)
    - BinaryContent (required for full XSD compliance)
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "AssetBinaryContent"
    _ATTRIBUTE_NAMES: List[str] = [
        "QualifierID",
        "ImageConversionConfigurationID",
        "MIMEType",
        "Checksum",
        "Filename",
    ]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["BinaryContent"]


class Task(BaseObject):
    """Single workflow task entry.

    Required TaskType fields:
    - STEPWorkflowID
    - StateID
    - AssigneeID
    - AssignedToGroup
    - EntryTime

    Optional fields:
    - Deadline
    - Priority
    - StatusID
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "Task"
    _ATTRIBUTE_NAMES: List[str] = [
        "STEPWorkflowID",
        "StateID",
        "AssigneeID",
        "AssignedToGroup",
        "EntryTime",
        "Deadline",
        "Priority",
        "StatusID",
    ]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []


class CurrentTasks(BaseObject):
    """Container for one or more Task entries (CurrentTasksType)."""

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "CurrentTasks"
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["Task"]


class Term(BaseObject):
    """Single commercial term entry (TermType, mixed text + attributes).

    Optional attributes:
    - MaximumQuantity
    - EndDate
    - TermsListID
    - MinimumQuantity
    - LeadTime
    - UnitID
    - StartDate
    - LotSize

    Optional text content:
    - value
    """

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "Term"
    _ATTRIBUTE_NAMES: List[str] = [
        "MaximumQuantity",
        "EndDate",
        "TermsListID",
        "MinimumQuantity",
        "LeadTime",
        "UnitID",
        "StartDate",
        "LotSize",
    ]
    _TEXT_NAMES: List[str] = []
    _VALUE_NAME: str = "value"
    _CHILDREN_NAMES: List[str] = []


class Terms(BaseObject):
    """Container for one or more Term entries (TermsType)."""

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "Terms"
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["Term"]


class Tables(BaseObject):
    """Container for TableDefinition or Table entries (TablesType)."""

    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = "Tables"
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["TableDefinition", "Table"]
