from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import (
        AssetCrossReference,
        ProductCrossReference,
        ClassificationReference,
        ClassificationCrossReference,
        EntityCrossReference,
    )
    from .deletion import DeleteAssetCrossReference, DeleteProductCrossReference
    from .complex_elements import (
        STEPWorkflowStateBind,
        SequenceProduct,
        OverrideSubProduct,
        PackagingReference,
    )


class Product(BaseObject):
    """Product entity in STEP MDM.

    This model serializes to STEP ``Product`` and supports both direct dictionary
    payloads and helper methods.

    Common top-level ``data`` keys:
    - ``ID`` (str): Product identifier
    - ``ParentId`` (str): Parent product ID
    - ``UserTypeID`` (str): Product object type
    - ``Name`` (str): Product name
    - ``KeyValue`` (dict/list): external keys, e.g. ``{"KeyID": "ExternalKey", "value": "P-1"}``
    - ``Values`` (dict): attribute value map

    Frequently used child collections:
    - ``AssetCrossReference``
    - ``ProductCrossReference``
    - ``ClassificationReference``
    - ``ClassificationCrossReference``
    - ``EntityCrossReference``
    """

    _GROUP_NAME: str = "products"
    _TAG_NAME: str = "Product"
    _ATTRIBUTE_NAMES: List[str] = [
        "ID",
        "ParentId",
        "UserTypeID",
        "QualifierID",
        "Changed",
        "Republished",
        "Selected",
        "Referenced",
    ]
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
        "PackagingReference",
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        for rel_name in [
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
            "DeleteAssetCrossReference",
            "DeleteProductCrossReference",
            "SequenceProduct",
            "CurrentTasks",
            "Terms",
            "Tables",
            "OverrideSubProduct",
            "PackagingReference",
        ]:
            if rel_name not in self._data:
                self._data[rel_name] = []

    def add_asset_reference(
        self,
        asset_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        ref_object: Optional["AssetCrossReference"] = None,
    ) -> None:
        """Add an ``AssetCrossReference``.

        Fields:
        - ``AssetID``
        - ``Type``
        - ``QualifierID``
        """
        from .relations import AssetCrossReference

        ref = ref_object or AssetCrossReference(
            {"AssetID": asset_id, "Type": type_, "QualifierID": qualifier_id}
        )
        if not isinstance(self._data["AssetCrossReference"], list):
            self._data["AssetCrossReference"] = []
        self._data["AssetCrossReference"].append(ref)

    def delete_asset_reference(
        self,
        asset_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        delete_ref_object: Optional["DeleteAssetCrossReference"] = None,
    ) -> None:
        """Add ``DeleteAssetCrossReference`` to remove an asset link.

        Fields:
        - ``AssetID``
        - ``Type``
        - ``QualifierID``
        """
        from .deletion import DeleteAssetCrossReference

        delete_ref = delete_ref_object or DeleteAssetCrossReference(
            {"AssetID": asset_id, "Type": type_, "QualifierID": qualifier_id}
        )
        if not isinstance(self._data["DeleteAssetCrossReference"], list):
            self._data["DeleteAssetCrossReference"] = []
        self._data["DeleteAssetCrossReference"].append(delete_ref)

    def add_product_reference(
        self,
        product_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        mount_location: Optional[str] = None,
        ref_object: Optional["ProductCrossReference"] = None,
    ) -> None:
        """Add a ``ProductCrossReference``.

        Fields:
        - ``ProductID``
        - ``Type``
        - ``QualifierID``
        - ``MountLocation``
        """
        from .relations import ProductCrossReference

        ref = ref_object or ProductCrossReference(
            {
                "ProductID": product_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location,
            }
        )
        if not isinstance(self._data["ProductCrossReference"], list):
            self._data["ProductCrossReference"] = []
        self._data["ProductCrossReference"].append(ref)

    def delete_product_reference(
        self,
        product_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        mount_location: Optional[str] = None,
        delete_ref_object: Optional["DeleteProductCrossReference"] = None,
    ) -> None:
        """Add ``DeleteProductCrossReference`` to remove a product link.

        Fields:
        - ``ProductID``
        - ``Type``
        - ``QualifierID``
        - ``MountLocation``
        """
        from .deletion import DeleteProductCrossReference

        delete_ref = delete_ref_object or DeleteProductCrossReference(
            {
                "ProductID": product_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location,
            }
        )
        if not isinstance(self._data["DeleteProductCrossReference"], list):
            self._data["DeleteProductCrossReference"] = []
        self._data["DeleteProductCrossReference"].append(delete_ref)

    def add_classification_reference(
        self,
        classification_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        mount_location: Optional[str] = None,
        ref_object: Optional["ClassificationReference"] = None,
    ) -> None:
        """Add ``ClassificationReference`` (not CrossReference).

        Fields:
        - ``ClassificationID``
        - ``Type``
        - ``QualifierID``
        - ``MountLocation``
        """
        from .relations import ClassificationReference, ClassificationCrossReference

        if ref_object is not None:
            ref = ref_object
            if isinstance(ref, ClassificationCrossReference):
                ref = ClassificationReference(dict(ref._data))
        else:
            ref = ClassificationReference(
                {
                    "ClassificationID": classification_id,
                    "Type": type_,
                    "QualifierID": qualifier_id,
                    "MountLocation": mount_location,
                }
            )

        if not isinstance(self._data["ClassificationReference"], list):
            self._data["ClassificationReference"] = []
        self._data["ClassificationReference"].append(ref)

    def add_classification_cross_reference(
        self,
        classification_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        mount_location: Optional[str] = None,
        ref_object: Optional["ClassificationCrossReference"] = None,
    ) -> None:
        """Add explicit ``ClassificationCrossReference``.

        Fields:
        - ``ClassificationID``
        - ``Type``
        - ``QualifierID``
        - ``MountLocation``
        """
        from .relations import ClassificationCrossReference

        ref = ref_object or ClassificationCrossReference(
            {
                "ClassificationID": classification_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location,
            }
        )
        if not isinstance(self._data["ClassificationCrossReference"], list):
            self._data["ClassificationCrossReference"] = []
        self._data["ClassificationCrossReference"].append(ref)

    def add_entity_reference(
        self,
        entity_id: Optional[str] = None,
        type_: Optional[str] = None,
        qualifier_id: Optional[str] = None,
        mount_location: Optional[str] = None,
        ref_object: Optional["EntityCrossReference"] = None,
    ) -> None:
        """Add ``EntityCrossReference``.

        Fields:
        - ``EntityID``
        - ``Type``
        - ``QualifierID``
        - ``MountLocation``
        """
        from .relations import EntityCrossReference

        ref = ref_object or EntityCrossReference(
            {
                "EntityID": entity_id,
                "Type": type_,
                "QualifierID": qualifier_id,
                "MountLocation": mount_location,
            }
        )
        if not isinstance(self._data["EntityCrossReference"], list):
            self._data["EntityCrossReference"] = []
        self._data["EntityCrossReference"].append(ref)

    def set_workflow_state_bind(
        self,
        workflow_id: Optional[str] = None,
        state_id: Optional[str] = None,
        bind_data: Optional[Dict[str, Any]] = None,
        bind_object: Optional["STEPWorkflowStateBind"] = None,
    ) -> None:
        """Set ``STEPWorkflowStateBind``.

        Required XSD keys:
        - ``WorkflowID``
        - ``StateID``

        Compatibility:
        - legacy dict keys ``ID`` and ``CurrentStateID`` are normalized.
        """
        if bind_object is not None:
            self._data["STEPWorkflowStateBind"] = bind_object
            return

        if bind_data is not None:
            normalized = dict(bind_data)
            if "WorkflowID" not in normalized and "ID" in normalized:
                normalized["WorkflowID"] = normalized.pop("ID")
            if "StateID" not in normalized and "CurrentStateID" in normalized:
                normalized["StateID"] = normalized.pop("CurrentStateID")
            self._data["STEPWorkflowStateBind"] = normalized
            return

        self._data["STEPWorkflowStateBind"] = {
            "WorkflowID": workflow_id,
            "StateID": state_id,
        }

    def add_sequence_product(
        self,
        product_id: Optional[str] = None,
        changed: Optional[bool] = None,
        key_values: Optional[List[Dict[str, Any]]] = None,
        sequence_data: Optional[Dict[str, Any]] = None,
        sequence_object: Optional["SequenceProduct"] = None,
    ) -> None:
        """Add ``SequenceProduct``.

        XSD fields:
        - ``ID`` (required)
        - ``Changed`` (optional)
        - ``KeyValue`` (optional, list)
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

    def add_current_task(self, task_data: Optional[Dict[str, Any]] = None) -> None:
        """Add ``CurrentTasks``/``Task`` data.

        Typical task keys:
        - ``STEPWorkflowID``
        - ``StateID``
        - ``AssigneeID``
        - ``AssignedToGroup``
        - ``EntryTime``
        - optional: ``Deadline``, ``Priority``, ``StatusID``
        """
        if not isinstance(self._data.get("CurrentTasks"), list):
            self._data["CurrentTasks"] = []
        self._data["CurrentTasks"].append(task_data or {})

    def add_term(self, term_data: Optional[Dict[str, Any]] = None) -> None:
        """Add ``Terms``/``Term`` data.

        Common term keys:
        - ``TermsListID``
        - ``MinimumQuantity`` / ``MaximumQuantity``
        - ``StartDate`` / ``EndDate``
        - ``LeadTime``
        - ``UnitID``
        - ``LotSize``
        - optional text value: ``value``
        """
        if not isinstance(self._data.get("Terms"), list):
            self._data["Terms"] = []
        self._data["Terms"].append(term_data or {})

    def add_table(self, table_data: Optional[Dict[str, Any]] = None) -> None:
        """Add ``Tables`` data.

        Supported container forms:
        - ``{"Table": {...}}``
        - ``{"TableDefinition": {...}}``

        Common ``Table`` attributes:
        - ``ID``
        - ``ContextID``
        - ``TableTypeID``
        """
        if not isinstance(self._data.get("Tables"), list):
            self._data["Tables"] = []
        self._data["Tables"].append(table_data or {})

    def add_override_sub_product(
        self,
        product_id: Optional[str] = None,
        analyzer_result: Optional[str] = None,
        override_data: Optional[Dict[str, Any]] = None,
        override_object: Optional["OverrideSubProduct"] = None,
    ) -> None:
        """Add ``OverrideSubProduct``.

        XSD fields:
        - ``ProductID`` (required)
        - ``AnalyzerResult`` (optional, deprecated)
        """
        if override_object is not None:
            entry: Any = override_object
        elif override_data is not None:
            entry = override_data
        else:
            entry = {"ProductID": product_id, "AnalyzerResult": analyzer_result}

        if not isinstance(self._data.get("OverrideSubProduct"), list):
            self._data["OverrideSubProduct"] = []
        self._data["OverrideSubProduct"].append(entry)

    def add_packaging_reference(
        self,
        product_id: Optional[str] = None,
        quantity: Optional[str] = None,
        packaging_data: Optional[Dict[str, Any]] = None,
        packaging_object: Optional["PackagingReference"] = None,
    ) -> None:
        """Add ``PackagingReference``.

        Required XSD fields:
        - ``ProductID``
        - ``Quantity``
        """
        if packaging_object is not None:
            entry: Any = packaging_object
        elif packaging_data is not None:
            entry = packaging_data
        else:
            entry = {"ProductID": product_id, "Quantity": quantity}

        if not isinstance(self._data.get("PackagingReference"), list):
            self._data["PackagingReference"] = []
        self._data["PackagingReference"].append(entry)


class ProductReplacementRule(BaseObject):
    _GROUP_NAME: str = "product_replacement_rules"
    _TAG_NAME: str = "Product"
    _ATTRIBUTE_NAMES: List[str] = [
        "ID",
        "ParentId",
        "UserTypeID",
        "QualifierID",
        "Changed",
        "Republished",
        "Selected",
        "Referenced",
    ]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["KeyValue", "ParentKeyValue", "Values"]
