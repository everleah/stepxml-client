from typing import List, Optional, Any, Dict
from . import BaseObject

class Product(BaseObject):
    _GROUP_NAME: str = 'products'
    _TAG_NAME: str = 'Product'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentId", "UserTypeID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "Values",
        "AssetCrossReference",
        "ProductCrossReference",
        "ClassificationCrossReference",
        "EntityCrossReference",
        "DeleteAssetCrossReference",
        "DeleteProductCrossReference"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in ["AssetCrossReference", "ProductCrossReference", 
                        "ClassificationCrossReference", "EntityCrossReference",
                        "DeleteAssetCrossReference", "DeleteProductCrossReference"]:
            if rel_name not in self._data:
                self._data[rel_name] = []
    
    def add_asset_reference(self, asset_id: str, type_: Optional[str] = None, 
                          qualifier_id: Optional[str] = None) -> None:
        """Add asset cross-reference to this product."""
        from .relations import AssetCrossReference
        ref = AssetCrossReference({
            "AssetID": asset_id,
            "Type": type_,
            "QualifierID": qualifier_id
        })
        if not isinstance(self._data["AssetCrossReference"], list):
            self._data["AssetCrossReference"] = []
        self._data["AssetCrossReference"].append(ref)
    
    def add_product_reference(self, product_id: str, type_: Optional[str] = None,
                            qualifier_id: Optional[str] = None,
                            mount_location: Optional[str] = None) -> None:
        """Add product cross-reference to this product."""
        from .relations import ProductCrossReference
        ref = ProductCrossReference({
            "ProductID": product_id,
            "Type": type_,
            "QualifierID": qualifier_id,
            "MountLocation": mount_location
        })
        if not isinstance(self._data["ProductCrossReference"], list):
            self._data["ProductCrossReference"] = []
        self._data["ProductCrossReference"].append(ref)
    
    def delete_asset_reference(self, asset_id: str, type_: Optional[str] = None,
                             qualifier_id: Optional[str] = None) -> None:
        """Delete/sever asset reference from this product."""
        from .deletion import DeleteAssetCrossReference
        delete_ref = DeleteAssetCrossReference({
            "AssetID": asset_id,
            "Type": type_,
            "QualifierID": qualifier_id
        })
        if not isinstance(self._data["DeleteAssetCrossReference"], list):
            self._data["DeleteAssetCrossReference"] = []
        self._data["DeleteAssetCrossReference"].append(delete_ref)
    
    def delete_product_reference(self, product_id: str, type_: Optional[str] = None,
                               qualifier_id: Optional[str] = None,
                               mount_location: Optional[str] = None) -> None:
        """Delete/sever product reference from this product."""
        from .deletion import DeleteProductCrossReference
        delete_ref = DeleteProductCrossReference({
            "ProductID": product_id,
            "Type": type_,
            "QualifierID": qualifier_id,
            "MountLocation": mount_location
        })
        if not isinstance(self._data["DeleteProductCrossReference"], list):
            self._data["DeleteProductCrossReference"] = []
        self._data["DeleteProductCrossReference"].append(delete_ref)

class ProductReplacementRule(BaseObject):
    _GROUP_NAME: str = 'product_replacement_rules'
    _TAG_NAME: str = 'Product'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentId", "UserTypeID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["Values"]