"""Classification model for STEP XML Client.

Defines the Classification entity class for representing hierarchical product categorization
in STEP MDM. Classifications organize products into taxonomies and support cross-references.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import ProductCrossReference, ClassificationCrossReference, EntityCrossReference, AssetCrossReference
    from .deletion import DeleteProductCrossReference, DeleteClassificationCrossReference, DeleteEntityCrossReference, DeleteAssetCrossReference
    from .asset import Asset
    from .complex_elements import SequenceProduct, CurrentTasks, Task, Terms, Term, Tables


class Classification(BaseObject):
    """Classification entity in STEP MDM.

    Common ``data`` keys:
    - ``ID``, ``ParentID``, ``UserTypeID``, ``QualifierID``
    - ``Name``
    - ``KeyValue`` / ``ParentKeyValue``
    - ``Values``

    Additional supported children include ``SequenceProduct``, ``Tables``,
    embedded ``Asset``, ``CurrentTasks`` and standard cross-references.

    Usage examples:
        Dict-first style::

            cls = Classification({"ID": "C100", "UserTypeID": "UT_CLASS"})
            cls.add_sequence_product(product_id="P100")
            cls.add_current_task({
                "STEPWorkflowID": "WF1",
                "StateID": "S1",
                "AssigneeID": "U1",
                "AssignedToGroup": True,
                "EntryTime": "2026-01-01T00:00:00Z",
            })

        Pre-built object style::

            from stepxmlclient.model import SequenceProduct, Tables
            cls = Classification({"ID": "C101", "UserTypeID": "UT_CLASS"})
            cls.add_sequence_product(sequence_object=SequenceProduct({"ID": "P101"}))
            cls.add_table(tables_object=Tables({"Table": [{"ID": "T1"}]}))
    """
    _GROUP_NAME: str = 'classifications'
    _TAG_NAME: str = 'Classification'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentID", "UserTypeID", "QualifierID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "KeyValue",
        "ParentKeyValue",
        "SequenceProduct",
        "Classification",  # Nested classifications
        "DeleteSuppressedProductReference",
        "DeleteProductReference",
        "ProductReference",
        "DeleteProductCrossReference",
        "DeleteSuppressedProductCrossReference",
        "SuppressedProductCrossReference",
        "ProductCrossReference",
        "DeleteSuppressedClassificationCrossReference",
        "DeleteClassificationCrossReference",
        "SuppressedClassificationCrossReference",
        "ClassificationCrossReference",
        "DeleteSuppressedEntityCrossReference",
        "DeleteEntityCrossReference",
        "SuppressedEntityCrossReference",
        "EntityCrossReference",
        "DeleteSuppressedAssetCrossReference",
        "DeleteAssetCrossReference",
        "SuppressedAssetCrossReference",
        "AssetCrossReference",
        "DeleteAttributeLink",
        "AttributeLink",
        "DeleteDataContainerTypeLink",
        "DataContainerTypeLink",
        "MetaData",
        "Tables",
        "Asset",
        "PublicationGroup",
        "CurrentTasks",
        "Values"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize relation lists if not provided
        for rel_name in ["SequenceProduct", "ProductReference", "ProductCrossReference",
                "DeleteSuppressedProductReference", "DeleteProductReference", "DeleteProductCrossReference",
                "DeleteSuppressedProductCrossReference", "SuppressedProductCrossReference",
                        "ClassificationCrossReference", "DeleteClassificationCrossReference",
                        "SuppressedClassificationCrossReference", "DeleteSuppressedClassificationCrossReference",
                        "EntityCrossReference", "DeleteEntityCrossReference",
                        "SuppressedEntityCrossReference", "DeleteSuppressedEntityCrossReference",
                        "AssetCrossReference", "DeleteAssetCrossReference", "DeleteSuppressedAssetCrossReference",
                        "SuppressedAssetCrossReference", "DeleteAttributeLink", "AttributeLink",
                        "DeleteDataContainerTypeLink", "DataContainerTypeLink", "Tables", "Asset",
                        "PublicationGroup", "CurrentTasks", "Values"]:
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
    
    # ===== Classification Reference Methods =====
    
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
    
    # ===== Entity Reference Methods =====
    
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
    
    # ===== Asset Reference Methods =====
    
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
    
    def add_nested_classification(self, classification: Optional['Classification'] = None,
                                 **kwargs) -> None:
        """Add nested ``Classification``.

        Either pass ``classification`` object or provide kwargs like
        ``ID`` and ``Name``.
        """
        if classification is not None:
            nested = classification
        else:
            nested = Classification(kwargs)
        
        if not isinstance(self._data["Classification"], list):
            self._data["Classification"] = []
        self._data["Classification"].append(nested)

    def add_sequence_product(self,
                             product_id: Optional[str] = None,
                             changed: Optional[bool] = None,
                             key_values: Optional[List[Dict[str, Any]]] = None,
                             sequence_data: Optional[Dict[str, Any]] = None,
                             sequence_object: Optional['SequenceProduct'] = None) -> None:
        """Add ``SequenceProduct`` entry.

        XSD fields: ``ID`` (required), ``Changed`` (optional), ``KeyValue``
        (optional list).
        """
        if sequence_object is not None:
            entry: Any = sequence_object
        elif sequence_data is not None:
            entry = sequence_data
        else:
            entry = {"ID": product_id, "Changed": changed, "KeyValue": key_values}

        if not isinstance(self._data.get("SequenceProduct"), list):
            self._data["SequenceProduct"] = []
        self._data["SequenceProduct"].append(entry)

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

    def add_table(self,
                  table_data: Optional[Dict[str, Any]] = None,
                  tables_object: Optional['Tables'] = None) -> None:
        """Add ``Tables`` wrapper.

        ``table_data`` supports container forms like:
        - ``{"Table": {...}}``
        - ``{"TableDefinition": {...}}``
        """
        from .complex_elements import Tables

        if tables_object is not None:
            entry: Any = tables_object
        else:
            payload = table_data or {}
            if "Table" not in payload and "TableDefinition" not in payload:
                payload = {"Table": [payload]}
            entry = Tables(payload)

        if not isinstance(self._data.get("Tables"), list):
            self._data["Tables"] = []
        self._data["Tables"].append(entry)

    def add_asset(self, asset: Optional['Asset'] = None, **kwargs) -> None:
        """Add embedded ``Asset`` child.

        Pass either a pre-built ``Asset`` object or kwargs for ``Asset(...)``.
        """
        from .asset import Asset

        entry = asset if asset is not None else Asset(kwargs)
        if not isinstance(self._data.get("Asset"), list):
            self._data["Asset"] = []
        self._data["Asset"].append(entry)
