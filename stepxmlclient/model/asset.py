"""Asset model for STEP XML Client.

Defines the Asset entity class for representing binary asset files in STEP MDM.
Assets represent digital files (images, documents, videos, etc.) that can be associated
with products and other entities.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import ClassificationReference, EntityCrossReference

class Asset(BaseObject):
    """Asset entity in STEP MDM.
    
    Represents a binary asset (file) with metadata and relationships.
    
    Attributes:
        ID: Unique asset identifier
        Name: Asset name or description
        KeyValue: Optional key value for asset lookup
        Values: Dictionary of attribute ID to attribute values
        ClassificationReference: List of classifications
        EntityCrossReference: List of linked business entities
    """
    _GROUP_NAME: str = 'assets'
    _TAG_NAME: str = 'Asset'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "UserTypeID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = ["Name", "KeyValue"]
    _CHILDREN_NAMES: List[str] = [
        "AssetPushLocation",
        "DeleteSuppressedClassificationReference",
        "DeleteClassificationReference",
        "SuppressedClassificationReference",
        "ClassificationReference",
        "DeleteSuppressedEntityCrossReference",
        "DeleteEntityCrossReference",
        "SuppressedEntityCrossReference",
        "EntityCrossReference",
        "Values",
        "CurrentTasks",
        "Pages",
        "AssetContent",
        "AssetBinaryContent"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in [
            "DeleteSuppressedClassificationReference",
            "DeleteClassificationReference",
            "SuppressedClassificationReference",
            "ClassificationReference",
            "DeleteSuppressedEntityCrossReference",
            "DeleteEntityCrossReference",
            "SuppressedEntityCrossReference",
            "EntityCrossReference",
        ]:
            if rel_name not in self._data:
                self._data[rel_name] = []

        # Backward compatibility: older code may still pass this legacy key.
        legacy_class_refs = self._data.get("ClassificationCrossReference")
        if legacy_class_refs and not self._data.get("ClassificationReference"):
            self._data["ClassificationReference"] = legacy_class_refs
    
    # ===== Classification Reference Methods =====
    
    def add_classification_reference(self, classification_id: Optional[str] = None, 
                                   type_: Optional[str] = None,
                                   qualifier_id: Optional[str] = None,
                                   mount_location: Optional[str] = None,
                                   ref_object: Optional['ClassificationReference'] = None) -> None:
        """Add classification reference to this asset.
        
        Can be called two ways:
        1. With parameters: add_classification_reference(classification_id="C001")
        2. With object: add_classification_reference(ref_object=class_ref_obj)
        """
        from .relations import ClassificationReference, ClassificationCrossReference
        
        if ref_object is not None:
            # Use provided object
            ref = ref_object
            if isinstance(ref, ClassificationCrossReference):
                # Gracefully normalize legacy object type to the XSD-compliant tag.
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
