"""Business rules and workflow models for STEP XML Client.

Defines business logic execution entities including Business Rules and Workflows
that control behavior and processes within STEP MDM systems.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    pass


class BusinessRule(BaseObject):
    """Business logic executable in STEP MDM.
    
    Defines executable business logic including actions, conditions, functions, and libraries.
    Business rules contain logic that executes within the STEP system to automate processes.
    
    Supports:
    - Multiple rule types (Action, Condition, Function, Library)
    - Rule scope (Local or Global)
    - Privileged execution mode
    - Dependencies on other rules
    - Multi-language names and descriptions
    - Setup group configuration
    
    Attributes:
        ID: Unique business rule identifier
        Type: Rule type (Action, Condition, Function, Library, etc.)
        Scope: Scope of execution (Local or Global)
        RunPrivileged: Whether to run with elevated privileges
        Name: Rule name (localized)
        Description: Rule description (localized)
        Dependency: List of dependent rules
        FunctionDependency: List of function dependencies
        OnApprove: On-approval behavior configuration
        Configuration: Rule-specific configuration
        ValidObjectTypes: Object types this rule applies to
        SetupGroupLink: Link to setup groups
    """
    _GROUP_NAME: str = 'businessrules'
    _TAG_NAME: str = 'BusinessRule'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "Type", "Scope", "RunPrivileged", "Selected", "Referenced", "Changed"]
    _TEXT_NAMES: List[str] = ["Name", "Description"]
    _CHILDREN_NAMES: List[str] = [
        "Dependency",
        "FunctionDependency",
        "OnApprove",
        "Configuration",
        "ValidObjectTypes",
        "SetupGroupLink"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize dependency lists if not provided
        for dep_name in ["Dependency", "FunctionDependency"]:
            if dep_name not in self._data:
                self._data[dep_name] = []


class Workflow(BaseObject):
    """Workflow - orchestrates business processes in STEP.
    
    Workflows define states, transitions, and validations that control how objects
    move through business processes. Workflows enforce rules about what operations
    are allowed in each state and what data must be valid before transitions.
    
    Supports:
    - Object type constraints (ValidUserTypeLink)
    - Start conditions
    - Embedded business rules
    - Business rule references
    - Setup group configuration
    - Multi-language names
    - Boolean state tracking (Selected, Referenced, Changed)
    
    Attributes:
        ID: Unique workflow identifier
        Name: Workflow name (localized)
        Description: Workflow description
        ValidUserTypeLink: Links to object types this workflow applies to
        ValidBusinessRuleLink: Links to relevant business rules
        StartCondition: Condition for workflow start
        STEPAction: Workflow actions
        STEPState: Workflow states
        STEPEdge: State transitions
        SetupGroupLink: Setup group associations
    """
    _GROUP_NAME: str = 'workflows'
    _TAG_NAME: str = 'Workflow'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "Selected", "Referenced", "Changed"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "MetaData",
        "ValidUserTypeLink",
        "StartCondition",
        "Configuration",
        "LocalBusinessRule",
        "BusinessRuleLink",
        "SetupGroupLink"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize link lists if not provided
        for link_name in ["ValidUserTypeLink", "LocalBusinessRule", "BusinessRuleLink"]:
            if link_name not in self._data:
                self._data[link_name] = []
    
    def add_valid_user_type_link(self, user_type_id: str) -> None:
        """Add a valid user type link to this workflow.
        
        Args:
            user_type_id: ID of the user type
        """
        if not isinstance(self._data["ValidUserTypeLink"], list):
            self._data["ValidUserTypeLink"] = []
        self._data["ValidUserTypeLink"].append(user_type_id)
    
    def add_business_rule_link(self, business_rule_id: str) -> None:
        """Add a business rule link to this workflow.
        
        Args:
            business_rule_id: ID of the business rule
        """
        if not isinstance(self._data["BusinessRuleLink"], list):
            self._data["BusinessRuleLink"] = []
        self._data["BusinessRuleLink"].append(business_rule_id)


class Collection(BaseObject):
    """Collection - represents a user-defined collection of objects.
    
    Collections group objects based on queries or manual selection.
    They provide flexible organization outside fixed hierarchies.
    
    Supports:
    - Query-based membership (QueryURL)
    - Parent collection linking for hierarchies
    - Multi-language names
    - Metadata tracking
    """
    _GROUP_NAME: str = 'collections'
    _TAG_NAME: str = 'Collection'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentID", "QueryURL"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["MetaData", "CollectionGroup"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize nested collection groups list
        if "CollectionGroup" not in self._data:
            self._data["CollectionGroup"] = []
    
    def add_nested_collection_group(self, collection_group: Optional['CollectionGroup'] = None,
                                   **kwargs) -> None:
        """Add nested collection group.
        
        Can be called two ways:
        1. With object: add_nested_collection_group(collection_group=group_obj)
        2. With parameters: add_nested_collection_group(ID="CG001", Name="Group")
        """
        if collection_group is not None:
            group = collection_group
        else:
            group = CollectionGroup(kwargs)
        
        if not isinstance(self._data["CollectionGroup"], list):
            self._data["CollectionGroup"] = []
        self._data["CollectionGroup"].append(group)


class CollectionGroup(BaseObject):
    """CollectionGroup - hierarchical grouping of collections.
    
    Collection groups organize collections and nested groups into
    logical hierarchies for better navigation and management.
    
    Supports:
    - Nested collection groups (parent/child hierarchy)
    - Nested collections
    - Multi-language names
    - Metadata tracking
    """
    _GROUP_NAME: str = 'collectiongroups'
    _TAG_NAME: str = 'CollectionGroup'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["MetaData", "CollectionGroup", "Collection"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize nested groups and collections lists
        if "CollectionGroup" not in self._data:
            self._data["CollectionGroup"] = []
        if "Collection" not in self._data:
            self._data["Collection"] = []
    
    def add_nested_collection_group(self, collection_group: Optional['CollectionGroup'] = None,
                                   **kwargs) -> None:
        """Add nested collection group.
        
        Can be called two ways:
        1. With object: add_nested_collection_group(collection_group=group_obj)
        2. With parameters: add_nested_collection_group(ID="CG002", Name="Nested")
        """
        if collection_group is not None:
            group = collection_group
        else:
            group = CollectionGroup(kwargs)
        
        if not isinstance(self._data["CollectionGroup"], list):
            self._data["CollectionGroup"] = []
        self._data["CollectionGroup"].append(group)
    
    def add_collection(self, collection: Optional['Collection'] = None,
                      **kwargs) -> None:
        """Add a collection to this group.
        
        Can be called two ways:
        1. With object: add_collection(collection=coll_obj)
        2. With parameters: add_collection(ID="C001", Name="Collection Name")
        """
        if collection is not None:
            coll = collection
        else:
            coll = Collection(kwargs)
        
        if not isinstance(self._data["Collection"], list):
            self._data["Collection"] = []
        self._data["Collection"].append(coll)
