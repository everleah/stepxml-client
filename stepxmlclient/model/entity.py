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
    from .complex_elements import CurrentTasks, Task, Terms, Term


class Entity(BaseObject):
    """Entity model in STEP MDM.

    Common ``data`` keys:
    - ``ID``, ``ParentID``, ``UserTypeID``, ``QualifierID``
    - ``Name``
    - ``KeyValue`` / ``ParentKeyValue``
    - ``Values`` and ``DataContainers``

    Supports cross-references and also ``CurrentTasks`` / ``Terms`` children.
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
        """Add ``ProductCrossReference``.

        Fields: ``ProductID``, ``Type``, ``QualifierID``, ``MountLocation``.
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
        """Add ``DeleteProductCrossReference``.

        Fields: ``ProductID``, ``Type``, ``QualifierID``, ``MountLocation``.
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
        """Add ``ClassificationCrossReference``.

        Fields: ``ClassificationID``, ``Type``, ``QualifierID``,
        ``MountLocation``.
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
        """Add ``DeleteClassificationCrossReference``.

        Fields: ``ClassificationID``, ``Type``, ``QualifierID``,
        ``MountLocation``.
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
        """Add ``EntityCrossReference``.

        Fields: ``EntityID``, ``Type``, ``QualifierID``, ``MountLocation``.
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
        """Add ``DeleteEntityCrossReference``.

        Fields: ``EntityID``, ``Type``, ``QualifierID``, ``MountLocation``.
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
        """Add ``AssetCrossReference``.

        Fields: ``AssetID``, ``Type``, ``QualifierID``.
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
        """Add ``DeleteAssetCrossReference``.

        Fields: ``AssetID``, ``Type``, ``QualifierID``.
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
        """Add nested ``Entity`` object.

        Pass either ``entity`` or kwargs for ``Entity(...)``.
        """
        if entity is not None:
            nested = entity
        else:
            nested = Entity(kwargs)
        
        if not isinstance(self._data["Entity"], list):
            self._data["Entity"] = []
        self._data["Entity"].append(nested)

    def add_current_task(self,
                         task_data: Optional[Dict[str, Any]] = None,
                         task_object: Optional['Task'] = None,
                         current_tasks_object: Optional['CurrentTasks'] = None) -> None:
        """Add ``CurrentTasks`` with task entries.

        Task keys: ``STEPWorkflowID``, ``StateID``, ``AssigneeID``,
        ``AssignedToGroup``, ``EntryTime``, optional ``Deadline``, ``Priority``,
        ``StatusID``.
        """
        from .complex_elements import CurrentTasks, Task

        if current_tasks_object is not None:
            entry: Any = current_tasks_object
        else:
            task = task_object or Task(task_data or {})
            entry = CurrentTasks({"Task": [task]})

        if not isinstance(self._data.get("CurrentTasks"), list):
            self._data["CurrentTasks"] = []
        self._data["CurrentTasks"].append(entry)

    def add_term(self,
                 term_data: Optional[Dict[str, Any]] = None,
                 term_object: Optional['Term'] = None,
                 terms_object: Optional['Terms'] = None) -> None:
        """Add ``Terms`` with one or more term entries.

        Term keys: ``TermsListID``, ``MinimumQuantity``, ``MaximumQuantity``,
        ``StartDate``, ``EndDate``, ``LeadTime``, ``UnitID``, ``LotSize`` and
        optional text value via ``value``.
        """
        from .complex_elements import Terms, Term

        if terms_object is not None:
            entry: Any = terms_object
        else:
            term = term_object or Term(term_data or {})
            entry = Terms({"Term": [term]})

        if not isinstance(self._data.get("Terms"), list):
            self._data["Terms"] = []
        self._data["Terms"].append(entry)
