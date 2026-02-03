from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import ProductCrossReference, ClassificationCrossReference, EntityCrossReference, AssetCrossReference
    from .deletion import DeleteProductCrossReference, DeleteClassificationCrossReference, DeleteEntityCrossReference, DeleteAssetCrossReference


class Classification(BaseObject):
    """Classification entity - hierarchical product categorization.
    
    Supports:
    - Nested classifications (parent/child hierarchy)
    - Multiple cross-references (Product, Classification, Entity, Asset)
    - Deletion operations (full deletion and link severance)
    - Multi-language via QualifierID
    - Boolean state tracking (Changed, Republished, Selected, Referenced)
    """
    _GROUP_NAME: str = 'classifications'
    _TAG_NAME: str = 'Classification'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentID", "UserTypeID", "QualifierID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "Values",
        "KeyValue",
        "ParentKeyValue",
        "Classification",  # Nested classifications
        "ProductReference",
        "ProductCrossReference",
        "DeleteProductReference",
        "DeleteProductCrossReference",
        "SuppressedProductReference",
        "SuppressedProductCrossReference",
        "DeleteSuppressedProductReference",
        "DeleteSuppressedProductCrossReference",
        "ClassificationCrossReference",
        "DeleteClassificationCrossReference",
        "SuppressedClassificationCrossReference",
        "DeleteSuppressedClassificationCrossReference",
        "EntityCrossReference",
        "DeleteEntityCrossReference",
        "SuppressedEntityCrossReference",
        "DeleteSuppressedEntityCrossReference",
        "AssetCrossReference",
        "DeleteAssetCrossReference",
        "SuppressedAssetCrossReference",
        "DeleteSuppressedAssetCrossReference",
        "MetaData",
        "AttributeLink",
        "DataContainerTypeLink"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in ["ProductReference", "ProductCrossReference",
                        "DeleteProductReference", "DeleteProductCrossReference",
                        "SuppressedProductReference", "SuppressedProductCrossReference",
                        "DeleteSuppressedProductReference", "DeleteSuppressedProductCrossReference",
                        "ClassificationCrossReference", "DeleteClassificationCrossReference",
                        "SuppressedClassificationCrossReference", "DeleteSuppressedClassificationCrossReference",
                        "EntityCrossReference", "DeleteEntityCrossReference",
                        "SuppressedEntityCrossReference", "DeleteSuppressedEntityCrossReference",
                        "AssetCrossReference", "DeleteAssetCrossReference",
                        "SuppressedAssetCrossReference", "DeleteSuppressedAssetCrossReference"]:
            if rel_name not in self._data:
                self._data[rel_name] = []
        
        # Initialize nested classifications list
        if "Classification" not in self._data:
            self._data["Classification"] = []
    
    # ===== Product Reference Methods =====
    
    def add_product_reference(self, product_id: Optional[str] = None,
                            type_: Optional[str] = None,
                            qualifier_id: Optional[str] = None,
                            mount_location: Optional[str] = None,
                            ref_object: Optional['ProductCrossReference'] = None) -> None:
        """Add product cross-reference to this classification.
        
        Can be called two ways:
        1. With parameters: add_product_reference(product_id="P001")
        2. With object: add_product_reference(ref_object=product_ref_obj)
        """
        from .relations import ProductCrossReference
        
        if ref_object is not None:
            ref = ref_object
        else:
            ref = ProductCrossReference({
                "ProductID": product_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["ProductCrossReference"], list):
            self._data["ProductCrossReference"] = []
        self._data["ProductCrossReference"].append(ref)
    
    # ===== Classification Reference Methods =====
    
    def add_classification_reference(self, classification_id: Optional[str] = None,
                                   type_: Optional[str] = None,
                                   qualifier_id: Optional[str] = None,
                                   mount_location: Optional[str] = None,
                                   ref_object: Optional['ClassificationCrossReference'] = None) -> None:
        """Add classification cross-reference to this classification.
        
        Can be called two ways:
        1. With parameters: add_classification_reference(classification_id="C001")
        2. With object: add_classification_reference(ref_object=class_ref_obj)
        """
        from .relations import ClassificationCrossReference
        
        if ref_object is not None:
            ref = ref_object
        else:
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
        """Add entity cross-reference to this classification.
        
        Can be called two ways:
        1. With parameters: add_entity_reference(entity_id="E001")
        2. With object: add_entity_reference(ref_object=entity_ref_obj)
        """
        from .relations import EntityCrossReference
        
        if ref_object is not None:
            ref = ref_object
        else:
            ref = EntityCrossReference({
                "EntityID": entity_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["EntityCrossReference"], list):
            self._data["EntityCrossReference"] = []
        self._data["EntityCrossReference"].append(ref)
    
    # ===== Asset Reference Methods =====
    
    def add_asset_reference(self, asset_id: Optional[str] = None,
                          type_: Optional[str] = None,
                          qualifier_id: Optional[str] = None,
                          ref_object: Optional['AssetCrossReference'] = None) -> None:
        """Add asset cross-reference to this classification.
        
        Can be called two ways:
        1. With parameters: add_asset_reference(asset_id="A001")
        2. With object: add_asset_reference(ref_object=asset_ref_obj)
        """
        from .relations import AssetCrossReference
        
        if ref_object is not None:
            ref = ref_object
        else:
            ref = AssetCrossReference({
                "AssetID": asset_id,
                "Type": type_,
                "QualifierID": qualifier_id
            })
        
        if not isinstance(self._data["AssetCrossReference"], list):
            self._data["AssetCrossReference"] = []
        self._data["AssetCrossReference"].append(ref)
    
    # ===== Nested Classification Methods =====
    
    def add_nested_classification(self, classification: Optional['Classification'] = None,
                                 **kwargs) -> None:
        """Add nested child classification.
        
        Can be called two ways:
        1. With object: add_nested_classification(classification=child_class)
        2. With parameters: add_nested_classification(ID="C002", Name="Child")
        """
        if classification is not None:
            nested = classification
        else:
            nested = Classification(kwargs)
        
        if not isinstance(self._data["Classification"], list):
            self._data["Classification"] = []
        self._data["Classification"].append(nested)
