"""Entity model for STEP XML Client.

Defines the Entity class for representing generic MDM objects in STEP.
Entities provide a flexible structure for modeling various types of business objects beyond
products, classifications, and assets.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import ProductCrossReference, ClassificationCrossReference, EntityCrossReference, AssetCrossReference
    from .deletion import DeleteProductCrossReference, DeleteClassificationCrossReference, DeleteEntityCrossReference, DeleteAssetCrossReference


class Entity(BaseObject):
    """Entity - generic MDM object with flexible structure.
    
    Represents a generic Master Data entity with flexible structure. Entities can model
    various business object types and support hierarchical organization and cross-references.
    
    Supports:
    - Nested entities (parent/child hierarchy)
    - Multiple cross-references (Product, Classification, Entity, Asset, Context, Workspace)
    - Deletion operations (full deletion and link severance)
    - Multi-language via QualifierID
    - Boolean state tracking (Changed, Republished, Selected, Referenced)
    - Values (attribute data)
    - DataContainers
    
    Attributes:
        ID: Unique entity identifier
        ParentID: Optional parent entity ID for hierarchy
        UserTypeID: Optional user type for extended properties
        QualifierID: Optional qualifier for multi-language/context support
        Name: Entity name (localized)
        Values: Dictionary of attribute ID to attribute values
        Entity: Nested child entities
        ProductCrossReference: Cross-referenced products
        ClassificationCrossReference: Cross-referenced classifications
        EntityCrossReference: Cross-referenced entities
        AssetCrossReference: Cross-referenced assets
    """
    _GROUP_NAME: str = 'entities'
    _TAG_NAME: str = 'Entity'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentID", "UserTypeID", "QualifierID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "KeyValue",
        "ParentKeyValue",
        "Entity",  # Nested entities
        "DeleteSuppressedClassificationCrossReference",
        "DeleteClassificationCrossReference",
        "SuppressedClassificationCrossReference",
        "ClassificationCrossReference",
        "DeleteSuppressedProductCrossReference",
        "DeleteProductCrossReference",
        "SuppressedProductCrossReference",
        "ProductCrossReference",
        "DeleteSuppressedAssetCrossReference",
        "DeleteAssetCrossReference",
        "SuppressedAssetCrossReference",
        "AssetCrossReference",
        "DeleteSuppressedEntityCrossReference",
        "DeleteEntityCrossReference",
        "SuppressedEntityCrossReference",
        "EntityCrossReference",
        "SuppressedContextCrossReference",
        "ContextCrossReference",
        "SuppressedWorkspaceCrossReference",
        "WorkspaceCrossReference",
        "Values",
        "DataContainers",
        "CurrentTasks",
        "Terms"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in ["ProductCrossReference", "DeleteProductCrossReference",
                        "SuppressedProductCrossReference", "DeleteSuppressedProductCrossReference",
                        "ClassificationCrossReference", "DeleteClassificationCrossReference",
                        "SuppressedClassificationCrossReference", "DeleteSuppressedClassificationCrossReference",
                        "EntityCrossReference", "DeleteEntityCrossReference",
                        "SuppressedEntityCrossReference", "DeleteSuppressedEntityCrossReference",
                        "AssetCrossReference", "DeleteAssetCrossReference",
                        "SuppressedAssetCrossReference", "DeleteSuppressedAssetCrossReference",
                        "ContextCrossReference", "SuppressedContextCrossReference",
                        "WorkspaceCrossReference", "SuppressedWorkspaceCrossReference",
                        "Values", "DataContainers", "CurrentTasks", "Terms"]:
            if rel_name not in self._data:
                self._data[rel_name] = []
        
        # Initialize nested entities list
        if "Entity" not in self._data:
            self._data["Entity"] = []
    
    # ===== Product Cross-Reference Methods =====
    
    def add_product_reference(self, product_id: Optional[str] = None,
                            type_: Optional[str] = None,
                            qualifier_id: Optional[str] = None,
                            mount_location: Optional[str] = None,
                            ref_object: Optional['ProductCrossReference'] = None) -> None:
        """Add product cross-reference to this entity.
        
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
    
    def delete_product_reference(self, product_id: Optional[str] = None,
                               type_: Optional[str] = None,
                               qualifier_id: Optional[str] = None,
                               mount_location: Optional[str] = None,
                               delete_ref_object: Optional['DeleteProductCrossReference'] = None) -> None:
        """Delete/sever product reference from this entity.
        
        Can be called two ways:
        1. With parameters: delete_product_reference(product_id="P001")
        2. With object: delete_product_reference(delete_ref_object=delete_ref_obj)
        """
        from .deletion import DeleteProductCrossReference
        
        if delete_ref_object is not None:
            delete_ref = delete_ref_object
        else:
            delete_ref = DeleteProductCrossReference({
                "ProductID": product_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["DeleteProductCrossReference"], list):
            self._data["DeleteProductCrossReference"] = []
        self._data["DeleteProductCrossReference"].append(delete_ref)
    
    # ===== Classification Cross-Reference Methods =====
    
    def add_classification_reference(self, classification_id: Optional[str] = None,
                                   type_: Optional[str] = None,
                                   qualifier_id: Optional[str] = None,
                                   mount_location: Optional[str] = None,
                                   ref_object: Optional['ClassificationCrossReference'] = None) -> None:
        """Add classification cross-reference to this entity.
        
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
    
    def delete_classification_reference(self, classification_id: Optional[str] = None,
                                      type_: Optional[str] = None,
                                      qualifier_id: Optional[str] = None,
                                      mount_location: Optional[str] = None,
                                      delete_ref_object: Optional['DeleteClassificationCrossReference'] = None) -> None:
        """Delete/sever classification reference from this entity.
        
        Can be called two ways:
        1. With parameters: delete_classification_reference(classification_id="C001")
        2. With object: delete_classification_reference(delete_ref_object=delete_ref_obj)
        """
        from .deletion import DeleteClassificationCrossReference
        
        if delete_ref_object is not None:
            delete_ref = delete_ref_object
        else:
            delete_ref = DeleteClassificationCrossReference({
                "ClassificationID": classification_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["DeleteClassificationCrossReference"], list):
            self._data["DeleteClassificationCrossReference"] = []
        self._data["DeleteClassificationCrossReference"].append(delete_ref)
    
    # ===== Entity Cross-Reference Methods =====
    
    def add_entity_reference(self, entity_id: Optional[str] = None,
                           type_: Optional[str] = None,
                           qualifier_id: Optional[str] = None,
                           mount_location: Optional[str] = None,
                           ref_object: Optional['EntityCrossReference'] = None) -> None:
        """Add entity cross-reference to this entity.
        
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
    
    def delete_entity_reference(self, entity_id: Optional[str] = None,
                              type_: Optional[str] = None,
                              qualifier_id: Optional[str] = None,
                              mount_location: Optional[str] = None,
                              delete_ref_object: Optional['DeleteEntityCrossReference'] = None) -> None:
        """Delete/sever entity reference from this entity.
        
        Can be called two ways:
        1. With parameters: delete_entity_reference(entity_id="E001")
        2. With object: delete_entity_reference(delete_ref_object=delete_ref_obj)
        """
        from .deletion import DeleteEntityCrossReference
        
        if delete_ref_object is not None:
            delete_ref = delete_ref_object
        else:
            delete_ref = DeleteEntityCrossReference({
                "EntityID": entity_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location
            })
        
        if not isinstance(self._data["DeleteEntityCrossReference"], list):
            self._data["DeleteEntityCrossReference"] = []
        self._data["DeleteEntityCrossReference"].append(delete_ref)
    
    # ===== Asset Cross-Reference Methods =====
    
    def add_asset_reference(self, asset_id: Optional[str] = None,
                          type_: Optional[str] = None,
                          qualifier_id: Optional[str] = None,
                          ref_object: Optional['AssetCrossReference'] = None) -> None:
        """Add asset cross-reference to this entity.
        
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
    
    def delete_asset_reference(self, asset_id: Optional[str] = None,
                             type_: Optional[str] = None,
                             qualifier_id: Optional[str] = None,
                             delete_ref_object: Optional['DeleteAssetCrossReference'] = None) -> None:
        """Delete/sever asset reference from this entity.
        
        Can be called two ways:
        1. With parameters: delete_asset_reference(asset_id="A001")
        2. With object: delete_asset_reference(delete_ref_object=delete_ref_obj)
        """
        from .deletion import DeleteAssetCrossReference
        
        if delete_ref_object is not None:
            delete_ref = delete_ref_object
        else:
            delete_ref = DeleteAssetCrossReference({
                "AssetID": asset_id,
                "Type": type_,
                "QualifierID": qualifier_id
            })
        
        if not isinstance(self._data["DeleteAssetCrossReference"], list):
            self._data["DeleteAssetCrossReference"] = []
        self._data["DeleteAssetCrossReference"].append(delete_ref)
    
    # ===== Nested Entity Methods =====
    
    def add_nested_entity(self, entity: Optional['Entity'] = None,
                         **kwargs) -> None:
        """Add nested child entity.
        
        Can be called two ways:
        1. With object: add_nested_entity(entity=child_entity)
        2. With parameters: add_nested_entity(ID="E002", Name="Child")
        """
        if entity is not None:
            nested = entity
        else:
            nested = Entity(kwargs)
        
        if not isinstance(self._data["Entity"], list):
            self._data["Entity"] = []
        self._data["Entity"].append(nested)
