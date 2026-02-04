"""Attribute model for STEP XML Client.

Defines the Attribute entity class for representing attribute definitions in STEP MDM.
Attributes define the properties that can be assigned to products, assets, and entities.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    pass


class Attribute(BaseObject):
    """Attribute definition in STEP MDM.
    
    Defines a property/characteristic that can be assigned to products, assets, and entities.
    Supports multiple data types, validation rules, units, and dimensional analysis.
    
    Attributes:
        ID: Unique attribute identifier
        DefaultUnitID: Default unit for numeric values
        ProductMode: 'Normal' or 'Property' (property attributes have limited usage)
        CryptographicKeyID: Optional encryption key for sensitive data
        HierarchicalFiltering: Whether to use hierarchical filtering
        ClassificationHierarchicalFiltering: Whether to use classification hierarchy filtering
        ExternallyMaintained: Whether values are maintained externally
        FullTextIndexed: Whether to index for full-text search
        MultiValued: Whether attribute can have multiple values
        Mandatory: Whether attribute is required
        Derived: Whether value is computed/derived
        Selected: Whether attribute is selected in UI
        Referenced: Whether attribute is referenced elsewhere
        Changed: Whether attribute was modified
        Deleted: Whether attribute is marked for deletion
        Name: Attribute name (localized)
        Validation: Data type validation configuration
        ListOfValueLink: Link to List-of-Values for choice attributes
        ValueTemplate: Template for attribute values
        UnitTemplate: Template for units
        DimensionLink: Links to dimensional definitions
        MetaData: Metadata associated with attribute
        AttributeGroupLink: Links to attribute groups
        UserTypeLink: Links to user types
        LinkType: Link type associations
        ValueFilter: Filters for attribute values
        CurrentTasks: Current task information
    """
    _GROUP_NAME: str = 'attributes'
    _TAG_NAME: str = 'Attribute'
    _ATTRIBUTE_NAMES: List[str] = [
        "ID", "DefaultUnitID", "ProductMode", "CryptographicKeyID",
        "HierarchicalFiltering", "ClassificationHierarchicalFiltering",
        "ExternallyMaintained", "FullTextIndexed", "MultiValued",
        "Mandatory", "Derived", "Selected", "Referenced", "Changed", "Deleted"
    ]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "Validation",
        "ListOfValueLink",
        "ValueTemplate",
        "UnitTemplate",
        "DimensionLink",
        "MetaData",
        "AttributeGroupLink",
        "UserTypeLink",
        "LinkType",
        "ValueFilter",
        "CurrentTasks"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize link lists if not provided
        for link_name in ["DimensionLink", "AttributeGroupLink", "UserTypeLink", "LinkType"]:
            if link_name not in self._data:
                self._data[link_name] = []


class AttributeGroup(BaseObject):
    """AttributeGroup - hierarchical grouping of attributes for organizational purposes.
    
    Supports:
    - Nested attribute groups (parent/child hierarchy)
    - Workbench visibility settings
    - Manual sorting control
    - Profiling exclusion options
    - Configuration/view definitions
    - Boolean state tracking (ShowInWorkbench, ExcludeFromProfiling, Selected, Referenced, etc.)
    """
    _GROUP_NAME: str = 'attributegroups'
    _TAG_NAME: str = 'AttributeGroup'
    _ATTRIBUTE_NAMES: List[str] = [
        "ID", "ParentID", "ShowInWorkbench", "ExcludeFromProfiling",
        "Referenced", "ManuallySorted", "Selected", "Changed", "Deleted"
    ]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "MetaData",
        "Configuration",
        "AttributeSequence",
        "AttributeGroup"  # Nested attribute groups
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize nested attribute groups list
        if "AttributeGroup" not in self._data:
            self._data["AttributeGroup"] = []
    
    def add_nested_attribute_group(self, attribute_group: Optional['AttributeGroup'] = None,
                                  **kwargs) -> None:
        """Add nested child attribute group.
        
        Can be called two ways:
        1. With object: add_nested_attribute_group(attribute_group=child_group)
        2. With parameters: add_nested_attribute_group(ID="AG002", Name="Child Group")
        """
        if attribute_group is not None:
            nested = attribute_group
        else:
            nested = AttributeGroup(kwargs)
        
        if not isinstance(self._data["AttributeGroup"], list):
            self._data["AttributeGroup"] = []
        self._data["AttributeGroup"].append(nested)


class ListOfValues(BaseObject):
    """ListOfValues - defines a set of allowed values for an attribute with optional grouping.
    
    Supports:
    - Hierarchical value groups (parent/child)
    - Value definitions and deletion
    - User-contributed values
    - Value ID usage control
    - Validation rules
    - Dimensional analysis (DimensionLink)
    - Unit definitions (DefaultUnitID)
    - Boolean state tracking (AllowUserValueAddition, UseValueID, ReplaceListOfValuesValues, etc.)
    """
    _GROUP_NAME: str = 'listofvalues'
    _TAG_NAME: str = 'ListOfValues'
    _ATTRIBUTE_NAMES: List[str] = [
        "ID", "ParentID", "AllowUserValueAddition", "UseValueID",
        "IDPattern", "ReplaceListOfValuesValues", "DefaultUnitID"
    ]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "Validation",
        "DimensionLink",
        "MetaData",
        "AttributeGroupLink",
        "Value",
        "ValueGroup",
        "DeleteValue",
        "ListOfValuesGroup"  # Nested groups
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize link lists if not provided
        for link_name in ["DimensionLink", "AttributeGroupLink"]:
            if link_name not in self._data:
                self._data[link_name] = []
        
        # Initialize value lists
        for value_name in ["Value", "ValueGroup", "DeleteValue", "ListOfValuesGroup"]:
            if value_name not in self._data:
                self._data[value_name] = []
    
    def add_value(self, value_id: Optional[str] = None,
                 name: Optional[str] = None,
                 **kwargs) -> None:
        """Add a value to this list of values.
        
        Args:
            value_id: ID of the value (if UseValueID=true)
            name: Display name of the value
            **kwargs: Additional attributes to pass to Value element
        """
        value_dict = {}
        if value_id is not None:
            value_dict["ID"] = value_id
        if name is not None:
            value_dict["Name"] = name
        value_dict.update(kwargs)
        
        if not isinstance(self._data["Value"], list):
            self._data["Value"] = []
        self._data["Value"].append(value_dict)
    
    def delete_value(self, value_id: str) -> None:
        """Mark a value for deletion from this list of values.
        
        Args:
            value_id: ID of the value to delete
        """
        delete_dict = {"ID": value_id}
        
        if not isinstance(self._data["DeleteValue"], list):
            self._data["DeleteValue"] = []
        self._data["DeleteValue"].append(delete_dict)
    
    def add_value_group(self, value_group: Optional['ValueGroup'] = None,
                       **kwargs) -> None:
        """Add a value group (for grouped value organization).
        
        Can be called two ways:
        1. With object: add_value_group(value_group=group_obj)
        2. With parameters: add_value_group(ID="VG001", Name="Group Name")
        """
        if value_group is not None:
            group = value_group
        else:
            group = ValueGroup(kwargs)
        
        if not isinstance(self._data["ValueGroup"], list):
            self._data["ValueGroup"] = []
        self._data["ValueGroup"].append(group)
    
    def add_nested_list_of_values_group(self, group: Optional['ListOfValuesGroup'] = None,
                                       **kwargs) -> None:
        """Add nested list of values group for hierarchical organization.
        
        Can be called two ways:
        1. With object: add_nested_list_of_values_group(group=child_group)
        2. With parameters: add_nested_list_of_values_group(ID="LOG001", Name="Group")
        """
        if group is not None:
            nested = group
        else:
            nested = ListOfValuesGroup(kwargs)
        
        if not isinstance(self._data["ListOfValuesGroup"], list):
            self._data["ListOfValuesGroup"] = []
        self._data["ListOfValuesGroup"].append(nested)


class ValueGroup(BaseObject):
    """ValueGroup - groups related values within a ListOfValues for organizational purposes."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ValueGroup'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["Value"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        if "Value" not in self._data:
            self._data["Value"] = []


class ListOfValuesGroup(BaseObject):
    """ListOfValuesGroup - hierarchical grouping of lists of values."""
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ListOfValuesGroup'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentID", "Selected", "Referenced", "Changed"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "MetaData",
        "AttributeGroupLink",
        "ListOfValuesGroup"  # Nested groups
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        if "AttributeGroupLink" not in self._data:
            self._data["AttributeGroupLink"] = []
        if "ListOfValuesGroup" not in self._data:
            self._data["ListOfValuesGroup"] = []
    
    def add_nested_list_of_values_group(self, group: Optional['ListOfValuesGroup'] = None,
                                       **kwargs) -> None:
        """Add nested list of values group.
        
        Can be called two ways:
        1. With object: add_nested_list_of_values_group(group=child_group)
        2. With parameters: add_nested_list_of_values_group(ID="LOG002", Name="Child")
        """
        if group is not None:
            nested = group
        else:
            nested = ListOfValuesGroup(kwargs)
        
        if not isinstance(self._data["ListOfValuesGroup"], list):
            self._data["ListOfValuesGroup"] = []
        self._data["ListOfValuesGroup"].append(nested)
