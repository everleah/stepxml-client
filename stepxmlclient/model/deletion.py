"""Deletion models for STEP XML Client.

Defines entity and cross-reference deletion classes for removing items from STEP MDM.
Supports both full entity deletion and link severance operations.
"""

from typing import List, Optional
from . import BaseObject

class DeleteAsset(BaseObject):
    """Top-level deletion specification for assets.
    
    Moves an asset to the recycle bin. The asset and all its associated data is marked for deletion.
    
    Attributes:
        ID: Asset ID to delete
        KeyValue: Optional key value reference
    """
    _GROUP_NAME: str = 'deletedassets'
    _TAG_NAME: str = 'DeleteAsset'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue"]


class DeleteProduct(BaseObject):
    """Top-level deletion specification for products.
    
    Moves a product to the recycle bin. The product and all its associated data is marked for deletion.
    
    Attributes:
        ID: Product ID to delete
        KeyValue: Optional key value reference
    """
    _GROUP_NAME: str = 'deletedproducts'
    _TAG_NAME: str = 'DeleteProduct'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue"]


class DeleteAssetCrossReference(BaseObject):
    """Deletion specification for asset cross-references.
    
    Severs the link between an asset and a product while keeping both items intact.
    The product remains but the asset reference is removed.
    
    Attributes:
        AssetID: Asset ID of the link to sever
        Type: Link type
        QualifierID: Optional qualifier
        Changed: Whether changed
        KeyValue: Optional key value reference
        MetaData: Optional metadata
    """
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
