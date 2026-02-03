"""Phase 7: Replacement Rules for bulk update operations.

Handles ReplaceValues, ReplaceCrossReferences, ReplaceAttributeLinks,
ReplaceClassificationReferences and their container classes for Products,
Classifications, Entities, and Assets.
"""

from typing import List, Optional, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    pass


class ReplaceValues(BaseObject):
    """Replacement instruction for attribute values.
    
    Child-only element used within ReplaceProducts, ReplaceClassifications,
    ReplaceAssets, ReplaceEntities containers.
    
    Attributes:
        AttributeID: Reference to attribute being replaced
        AttributeGroupID: Optional reference to attribute group
        ContextID: Optional context for the replacement
    """
    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = 'ReplaceValues'
    _ATTRIBUTE_NAMES: List[str] = ["AttributeID", "AttributeGroupID", "ContextID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []

    def __init__(self, attribute_id: Optional[str] = None,
                 attribute_group_id: Optional[str] = None,
                 context_id: Optional[str] = None):
        super().__init__()
        self.AttributeID = attribute_id
        self.AttributeGroupID = attribute_group_id
        self.ContextID = context_id


class ReplaceCrossReferences(BaseObject):
    """Replacement instruction for cross-references.
    
    Child-only element used within ReplaceProducts, ReplaceClassifications,
    ReplaceAssets, ReplaceEntities containers.
    
    Attributes:
        CrossReferenceID: Reference to the cross-reference being replaced
        ContextID: Optional context for the replacement
        MountLocation: Optional mount point location
    """
    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = 'ReplaceCrossReferences'
    _ATTRIBUTE_NAMES: List[str] = ["CrossReferenceID", "ContextID", "MountLocation"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []

    def __init__(self, cross_reference_id: Optional[str] = None,
                 context_id: Optional[str] = None,
                 mount_location: Optional[str] = None):
        super().__init__()
        self.CrossReferenceID = cross_reference_id
        self.ContextID = context_id
        self.MountLocation = mount_location


class ReplaceAttributeLinks(BaseObject):
    """Replacement instruction for attribute links.
    
    Child-only element used within ReplaceProducts, ReplaceClassifications
    containers.
    
    Attributes:
        AttributeID: Reference to the attribute link being replaced
    """
    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = 'ReplaceAttributeLinks'
    _ATTRIBUTE_NAMES: List[str] = ["AttributeID"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []

    def __init__(self, attribute_id: Optional[str] = None):
        super().__init__()
        self.AttributeID = attribute_id


class ReplaceClassificationReferences(BaseObject):
    """Replacement instruction for classification references.
    
    Child-only element used within ReplaceProducts, ReplaceClassifications
    containers.
    """
    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: str = 'ReplaceClassificationReferences'
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []

    def __init__(self):
        super().__init__()


class ReplaceProducts(BaseObject):
    """Container for replacement rules for a product.
    
    Used within ReplacementRules section. Supports four types of
    replacements: ReplaceValues, ReplaceCrossReferences, ReplaceAttributeLinks,
    ReplaceClassificationReferences.
    
    Convenience Methods:
        add_replace_values(attribute_id, attribute_group_id, context_id)
        add_replace_cross_references(cross_reference_id, context_id, mount_location)
        add_replace_attribute_links(attribute_id)
        add_replace_classification_references()
    """
    _GROUP_NAME: Optional[str] = None  # Child-only within ReplacementRules
    _TAG_NAME: str = 'Products'
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["ReplaceValues", "ReplaceCrossReferences",
                                   "ReplaceAttributeLinks", "ReplaceClassificationReferences"]

    def __init__(self):
        super().__init__()
        self.ReplaceValues: List[BaseObject] = []
        self.ReplaceCrossReferences: List[BaseObject] = []
        self.ReplaceAttributeLinks: List[BaseObject] = []
        self.ReplaceClassificationReferences: List[BaseObject] = []

    def add_replace_values(self, attribute_id: Optional[str] = None,
                          attribute_group_id: Optional[str] = None,
                          context_id: Optional[str] = None) -> ReplaceValues:
        """Add ReplaceValues instruction using parameters.
        
        Args:
            attribute_id: Reference to attribute being replaced
            attribute_group_id: Optional reference to attribute group
            context_id: Optional context for the replacement
            
        Returns:
            ReplaceValues: Created instruction object
        """
        rv = ReplaceValues(attribute_id, attribute_group_id, context_id)
        self.ReplaceValues.append(rv)
        return rv

    def add_replace_values_obj(self, replace_values: ReplaceValues) -> ReplaceValues:
        """Add ReplaceValues instruction using object.
        
        Args:
            replace_values: ReplaceValues object to add
            
        Returns:
            ReplaceValues: Added instruction object
        """
        self.ReplaceValues.append(replace_values)
        return replace_values

    def add_replace_cross_references(self, cross_reference_id: Optional[str] = None,
                                    context_id: Optional[str] = None,
                                    mount_location: Optional[str] = None) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using parameters.
        
        Args:
            cross_reference_id: Reference to the cross-reference being replaced
            context_id: Optional context for the replacement
            mount_location: Optional mount point location
            
        Returns:
            ReplaceCrossReferences: Created instruction object
        """
        rcr = ReplaceCrossReferences(cross_reference_id, context_id, mount_location)
        self.ReplaceCrossReferences.append(rcr)
        return rcr

    def add_replace_cross_references_obj(self, replace_cross_ref: ReplaceCrossReferences) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using object.
        
        Args:
            replace_cross_ref: ReplaceCrossReferences object to add
            
        Returns:
            ReplaceCrossReferences: Added instruction object
        """
        self.ReplaceCrossReferences.append(replace_cross_ref)
        return replace_cross_ref

    def add_replace_attribute_links(self, attribute_id: Optional[str] = None) -> ReplaceAttributeLinks:
        """Add ReplaceAttributeLinks instruction using parameters.
        
        Args:
            attribute_id: Reference to the attribute link being replaced
            
        Returns:
            ReplaceAttributeLinks: Created instruction object
        """
        ral = ReplaceAttributeLinks(attribute_id)
        self.ReplaceAttributeLinks.append(ral)
        return ral

    def add_replace_attribute_links_obj(self, replace_attr_links: ReplaceAttributeLinks) -> ReplaceAttributeLinks:
        """Add ReplaceAttributeLinks instruction using object.
        
        Args:
            replace_attr_links: ReplaceAttributeLinks object to add
            
        Returns:
            ReplaceAttributeLinks: Added instruction object
        """
        self.ReplaceAttributeLinks.append(replace_attr_links)
        return replace_attr_links

    def add_replace_classification_references(self) -> ReplaceClassificationReferences:
        """Add ReplaceClassificationReferences instruction.
        
        Returns:
            ReplaceClassificationReferences: Created instruction object
        """
        rcr = ReplaceClassificationReferences()
        self.ReplaceClassificationReferences.append(rcr)
        return rcr

    def add_replace_classification_references_obj(self, replace_class_refs: ReplaceClassificationReferences) -> ReplaceClassificationReferences:
        """Add ReplaceClassificationReferences instruction using object.
        
        Args:
            replace_class_refs: ReplaceClassificationReferences object to add
            
        Returns:
            ReplaceClassificationReferences: Added instruction object
        """
        self.ReplaceClassificationReferences.append(replace_class_refs)
        return replace_class_refs


class ReplaceClassifications(BaseObject):
    """Container for replacement rules for classifications.
    
    Supports ReplaceValues, ReplaceCrossReferences, and ReplaceAttributeLinks.
    Similar to ReplaceProducts but without ReplaceClassificationReferences.
    
    Convenience Methods:
        add_replace_values(attribute_id, attribute_group_id, context_id)
        add_replace_cross_references(cross_reference_id, context_id, mount_location)
        add_replace_attribute_links(attribute_id)
    """
    _GROUP_NAME: Optional[str] = None  # Child-only within ReplacementRules
    _TAG_NAME: str = 'Classifications'
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["ReplaceValues", "ReplaceCrossReferences",
                                   "ReplaceAttributeLinks"]

    def __init__(self):
        super().__init__()
        self.ReplaceValues: List[BaseObject] = []
        self.ReplaceCrossReferences: List[BaseObject] = []
        self.ReplaceAttributeLinks: List[BaseObject] = []

    def add_replace_values(self, attribute_id: Optional[str] = None,
                          attribute_group_id: Optional[str] = None,
                          context_id: Optional[str] = None) -> ReplaceValues:
        """Add ReplaceValues instruction using parameters."""
        rv = ReplaceValues(attribute_id, attribute_group_id, context_id)
        self.ReplaceValues.append(rv)
        return rv

    def add_replace_values_obj(self, replace_values: ReplaceValues) -> ReplaceValues:
        """Add ReplaceValues instruction using object."""
        self.ReplaceValues.append(replace_values)
        return replace_values

    def add_replace_cross_references(self, cross_reference_id: Optional[str] = None,
                                    context_id: Optional[str] = None,
                                    mount_location: Optional[str] = None) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using parameters."""
        rcr = ReplaceCrossReferences(cross_reference_id, context_id, mount_location)
        self.ReplaceCrossReferences.append(rcr)
        return rcr

    def add_replace_cross_references_obj(self, replace_cross_ref: ReplaceCrossReferences) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using object."""
        self.ReplaceCrossReferences.append(replace_cross_ref)
        return replace_cross_ref

    def add_replace_attribute_links(self, attribute_id: Optional[str] = None) -> ReplaceAttributeLinks:
        """Add ReplaceAttributeLinks instruction using parameters."""
        ral = ReplaceAttributeLinks(attribute_id)
        self.ReplaceAttributeLinks.append(ral)
        return ral

    def add_replace_attribute_links_obj(self, replace_attr_links: ReplaceAttributeLinks) -> ReplaceAttributeLinks:
        """Add ReplaceAttributeLinks instruction using object."""
        self.ReplaceAttributeLinks.append(replace_attr_links)
        return replace_attr_links


class ReplaceEntities(BaseObject):
    """Container for replacement rules for entities.
    
    Supports ReplaceValues and ReplaceCrossReferences (no attribute links or
    classification references for entities).
    
    Convenience Methods:
        add_replace_values(attribute_id, attribute_group_id, context_id)
        add_replace_cross_references(cross_reference_id, context_id, mount_location)
    """
    _GROUP_NAME: Optional[str] = None  # Child-only within ReplacementRules
    _TAG_NAME: str = 'Entities'
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["ReplaceValues", "ReplaceCrossReferences"]

    def __init__(self):
        super().__init__()
        self.ReplaceValues: List[BaseObject] = []
        self.ReplaceCrossReferences: List[BaseObject] = []

    def add_replace_values(self, attribute_id: Optional[str] = None,
                          attribute_group_id: Optional[str] = None,
                          context_id: Optional[str] = None) -> ReplaceValues:
        """Add ReplaceValues instruction using parameters."""
        rv = ReplaceValues(attribute_id, attribute_group_id, context_id)
        self.ReplaceValues.append(rv)
        return rv

    def add_replace_values_obj(self, replace_values: ReplaceValues) -> ReplaceValues:
        """Add ReplaceValues instruction using object."""
        self.ReplaceValues.append(replace_values)
        return replace_values

    def add_replace_cross_references(self, cross_reference_id: Optional[str] = None,
                                    context_id: Optional[str] = None,
                                    mount_location: Optional[str] = None) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using parameters."""
        rcr = ReplaceCrossReferences(cross_reference_id, context_id, mount_location)
        self.ReplaceCrossReferences.append(rcr)
        return rcr

    def add_replace_cross_references_obj(self, replace_cross_ref: ReplaceCrossReferences) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using object."""
        self.ReplaceCrossReferences.append(replace_cross_ref)
        return replace_cross_ref


class ReplaceAssets(BaseObject):
    """Container for replacement rules for assets.
    
    Supports ReplaceValues and ReplaceCrossReferences (no attribute links or
    classification references for assets).
    
    Convenience Methods:
        add_replace_values(attribute_id, attribute_group_id, context_id)
        add_replace_cross_references(cross_reference_id, context_id, mount_location)
    """
    _GROUP_NAME: Optional[str] = None  # Child-only within ReplacementRules
    _TAG_NAME: str = 'Assets'
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["ReplaceValues", "ReplaceCrossReferences"]

    def __init__(self):
        super().__init__()
        self.ReplaceValues: List[BaseObject] = []
        self.ReplaceCrossReferences: List[BaseObject] = []

    def add_replace_values(self, attribute_id: Optional[str] = None,
                          attribute_group_id: Optional[str] = None,
                          context_id: Optional[str] = None) -> ReplaceValues:
        """Add ReplaceValues instruction using parameters."""
        rv = ReplaceValues(attribute_id, attribute_group_id, context_id)
        self.ReplaceValues.append(rv)
        return rv

    def add_replace_values_obj(self, replace_values: ReplaceValues) -> ReplaceValues:
        """Add ReplaceValues instruction using object."""
        self.ReplaceValues.append(replace_values)
        return replace_values

    def add_replace_cross_references(self, cross_reference_id: Optional[str] = None,
                                    context_id: Optional[str] = None,
                                    mount_location: Optional[str] = None) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using parameters."""
        rcr = ReplaceCrossReferences(cross_reference_id, context_id, mount_location)
        self.ReplaceCrossReferences.append(rcr)
        return rcr

    def add_replace_cross_references_obj(self, replace_cross_ref: ReplaceCrossReferences) -> ReplaceCrossReferences:
        """Add ReplaceCrossReferences instruction using object."""
        self.ReplaceCrossReferences.append(replace_cross_ref)
        return replace_cross_ref


class ReplaceAttributes(BaseObject):
    """Container for replacement rules for attributes (empty container).
    
    Currently a simple container with no child elements defined in the schema.
    Provides expansion point for future attribute-specific replacements.
    """
    _GROUP_NAME: Optional[str] = None  # Child-only within ReplacementRules
    _TAG_NAME: str = 'Attributes'
    _ATTRIBUTE_NAMES: List[str] = []
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = []

    def __init__(self):
        super().__init__()
