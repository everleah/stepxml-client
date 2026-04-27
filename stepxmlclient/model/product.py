from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import AssetCrossReference, ProductCrossReference, ClassificationReference, ClassificationCrossReference, EntityCrossReference
    from .deletion import DeleteAssetCrossReference, DeleteProductCrossReference

class Product(BaseObject):
    """Product entity in STEP MDM.
    
    Represents a product with attributes, relationships to other products/assets/entities,
    and hierarchical parent/child relationships.
    
    Attributes:
        ID: Unique product identifier
        ParentId: Optional parent product ID for hierarchical relationships
        UserTypeID: Optional user type that defines extended properties
        Name: Product name (localized dictionary)
        Values: Dictionary of attribute ID to attribute values
        AssetCrossReference: List of linked assets
        ProductCrossReference: List of linked products
        ClassificationReference: List of linked classifications
        ClassificationCrossReference: List of cross-referenced classifications
        EntityCrossReference: List of linked business entities
        DeleteAssetCrossReference: Assets to unlink
        DeleteProductCrossReference: Products to unlink
    """
    _GROUP_NAME: str = 'products'
    _TAG_NAME: str = 'Product'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentId", "UserTypeID", "QualifierID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "KeyValue",
        "ParentKeyValue",
        "STEPWorkflowStateBind",
        "Values",
        "DeleteSuppressedAssetCrossReference",
        "SuppressedAssetCrossReference",
        "AssetCrossReference",
        "DeleteSuppressedProductCrossReference",
        "SuppressedProductCrossReference",
        "ProductCrossReference",
        "DeleteSuppressedClassificationReference",
        "DeleteClassificationReference",
        "SuppressedClassificationReference",
        "ClassificationReference",
        "DeleteSuppressedClassificationCrossReference",
        "DeleteClassificationCrossReference",
        "SuppressedClassificationCrossReference",
        "ClassificationCrossReference",
        "DeleteSuppressedEntityCrossReference",
        "DeleteEntityCrossReference",
        "SuppressedEntityCrossReference",
        "EntityCrossReference",
        "DeleteAttributeLink",
        "AttributeLink",
        "DataContainerTypeLink",
        "DeleteDataContainerTypeLink",
        "DataContainers",
        "DeleteAssetCrossReference",
        "DeleteProductCrossReference",
        "SequenceProduct",
        "CurrentTasks",
        "Terms",
        "Tables",
        "OverrideSubProduct",
        "PackagingReference"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in [
                        "DeleteSuppressedAssetCrossReference", "SuppressedAssetCrossReference", "AssetCrossReference",
                        "DeleteSuppressedProductCrossReference", "SuppressedProductCrossReference", "ProductCrossReference",
                        "DeleteSuppressedClassificationReference", "DeleteClassificationReference", "SuppressedClassificationReference", "ClassificationReference",
                        "DeleteSuppressedClassificationCrossReference", "DeleteClassificationCrossReference", "SuppressedClassificationCrossReference", "ClassificationCrossReference",
                        "DeleteSuppressedEntityCrossReference", "DeleteEntityCrossReference", "SuppressedEntityCrossReference", "EntityCrossReference",
                        "DeleteAttributeLink", "AttributeLink", "DataContainerTypeLink", "DeleteDataContainerTypeLink",
                        "DeleteAssetCrossReference", "DeleteProductCrossReference",
                        "SequenceProduct", "CurrentTasks", "Terms", "Tables", "OverrideSubProduct", "PackagingReference"]:
            if rel_name not in self._data:
                self._data[rel_name] = []
    
    # ===== Asset Reference Methods =====
    
    def add_asset_reference(self, asset_id: Optional[str] = None, 
                          type_: Optional[str] = None, 
                          qualifier_id: Optional[str] = None,
                          ref_object: Optional['AssetCrossReference'] = None) -> None:
        """Add asset cross-reference to this product.
        
        Can be called two ways:
        1. With parameters: add_asset_reference(asset_id="A001", type_="Image")
        2. With object: add_asset_reference(ref_object=asset_ref_obj)
        """
        from .relations import AssetCrossReference
        
        if ref_object is not None:
            # Use provided object
            ref = ref_object
        else:
            # Create from parameters
            ref = AssetCrossReference({
                "AssetID": asset_id,
                "Type": type_,
                "QualifierID": qualifier_id
            })
        
        if not isinstance(self._data["AssetCrossReference"], list):
            self._data["AssetCrossReference"] = []
        self._data["AssetCrossReference"].append(ref)
    
    def delete_asset_reference(self, asset_id: Optional[str] = None, 
                             type_: Optional[str] = None,
                             qualifier_id: Optional[str] = None,
                             delete_ref_object: Optional['DeleteAssetCrossReference'] = None) -> None:
        """Delete/sever asset reference from this product.
        
        Can be called two ways:
        1. With parameters: delete_asset_reference(asset_id="A001")
        2. With object: delete_asset_reference(delete_ref_object=delete_ref_obj)
        """
        from .deletion import DeleteAssetCrossReference
        
        if delete_ref_object is not None:
            # Use provided object
            delete_ref = delete_ref_object
        else:
            # Create from parameters
            delete_ref = DeleteAssetCrossReference({
                "AssetID": asset_id,
                "Type": type_,
                "QualifierID": qualifier_id
            })
        
        if not isinstance(self._data["DeleteAssetCrossReference"], list):
            self._data["DeleteAssetCrossReference"] = []
        self._data["DeleteAssetCrossReference"].append(delete_ref)
    
    # ===== Product Reference Methods =====
    
    def add_product_reference(self, product_id: Optional[str] = None, 
                            type_: Optional[str] = None,
                            qualifier_id: Optional[str] = None,
                            mount_location: Optional[str] = None,
                            ref_object: Optional['ProductCrossReference'] = None) -> None:
        """Add product cross-reference to this product.
        
        Can be called two ways:
        1. With parameters: add_product_reference(product_id="P002", type_="Related")
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
        """Delete/sever product reference from this product.
        
        Can be called two ways:
        1. With parameters: delete_product_reference(product_id="P002")
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
                                   ref_object: Optional['ClassificationReference'] = None) -> None:
        """Add classification reference to this product.
        
        Can be called two ways:
        1. With parameters: add_classification_reference(classification_id="C001")
        2. With object: add_classification_reference(ref_object=class_ref_obj)
        """
        from .relations import ClassificationReference, ClassificationCrossReference
        
        if ref_object is not None:
            # Use provided object
            ref = ref_object
            if isinstance(ref, ClassificationCrossReference):
                # Normalize legacy cross-reference object to the reference tag.
                ref = ClassificationReference(dict(ref._data))
        else:
            # Create from parameters
            ref = ClassificationReference({
                "ClassificationID": classification_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["ClassificationReference"], list):
            self._data["ClassificationReference"] = []
        self._data["ClassificationReference"].append(ref)

    def add_classification_cross_reference(self, classification_id: Optional[str] = None,
                                         type_: Optional[str] = None,
                                         qualifier_id: Optional[str] = None,
                                         mount_location: Optional[str] = None,
                                         ref_object: Optional['ClassificationCrossReference'] = None) -> None:
        """Add classification cross-reference to this product.

        Use this helper when you explicitly need the
        ``ClassificationCrossReference`` tag.
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
        """Add entity cross-reference to this product.
        
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

class ProductReplacementRule(BaseObject):
    _GROUP_NAME: str = 'product_replacement_rules'
    _TAG_NAME: str = 'Product'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentId", "UserTypeID", "QualifierID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["KeyValue", "ParentKeyValue", "Values"]