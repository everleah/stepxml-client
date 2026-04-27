"""Cross-reference models for STEP XML Client.

Defines relationship/cross-reference classes for linking STEP entities together.
These are used to create various types of associations between products, assets,
classifications, and entities in the MDM system.
"""

from typing import List, Optional
from . import BaseObject

class AssetCrossReference(BaseObject):
    """Link between a product and an asset.
    
    Represents a relationship from a product (or asset) to an asset file.
    Includes optional type and qualifier information for classification of the link.
    
    Attributes:
        AssetID: ID of the asset being linked
        Type: Optional link type (e.g., 'Image', 'Document')
        QualifierID: Optional qualifier for context/language specificity
        KeyValue: Optional key value reference
        MetaData: Optional metadata for the relationship
    """
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'AssetCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["AssetID", "Type", "QualifierID", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class ProductCrossReference(BaseObject):
    """Link between two products.
    
    Represents a relationship from one product to another (parent, related, component, etc.).
    Includes optional type, qualifier, and mount location information.
    
    Attributes:
        ProductID: ID of the linked product
        Type: Optional link type (e.g., 'Parent', 'Related', 'Component')
        QualifierID: Optional qualifier for context/language specificity
        MountLocation: Optional location where product is mounted/used
        KeyValue: Optional key value reference
        MetaData: Optional metadata for the relationship
    """
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ProductCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["ProductID", "Type", "QualifierID", "MountLocation", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class ClassificationCrossReference(BaseObject):
    """Link between a product/classification and another classification.
    
    Represents a relationship from a product or classification to a classification.
    Used to associate products or classifications with categories in the taxonomy.
    
    Attributes:
        ClassificationID: ID of the classification being linked
        Type: Optional link type for classification relationships
        QualifierID: Optional qualifier for context/language specificity
        MountLocation: Optional location/context for the classification
        KeyValue: Optional key value reference
        MetaData: Optional metadata for the relationship
    """
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ClassificationCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["ClassificationID", "Type", "QualifierID", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class ClassificationReference(BaseObject):
    """Reference from an asset/product to a classification.

    This relation uses the ``ClassificationReference`` tag (not
    ``ClassificationCrossReference``) and is required for asset-to-classification
    links according to STEP.xsd ``AssetType``.
    """
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'ClassificationReference'
    _ATTRIBUTE_NAMES: List[str] = ["ClassificationID", "Type", "QualifierID", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]


class EntityCrossReference(BaseObject):
    """Link between a product/entity and another entity.
    
    Represents a relationship from a product or entity to an entity.
    Entities can have various types of links to other entities for flexible data modeling.
    
    Attributes:
        EntityID: ID of the entity being linked
        Type: Optional link type for entity relationships
        QualifierID: Optional qualifier for context/language specificity
        MountLocation: Optional location/context for the entity link
        KeyValue: Optional key value reference
        MetaData: Optional metadata for the relationship
    """
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'EntityCrossReference'
    _ATTRIBUTE_NAMES: List[str] = ["EntityID", "Type", "QualifierID", "Changed"]
    _TEXT_NAMES: List[str] = []
    _CHILDREN_NAMES: List[str] = ["KeyValue", "MetaData"]
