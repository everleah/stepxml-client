from typing import List, Optional, Any, Dict
from . import BaseObject

class Asset(BaseObject):
    _GROUP_NAME: str = 'assets'
    _TAG_NAME: str = 'Asset'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name", "KeyValue"]
    _CHILDREN_NAMES: List[str] = ["Values"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in ["AssetCrossReference", "ProductCrossReference",
                        "ClassificationCrossReference", "EntityCrossReference",
                        "DeleteAssetCrossReference", "DeleteProductCrossReference"]:
            if rel_name not in self._data:
                self._data[rel_name] = []
    
    def add_product_reference(self, product_id: str, type_: Optional[str] = None,
                            qualifier_id: Optional[str] = None,
                            mount_location: Optional[str] = None) -> None:
        """Add product cross-reference to this asset."""
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
    
    def delete_product_reference(self, product_id: str, type_: Optional[str] = None,
                               qualifier_id: Optional[str] = None,
                               mount_location: Optional[str] = None) -> None:
        """Delete/sever product reference from this asset."""
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
