"""Asset model for STEP XML Client.

Defines the Asset entity class for representing binary asset files in STEP MDM.
Assets represent digital files (images, documents, videos, etc.) that can be associated
with products and other entities.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    from .relations import ClassificationReference, EntityCrossReference
    from .complex_elements import AssetPushLocation, AssetContent, AssetBinaryContent

class Asset(BaseObject):
    """Asset entity in STEP MDM.

    This model serializes to the STEP ``Asset`` element and supports helper
    methods for common relationship/content elements.

    Common top-level ``data`` keys:
    - ``ID`` (str): Asset identifier
    - ``UserTypeID`` (str): STEP object type
    - ``Name`` (str or dict/list): Asset name
    - ``KeyValue`` (dict or list): External key references
      (for example ``{"KeyID": "ExternalKey", "value": "A-100"}``)
    - ``Values`` (dict): Attribute values map

    Usage examples:
        Dict-first style::

            asset = Asset({"ID": "A100", "UserTypeID": "UT_ASSET"})
            asset.add_classification_reference(classification_id="C_ASSETS")
            asset.add_asset_push_location({"ConfigurationID": "PUSH_CFG", "Status": "DONE"})

        Pre-built object style::

            from stepxmlclient.model import AssetContent, AssetContentSpecification
            asset = Asset({"ID": "A101", "UserTypeID": "UT_ASSET"})
            asset.add_asset_content(content_object=AssetContent({
                "QualifierID": "en",
                "AssetContentSpecification": [
                    AssetContentSpecification({"RelativeURL": "/assets/a101.jpg"})
                ],
            }))
    """
    _GROUP_NAME: str = 'assets'
    _TAG_NAME: str = 'Asset'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "UserTypeID", "Changed", "Republished", "Selected", "Referenced"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = [
        "KeyValue",
        "Name",
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
        """Add a ``ClassificationReference`` child.

        If a legacy ``ClassificationCrossReference`` object is passed, it is
        normalized to ``ClassificationReference``.

        Args:
            classification_id: Value for ``ClassificationID``.
            type_: Optional ``Type``.
            qualifier_id: Optional ``QualifierID``.
            mount_location: Optional ``MountLocation``.
            ref_object: Pre-built relation object.
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
        """Add an ``EntityCrossReference`` child.

        Args:
            entity_id: Value for ``EntityID``.
            type_: Optional ``Type``.
            qualifier_id: Optional ``QualifierID``.
            mount_location: Optional ``MountLocation``.
            ref_object: Pre-built ``EntityCrossReference`` instance.
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

    # ===== Additional Asset Content Helpers =====

    def add_asset_push_location(self, push_location_data: Optional[Dict[str, Any]] = None) -> None:
        """Add an ``AssetPushLocation`` child entry.

        Args:
            push_location_data: Dictionary with keys:
                - ``ConfigurationID`` (required)
                - ``Status`` (optional)
                - ``QualifierID`` (optional)
                - ``value`` or ``text`` (optional element text)
        """
        if not isinstance(self._data.get("AssetPushLocation"), list):
            self._data["AssetPushLocation"] = []
        self._data["AssetPushLocation"].append(push_location_data or {})

    def add_asset_push_location_object(self, push_location_object: 'AssetPushLocation') -> None:
        """Add pre-built ``AssetPushLocation`` object."""
        if not isinstance(self._data.get("AssetPushLocation"), list):
            self._data["AssetPushLocation"] = []
        self._data["AssetPushLocation"].append(push_location_object)

    def add_current_task(self, task_data: Optional[Dict[str, Any]] = None) -> None:
        """Add a ``CurrentTasks`` child entry.

        Args:
            task_data: Dictionary mapped to ``Task`` attributes. Typical keys:
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

    def add_page(self, page_data: Optional[Dict[str, Any]] = None) -> None:
        """Add a ``Pages`` child entry.

        Args:
            page_data: Dictionary with optional top-level key ``Page``.
                ``Page`` objects commonly use attributes ``VersionID`` (required
                by XSD), ``ID`` and ``PageNumber``.
        """
        if not isinstance(self._data.get("Pages"), list):
            self._data["Pages"] = []
        self._data["Pages"].append(page_data or {})

    def add_asset_content(self,
                         content_data: Optional[Dict[str, Any]] = None,
                         content_object: Optional['AssetContent'] = None) -> None:
        """Add an ``AssetContent`` child entry.

        Args:
            content_data: Dictionary with keys:
                - ``QualifierID`` (optional)
                - ``AssetContentSpecification`` (optional list), each entry with
                  ``ImageConversionConfigurationID``, ``IncludesBinaryContent``,
                  ``RelativeURL``
            content_object: Pre-built ``AssetContent`` object.
        """
        if not isinstance(self._data.get("AssetContent"), list):
            self._data["AssetContent"] = []
        self._data["AssetContent"].append(content_object or content_data or {})

    def add_asset_binary_content(self,
                                binary_content_data: Optional[Dict[str, Any]] = None,
                                binary_content_object: Optional['AssetBinaryContent'] = None) -> None:
        """Add an ``AssetBinaryContent`` child entry.

        Args:
            binary_content_data: Dictionary with keys:
                - ``QualifierID`` (optional)
                - ``ImageConversionConfigurationID`` (optional)
                - ``MIMEType`` (optional)
                - ``Checksum`` (optional)
                - ``Filename`` (optional)
                - ``BinaryContent`` (required for full XSD compliance), e.g.
                  ``{"value": "<base64>"}``
            binary_content_object: Pre-built ``AssetBinaryContent`` object.
        """
        if not isinstance(self._data.get("AssetBinaryContent"), list):
            self._data["AssetBinaryContent"] = []
        self._data["AssetBinaryContent"].append(binary_content_object or binary_content_data or {})
