from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import ProductCrossReference, ClassificationCrossReference, EntityCrossReference
    from .deletion import DeleteProductCrossReference

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
    
    # ===== Product Reference Methods =====
    
    def add_product_reference(self, product_id: Optional[str] = None, 
                            type_: Optional[str] = None,
                            qualifier_id: Optional[str] = None,
                            mount_location: Optional[str] = None,
                            ref_object: Optional['ProductCrossReference'] = None) -> None:
        """Add product cross-reference to this asset.
        
        Can be called two ways:
        1. With parameters: add_product_reference(product_id="P001", type_="Related")
        2. With object: add_product_reference(ref_object=product_ref_obj)
        """
        from .relations import ProductCrossReference
        
        if ref_object is not None:
            # Use provided object
            ref = ref_object
        else:
            # Create from parameters
            ref = ProductCrossReference({
                "ProductID": product_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["ProductCrossReference"], list):
            self._data["ProductCrossReference"] = []
        self._data["ProductCrossReference"].append(ref)
    
    def delete_product_reference(self, product_id: Optional[str] = None, 
                               type_: Optional[str] = None,
                               qualifier_id: Optional[str] = None,
                               mount_location: Optional[str] = None,
                               delete_ref_object: Optional['DeleteProductCrossReference'] = None) -> None:
        """Delete/sever product reference from this asset.
        
        Can be called two ways:
        1. With parameters: delete_product_reference(product_id="P001")
        2. With object: delete_product_reference(delete_ref_object=delete_ref_obj)
        """
        from .deletion import DeleteProductCrossReference
        
        if delete_ref_object is not None:
            # Use provided object
            delete_ref = delete_ref_object
        else:
            # Create from parameters
            delete_ref = DeleteProductCrossReference({
                "ProductID": product_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["DeleteProductCrossReference"], list):
            self._data["DeleteProductCrossReference"] = []
        self._data["DeleteProductCrossReference"].append(delete_ref)
    
    # ===== Classification Reference Methods =====
    
    def add_classification_reference(self, classification_id: Optional[str] = None, 
                                   type_: Optional[str] = None,
                                   qualifier_id: Optional[str] = None,
                                   mount_location: Optional[str] = None,
                                   ref_object: Optional['ClassificationCrossReference'] = None) -> None:
        """Add classification cross-reference to this asset.
        
        Can be called two ways:
        1. With parameters: add_classification_reference(classification_id="C001")
        2. With object: add_classification_reference(ref_object=class_ref_obj)
        """
        from .relations import ClassificationCrossReference
        
        if ref_object is not None:
            # Use provided object
            ref = ref_object
        else:
            # Create from parameters
            ref = ClassificationCrossReference({
                "ClassificationID": classification_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["ClassificationCrossReference"], list):
            self._data["ClassificationCrossReference"] = []
        self._data["ClassificationCrossReference"].append(ref)
    
    # ===== Entity Reference Methods =====
    
    def add_entity_reference(self, entity_id: Optional[str] = None, 
                           type_: Optional[str] = None,
                           qualifier_id: Optional[str] = None,
                           mount_location: Optional[str] = None,
                           ref_object: Optional['EntityCrossReference'] = None) -> None:
        """Add entity cross-reference to this asset.
        
        Can be called two ways:
        1. With parameters: add_entity_reference(entity_id="E001", type_="Component")
        2. With object: add_entity_reference(ref_object=entity_ref_obj)
        """
        from .relations import EntityCrossReference
        
        if ref_object is not None:
            # Use provided object
            ref = ref_object
        else:
            # Create from parameters
            ref = EntityCrossReference({
                "EntityID": entity_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["EntityCrossReference"], list):
            self._data["EntityCrossReference"] = []
        self._data["EntityCrossReference"].append(ref)
