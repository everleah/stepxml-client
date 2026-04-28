
"""
Base object model module for STEP XML Client.

This module provides the BaseObject class, which is the foundation for all STEP entity models
(Product, Asset, Attribute, Classification, etc.). BaseObject uses a declarative configuration
approach to define XML serialization behavior.

All STEP entity classes inherit from BaseObject and use class-level configuration attributes
to define how instances are serialized to XML elements. This approach enables automatic
serialization without requiring custom to_element() implementations in subclasses.

Configuration Attributes (set in subclasses):
    _GROUP_NAME: The collection name in Creator (e.g., 'products', 'assets')
    _TAG_NAME: The XML element tag name (e.g., 'Product', 'Asset')
    _ATTRIBUTE_NAMES: Tuple of attribute names to serialize as XML attributes
    _TEXT_NAMES: Tuple of simple text element names
    _VALUE_NAME: Name of the single text value for this element
    _CHILDREN_NAMES: Tuple of child element names to process recursively

Example:
    Defining a custom STEP entity model::
    
        from stepxmlclient.model import BaseObject
        
        class MyEntity(BaseObject):
            _GROUP_NAME = 'my_entities'
            _TAG_NAME = 'MyEntity'
            _ATTRIBUTE_NAMES = ('ID', 'Type')
            _TEXT_NAMES = ('Name', 'Description')
            _CHILDREN_NAMES = ('Values', 'Relations')
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union, Type

class BaseObject:
    """Base class for all STEP entity models.
    
    Provides declarative XML serialization for STEP entities. Subclasses define their
    structure through class-level configuration attributes that control how instances
    are converted to XML elements.
    
    The to_element() method handles the actual serialization by inspecting these
    configuration attributes and building the appropriate XML structure.
    
    Attributes:
        _GROUP_NAME: Collection name for this entity type in Creator
        _TAG_NAME: XML element tag name for this entity
        _ATTRIBUTE_NAMES: Tuple of attribute names to serialize as XML attributes
        _TEXT_NAMES: Tuple of child element names to render as text elements
        _VALUE_NAME: Name of the element value (for elements with single text content)
        _CHILDREN_NAMES: Tuple of child element names to process recursively
    """
    
    #: Collection name for grouping in Creator (override in subclasses)
    _GROUP_NAME: Optional[str] = None
    
    #: XML element tag name (override in subclasses)
    _TAG_NAME: Optional[str] = None
    
    #: Attribute names to serialize as XML attributes (override in subclasses)
    _ATTRIBUTE_NAMES: Optional[List[str]] = None
    
    #: Child element names to render as simple text elements (override in subclasses)
    _TEXT_NAMES: Optional[List[str]] = None
    
    #: Name of element value for single-value elements (override in subclasses)
    _VALUE_NAME: Optional[str] = None
    
    #: Child element names to process and add recursively (override in subclasses)
    _CHILDREN_NAMES: Optional[List[str]] = None

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize a BaseObject with data dictionary.
        
        Args:
            data: Dictionary containing the entity data.
                  Keys should match configuration attribute names defined in subclasses.
        """
        self._data: Dict[str, Any] = data
        return
    
    def to_element(self, parent: Optional[ET.Element] = None) -> ET.Element:
        """Serialize this object to an XML element.
        
        Converts the entity to an ElementTree element using the class-level configuration
        attributes. If parent is provided, adds this element as a child; otherwise creates
        a standalone element.
        
        The serialization process:
        1. Creates the element with _TAG_NAME and serializes _ATTRIBUTE_NAMES as attributes
        2. Sets element text if _VALUE_NAME is defined
        3. Adds simple text child elements from _TEXT_NAMES
        4. Recursively processes children from _CHILDREN_NAMES
        
        Args:
            parent: Optional parent ElementTree element. If provided, adds this element as a child.
                   If None, creates and returns a standalone element.
                   
        Returns:
            The created ElementTree element
        """
        if parent is None:
            element = ET.Element(
                tag=self._TAG_NAME if self._TAG_NAME else "",
                attrib=self._get_attributes()
            )
        else:
                element = ET.SubElement(
                    parent,
                    self._TAG_NAME if self._TAG_NAME else "",
                    self._get_attributes()
                )
        value = self._get_value()
        if value:
            element.text = value
        self._add_texts(element)
        self._add_children(element)
        return element
    
    def _get_value(self) -> Optional[str]:
        """Get the element's text value if configured.
        
        Returns the string value from the data dictionary using the _VALUE_NAME key.
        Used for elements that contain simple text content rather than child elements.
        
        Returns:
            String representation of the value, or None if not configured or not present
        """
        if self._VALUE_NAME:
            val = self._data.get(self._VALUE_NAME)
            if val is not None:
                return str(val)
        return None
    
    def _get_attributes(self) -> Dict[str, str]:
        """Collect XML attributes from configured attribute names.
        
        Extracts values from the data dictionary for all names specified in
        _ATTRIBUTE_NAMES and builds an attributes dictionary suitable for ElementTree.
        
        Returns:
            Dictionary mapping attribute names to string values
        """
        attributes: Dict[str, str] = {}
        if self._ATTRIBUTE_NAMES:
            for name in self._ATTRIBUTE_NAMES:                
                value = self._data.get(name)
                if value is not None:
                    attributes[name] = str(value)
        return attributes
    
    def _add_texts(self, element: ET.Element) -> None:
        """Add simple text child elements.
        
        Creates child elements for each name in _TEXT_NAMES and populates them with
        corresponding values from the data dictionary.
        
        Args:
            element: Parent ElementTree element to add text children to
        """
        if self._TEXT_NAMES:    
            for name in self._TEXT_NAMES:
                value = self._data.get(name)
                if value is not None:
                    child = ET.SubElement(element, name)
                    child.text = str(value)
        return
    
    def _add_children(self, element: ET.Element) -> None:
        """Add child elements recursively.
        
        Processes items from _CHILDREN_NAMES and handles different data types:
        - BaseObject instances: calls to_element() recursively
        - Dictionaries: passes to _add_dict_child() for special handling
        - Lists: processes each item in the list
        
        Args:
            element: Parent ElementTree element to add children to
        """
        if self._CHILDREN_NAMES:    
            for name in self._CHILDREN_NAMES:
                child = self._data.get(name)
                if child is not None:
                    # Handle different child data types
                    if hasattr(child, 'to_element'):
                        # BaseObject instance
                        child.to_element(element)
                    elif isinstance(child, dict):
                        # Dictionary data (like AssetCrossReference)
                        self._add_dict_child(element, name, child)
                    elif isinstance(child, list):
                        # List of items
                        for item in child:
                            if hasattr(item, 'to_element'):
                                item.to_element(element)
                            elif isinstance(item, dict):
                                self._add_dict_child(element, name, item)
                            elif item is not None:
                                # Primitive list item -> simple text child element
                                item_element = ET.SubElement(element, name)
                                item_element.text = str(item)
                    else:
                        # Primitive child value -> simple text child element
                        child_element = ET.SubElement(element, name)
                        child_element.text = str(child)
        return
    
    def _add_dict_child(self, parent: ET.Element, tag_name: str, data: Dict[str, Any]) -> ET.Element:
        """Add a child element from dictionary data.
        
        Processes dictionary data and creates appropriate XML elements. Handles special cases
        like the Values element with MultiValue/Value nesting structure commonly used in STEP.
        
        Args:
            parent: Parent ElementTree element
            tag_name: XML tag name for the child element
            data: Dictionary data to serialize
            
        Returns:
            The created child element
        """
        child_element = ET.SubElement(parent, tag_name)        # Handle special case for Values (nested structure)
        if tag_name == "Values" and isinstance(data, dict):
            for attribute_id, value_data in data.items():
                if isinstance(value_data, list):
                    # MultiValue
                    multi_value_elem = ET.SubElement(child_element, "MultiValue", AttributeID=attribute_id)
                    for item in value_data:
                        self._add_value_element(multi_value_elem, item)
                else:
                    # Single Value
                    self._add_value_element(child_element, value_data, attribute_id)
        elif tag_name in ("KeyValue", "ParentKeyValue"):
            # KeyValueType is mixed content with required attributes like KeyID.
            text_value = data.get("value", data.get("text"))
            for key, value in data.items():
                if key in ("value", "text"):
                    continue
                if value is not None:
                    child_element.set(key, str(value))
            if text_value is not None:
                child_element.text = str(text_value)
        else:
            # Simple dictionary - add all as attributes
            for key, value in data.items():
                if value is not None:
                    child_element.set(key, str(value))
        return child_element
    
    def _add_value_element(self, parent: ET.Element, value_data: Any, attribute_id: Optional[str] = None) -> Optional[ET.Element]:
        """Add a Value element from parsed value data"""
        value_elem: Optional[ET.Element] = None
        if isinstance(value_data, dict):
            attribs: Dict[str, str] = {}
            if attribute_id:
                attribs["AttributeID"] = attribute_id
            if "ID" in value_data:
                attribs["ID"] = str(value_data["ID"])

            value_elem = ET.SubElement(parent, "Value", attribs)
            if "value" in value_data:
                value_elem.text = str(value_data["value"])
        return value_elem


