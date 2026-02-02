from typing import List, Optional
from . import BaseObject

class AssetCrossReference(BaseObject):
    """Link a product to an asset with optional type and qualifier."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'AssetCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["AssetID", "Type", "QualifierID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class ProductCrossReference(BaseObject):
    """Link a product to another product (parent/child, related, etc.)."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ProductCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["ProductID", "Type", "QualifierID", "MountLocation"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class ClassificationCrossReference(BaseObject):
    """Link a product or classification to another classification."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ClassificationCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["ClassificationID", "Type", "QualifierID", "MountLocation"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class EntityCrossReference(BaseObject):
    """Link a product or entity to another entity."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'EntityCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["EntityID", "Type", "QualifierID", "MountLocation"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]
