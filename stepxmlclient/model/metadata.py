"""Metadata and configuration models for STEP XML Client.

Defines metadata and configuration classes for STEP MDM systems including user types,
contexts, qualifiers, dimensions, tags, units, and other configuration elements.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    pass


class UserType(BaseObject):
    """User type - object type definition in STEP MDM.
    
    User types define customizable object classifications with attributes, validation rules,
    icons, and category information. User types control the structure and behavior of
    products, assets, classifications, and entities.
    
    Supports:
    - Multiple names (multi-language)
    - Custom icons and templates
    - Attribute and dimension associations
    - Validation rules
    - Category classification
    - Revisability and link policies
    - Boolean state tracking (Selected, Referenced, Changed, Deleted)
    
    Attributes:
        ID: Unique user type identifier
        AllowOverlappingTerms: Whether overlapping terms are allowed
        AllowQuarkTemplate: Support for Quark templates
        AllowInDesignTemplate: Support for InDesign templates
        Revisability: Revision tracking policy
        IsCategory: Whether this type represents a category
        DefaultProfileConfiguration: Default profile configuration
        ClassificationOwnsProductLinks: Classification ownership semantics
        NamePattern: Pattern for naming instances
        IDPattern: Pattern for ID generation
        ManuallySorted: Whether instances are manually sorted
        ReferenceTargetLockPolicy: Link policy
        Name: User type name (localized)
        Icon: Icon representation
        VisibleTermFields: Visible fields for search
        MetaData: Metadata
        DimensionLink: Dimension associations
        UserTypeLink: Links to other user types
        AttributeLink: Attribute associations
        Validation: Validation rules
        MIMEType: Associated MIME types
    """
    _GROUP_NAME: str = 'usertypes'
    _TAG_NAME: str = 'UserType'
    _ATTRIBUTE_NAMES: List[str] = [
        "ID", "AllowOverlappingTerms", "AllowQuarkTemplate",
        "AllowInDesignTemplate", "Revisability", "IsCategory",
        "DefaultProfileConfiguration", "ClassificationOwnsProductLinks",
        "NamePattern", "IDPattern", "ManuallySorted",
        "ReferenceTargetLockPolicy", "Selected", "Referenced",
        "Changed", "Deleted"
    ]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "Icon",
        "VisibleTermFields",
        "MetaData",
        "DimensionLink",
        "UserTypeLink",
        "AttributeLink",
        "Validation",
        "MIMEType"
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize link lists if not provided
        for link_name in ["DimensionLink", "UserTypeLink", "AttributeLink", "MIMEType"]:
            if link_name not in self._data:
                self._data[link_name] = []


class LinkType(BaseObject):
    """LinkType - defines the type of cross-reference between objects.
    
    Link types specify valid relationship types (e.g., CA=Classification-to-Attribute,
    PA=Product-to-Attribute) for organizing cross-references.
    
    Simple metadata element with minimal structure.
    """
    _GROUP_NAME: str = 'linktypes'
    _TAG_NAME: str = 'LinkType'
    _ATTRIBUTE_NAMES: List[str] = ["LinkTypeID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)


class Tag(BaseObject):
    """Tag - flexible categorization element independent of hierarchies.
    
    Tags enable custom classification and filtering of objects
    outside the standard product/classification hierarchies.
    
    Supports:
    - Multi-language names
    - Metadata tracking
    """
    _GROUP_NAME: str = 'tags'
    _TAG_NAME: str = 'Tag'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["MetaData"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)


class TagGroup(BaseObject):
    """TagGroup - hierarchical grouping of tags.
    
    Organizes tags into logical collections with parent/child relationships.
    
    Supports:
    - Nested tag groups (hierarchies)
    - Multi-language names
    - Tag collection
    - Metadata tracking
    """
    _GROUP_NAME: str = 'taggroups'
    _TAG_NAME: str = 'TagGroup'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["MetaData", "TagGroup", "Tag"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize nested tag groups and tags lists
        if "TagGroup" not in self._data:
            self._data["TagGroup"] = []
        if "Tag" not in self._data:
            self._data["Tag"] = []
    
    def add_nested_tag_group(self, tag_group: Optional['TagGroup'] = None,
                            **kwargs) -> None:
        """Add nested tag group.
        
        Can be called two ways:
        1. With object: add_nested_tag_group(tag_group=group_obj)
        2. With parameters: add_nested_tag_group(ID="TG002", Name="Nested Group")
        """
        if tag_group is not None:
            group = tag_group
        else:
            group = TagGroup(kwargs)
        
        if not isinstance(self._data["TagGroup"], list):
            self._data["TagGroup"] = []
        self._data["TagGroup"].append(group)
    
    def add_tag(self, tag: Optional['Tag'] = None,
               **kwargs) -> None:
        """Add a tag to this group.
        
        Can be called two ways:
        1. With object: add_tag(tag=tag_obj)
        2. With parameters: add_tag(ID="T001", Name="Tag Name")
        """
        if tag is not None:
            t = tag
        else:
            t = Tag(kwargs)
        
        if not isinstance(self._data["Tag"], list):
            self._data["Tag"] = []
        self._data["Tag"].append(t)


class Unit(BaseObject):
    """Unit - defines a measurement unit for quantitative attributes.
    
    Units represent measurement standards (meters, kilograms, liters, etc.)
    used for quantitative attribute values.
    
    Supports:
    - Unit symbol (m, kg, l, etc.)
    - Conversion formula to base unit
    - Metadata tracking
    """
    _GROUP_NAME: str = 'units'
    _TAG_NAME: str = 'Unit'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "Name", "Symbol", "Formula"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["MetaData"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