# Export model classes
from .product import Product, ProductReplacementRule
from .asset import Asset
from .classification import Classification
from .entity import Entity
from .attribute import Attribute, AttributeGroup, ListOfValues, ValueGroup, ListOfValuesGroup
from .organization import Context, Qualifier, Dimension, DimensionPoint
from .metadata import UserType, LinkType, Tag, TagGroup, Unit
from .business import BusinessRule, Workflow, Collection, CollectionGroup
from .deletion import DeleteAsset, DeleteProduct, DeleteAssetCrossReference, DeleteProductCrossReference, DeleteClassificationCrossReference, DeleteEntityCrossReference
from .replacement import ReplaceValues, ReplaceCrossReferences, ReplaceAttributeLinks, ReplaceClassificationReferences, ReplaceProducts, ReplaceClassifications, ReplaceEntities, ReplaceAssets, ReplaceAttributes
from .relations import AssetCrossReference, ProductCrossReference, ClassificationReference, ClassificationCrossReference, EntityCrossReference
from .complex_elements import STEPWorkflowStateBind, SequenceProduct, OverrideSubProduct, PackagingReference, AssetPushLocation, AssetContent, AssetContentSpecification, BinaryContent, AssetBinaryContent, Task, CurrentTasks, Term, Terms, Tables

