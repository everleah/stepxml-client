
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union, Type

class BaseObject:
    _GROUP_NAME: Optional[str] = None
    _TAG_NAME: Optional[str] = None
    _ATTRIBUTE_NAMES: Optional[List[str]] = None
    _TEXT_NAMES: Optional[List[str]] = None
    _VALUE_NAME: Optional[str] = None
    _CHILDREN_NAMES: Optional[List[str]] = None

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data: Dict[str, Any] = data
        return
    
    def to_element(self, parent: Optional[ET.Element] = None) -> ET.Element:
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
        if self._VALUE_NAME:
            val = self._data.get(self._VALUE_NAME)
            if val is not None:
                return str(val)
        return None
    
    def _get_attributes(self) -> Dict[str, str]:
        attributes: Dict[str, str] = {}
        if self._ATTRIBUTE_NAMES:
            for name in self._ATTRIBUTE_NAMES:
                value = self._data.get(name)
                if value is not None:
                    attributes[name] = str(value)
        return attributes
    
    def _add_texts(self, element: ET.Element) -> None:
        if self._TEXT_NAMES:
            for name in self._TEXT_NAMES:
                value = self._data.get(name)
                if value is not None:
                    child = ET.SubElement(element, name)
                    child.text = str(value)
        return
    
    def _add_children(self, element: ET.Element) -> None:
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
        return
    
    def _add_dict_child(self, parent: ET.Element, tag_name: str, data: Dict[str, Any]) -> ET.Element:
        """Add a child element from dictionary data"""
        child_element = ET.SubElement(parent, tag_name)

        # Handle special case for Values (nested structure)
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
from .deletion import DeleteAsset, DeleteProduct, DeleteAssetCrossReference, DeleteProductCrossReference
from .relations import AssetCrossReference, ProductCrossReference, ClassificationCrossReference, EntityCrossReference

def get_model_class(class_name: str) -> Optional[Type[BaseObject]]:
    """Get model class by its class name as string (case-insensitive).
    
    Args:
        class_name: The name of the model class (e.g., 'Product', 'Asset')
        
    Returns:
        The model class type, or None if not found. All returned types are 
        subclasses of BaseObject.
        
    Example:
        >>> ProductClass = get_model_class('Product')
        >>> product = ProductClass({"ID": "P001", "Name": "Test"})
    """
    model_classes = {
        'product': Product,
        'productreplacementrule': ProductReplacementRule,
        'asset': Asset,
        'deleteasset': DeleteAsset,
        'deleteproduct': DeleteProduct,
        'deleteassetcrossreference': DeleteAssetCrossReference,
        'deleteproductcrossreference': DeleteProductCrossReference,
        'assetcrossreference': AssetCrossReference,
        'productcrossreference': ProductCrossReference,
        'classificationcrossreference': ClassificationCrossReference,
        'entitycrossreference': EntityCrossReference,
    }
    return model_classes.get(class_name.lower(), None)

__all__ = [
    'get_model_class',
    'BaseObject',
    'Product',
    'ProductReplacementRule',
    'Asset',
    'DeleteAsset',
    'DeleteProduct',
    'DeleteAssetCrossReference',
    'DeleteProductCrossReference',
    'AssetCrossReference',
    'ProductCrossReference',
    'ClassificationCrossReference',
    'EntityCrossReference',
]
