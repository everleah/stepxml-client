from typing import List, Optional
from . import BaseObject

class DeleteAsset(BaseObject):
    """Move asset to recycle bin. Top-level deletion structure."""
    _GROUP_NAME: str = 'deletedassets'
    _TAG_NAME: str = 'DeleteAsset'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue"]


class DeleteProduct(BaseObject):
    """Move product to recycle bin. Top-level deletion structure."""
    _GROUP_NAME: str = 'deletedproducts'
    _TAG_NAME: str = 'DeleteProduct'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue"]


class DeleteAssetCrossReference(BaseObject):
    """Delete/sever asset link from a product while keeping product intact."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'DeleteAssetCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["AssetID", "Type", "QualifierID", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class DeleteProductCrossReference(BaseObject):
    """Delete/sever product link from another product while keeping both intact."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'DeleteProductCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["ProductID", "Type", "QualifierID", "MountLocation", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class DeleteClassificationCrossReference(BaseObject):
    """Delete/sever classification link while keeping classification intact."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'DeleteClassificationCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["ClassificationID", "Type", "QualifierID", "MountLocation", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class DeleteEntityCrossReference(BaseObject):
    """Delete/sever entity link while keeping entity intact."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'DeleteEntityCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["EntityID", "Type", "QualifierID", "MountLocation", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]