def get_model_class(class_name: str) -> Optional[Type[BaseObject]]:
    """Get model class by its class name as string (case-insensitive).
    
    Args:
        class_name: The name of the model class (e.g., 'Product', 'Workflow', 'Collection')
        
    Returns:
        The model class type, or None if not found. All returned types are 
        subclasses of BaseObject.
        
    Example:
        >>> ProductClass = get_model_class('Product')
        >>> product = ProductClass({"ID": "P001", "Name": "Test"})
        >>> WorkflowClass = get_model_class('Workflow')
        >>> workflow = WorkflowClass({"ID": "WF001", "Name": "Approval"})
    """
    model_classes = {
        'product': Product,
        'productreplacementrule': ProductReplacementRule,
        'asset': Asset,
        'classification': Classification,
        'entity': Entity,
        'attribute': Attribute,
        'attributegroup': AttributeGroup,
        'listofvalues': ListOfValues,
        'valuegroup': ValueGroup,
        'listofvaluesgroup': ListOfValuesGroup,
        'context': Context,
        'qualifier': Qualifier,
        'dimension': Dimension,
        'dimensionpoint': DimensionPoint,
        'usertype': UserType,
        'linktype': LinkType,
        'tag': Tag,
        'taggroup': TagGroup,
        'unit': Unit,
        'businessrule': BusinessRule,
        'workflow': Workflow,
        'collection': Collection,
        'collectiongroup': CollectionGroup,
        'deleteasset': DeleteAsset,
        'deleteproduct': DeleteProduct,
        'deleteassetcrossreference': DeleteAssetCrossReference,
        'deleteproductcrossreference': DeleteProductCrossReference,
        'deleteclassificationcrossreference': DeleteClassificationCrossReference,
        'deleteentitycrossreference': DeleteEntityCrossReference,
        'assetcrossreference': AssetCrossReference,
        'productcrossreference': ProductCrossReference,
        'classificationreference': ClassificationReference,
        'classificationcrossreference': ClassificationCrossReference,
        'entitycrossreference': EntityCrossReference,
        'stepworkflowstatebind': STEPWorkflowStateBind,
        'sequenceproduct': SequenceProduct,
        'overridesubproduct': OverrideSubProduct,
        'packagingreference': PackagingReference,
        'assetpushlocation': AssetPushLocation,
        'assetcontent': AssetContent,
        'assetcontentspecification': AssetContentSpecification,
        'binarycontent': BinaryContent,
        'assetbinarycontent': AssetBinaryContent,
        'task': Task,
        'currenttasks': CurrentTasks,
        'term': Term,
        'terms': Terms,
        'tables': Tables,
        'replacevalues': ReplaceValues,
        'replacecrossreferences': ReplaceCrossReferences,
        'replaceattributelinks': ReplaceAttributeLinks,
        'replaceclassificationreferences': ReplaceClassificationReferences,
        'replaceproducts': ReplaceProducts,
        'replaceclassifications': ReplaceClassifications,
        'replaceentities': ReplaceEntities,
        'replaceassets': ReplaceAssets,
        'replaceattributes': ReplaceAttributes,
    }
    return model_classes.get(class_name.lower(), None)

__all__ = [
    'get_model_class',
    'BaseObject',
    'Product',
    'ProductReplacementRule',
    'Asset',
    'Classification',
    'Entity',
    'Attribute',
    'AttributeGroup',
    'ListOfValues',
    'ValueGroup',
    'ListOfValuesGroup',
    'Context',
    'Qualifier',
    'Dimension',
    'DimensionPoint',
    'UserType',
    'LinkType',
    'Tag',
    'TagGroup',
    'Unit',
    'BusinessRule',
    'Workflow',
    'Collection',
    'CollectionGroup',
    'DeleteAsset',
    'DeleteProduct',
    'DeleteAssetCrossReference',
    'DeleteProductCrossReference',
    'DeleteClassificationCrossReference',
    'DeleteEntityCrossReference',
    'AssetCrossReference',
    'ProductCrossReference',
    'ClassificationCrossReference',
    'EntityCrossReference',
    'STEPWorkflowStateBind',
    'SequenceProduct',
    'OverrideSubProduct',
    'PackagingReference',
    'AssetPushLocation',
    'AssetContent',
    'AssetContentSpecification',
    'BinaryContent',
    'AssetBinaryContent',
    'Task',
    'CurrentTasks',
    'Term',
    'Terms',
    'Tables',
    'ReplaceValues',
    'ReplaceCrossReferences',
    'ReplaceAttributeLinks',
    'ReplaceClassificationReferences',
    'ReplaceProducts',
    'ReplaceClassifications',
    'ReplaceEntities',
    'ReplaceAssets',
    'ReplaceAttributes',
]
