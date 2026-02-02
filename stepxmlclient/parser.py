import xml.etree.ElementTree as ET
from typing import Any, Callable, List, Optional
from . import STEPXML_NS


def _str_to_bool(value: str) -> bool:
    """Convert XML boolean string ('true'/'false') to Python bool."""
    return value.lower() == 'true'


class Parser:
    
    def __init__(self):
        self._tree = None
        self._root: Optional[ET.Element] = None
        self.products: List[dict] = []
        self.assets: List[dict] = []
        self.classifications: List[dict] = []
        self.delete_products: List[dict] = []
        self.delete_assets: List[dict] = []
        return

    def parse_file(self, file_path: str):
        self._tree = ET.parse(file_path)
        return self.parse(self._tree.getroot())

    def parse_str(self, xml_str: str):
        return self.parse(ET.fromstring(xml_str))

    def parse(self, root: ET.Element):
        assert root.tag == 'STEP-ProductInformation'
        self._root = root
        self.assets = self._parse_item_list(
            'Assets', 'Asset', _parse_asset)
        self.products = self._parse_item_list(
            'Products', 'Product', _parse_product)
        self.classifications = self._parse_item_list(
            'Classifications', 'Classification', _parse_classification
        )
        self.delete_assets = self._parse_item_list(
            'DeleteAssets', 'DeleteAsset', _parse_delete_asset
        )
        self.delete_products = self._parse_item_list(
            'DeleteProducts', 'DeleteProduct', _parse_delete_product
        )
        return

    def _parse_item_list(self, 
                         list_name: str, 
                         item_name: str, 
                         parse_fct: Callable[[Any], Any]
                         ) -> List[Any]:
        results: List[Any] = []
        if self._root is None:
            return results
        item_list = self._root.find(list_name, STEPXML_NS)
        if item_list is not None:
            for item in item_list.findall(item_name, STEPXML_NS):
                result = parse_fct(item)
                if result is not None:
                   results.append(result)
        return results
    
    
def _parse_element(
        element, attributes = [], texts = [], 
        specials = {}, conversions={}):
    result = {}
    for attr_name in attributes:
        result[attr_name] = element.get(attr_name)
    # Apply conversions to attributes after parsing
    for attr_name in attributes:
        if attr_name in conversions:
            conv_fct, default = conversions[attr_name]
            if result[attr_name] is not None:
                result[attr_name] = conv_fct(result[attr_name])
            elif default is not None:
                result[attr_name] = default
    for child in element:
        key = child.tag
        if key in texts:
            result[key] = child.text
        elif key in specials:
            result[key] = specials[key](child)
        # Apply conversions to child elements
        if key in conversions:
            conv_fct, default = conversions[key]
            if result.get(key):
                result[key] = conv_fct(result[key])
            elif default is not None:
                result[key] = default
    return result

def _parse_leaf_element(element, name=None, attributes = []):
    result = {}
    for attr_name in attributes:
        result[attr_name] = element.get(attr_name)
    if name is None:
        name = element.tag
    result[name] = element.text
    return result
        
    
def _parse_asset(element):
    return _parse_element(
        element,
        attributes=("ID",),
        texts= ('Name', 'KeyValue'),
        specials= {"Values" : _parse_values}
    )
    
def _parse_delete_asset(element):
    return _parse_element(
        element,
        attributes=("ID",)
    )

def _parse_product(element):
    """Parse Product element with support for multiple cross-references.
    
    Handles:
    - Attributes: ID, ParentId, UserTypeID
    - Child: Name (text)
    - Child: Values (complex)
    - Children: Multiple AssetCrossReference, ProductCrossReference, etc.
    """
    result = _parse_element(
        element,
        attributes = ("ID", "ParentId", "UserTypeID"),
        texts = ("Name",),
        specials = {
            "Values": _parse_values,
        }
    )
    
    # Handle cross-references that can appear multiple times
    cross_ref_types = {
        "AssetCrossReference": _parse_asset_reference,
        "DeleteAssetCrossReference": _parse_asset_reference,
        "ProductCrossReference": _parse_product_cross_reference,
        "DeleteProductCrossReference": _parse_product_cross_reference,
        "ClassificationReference": _parse_classification_reference,
        "DeleteClassificationReference": _parse_classification_reference,
        "ClassificationCrossReference": _parse_classification_reference,
        "DeleteClassificationCrossReference": _parse_classification_reference,
        "EntityCrossReference": _parse_entity_cross_reference,
        "DeleteEntityCrossReference": _parse_entity_cross_reference,
    }
    
    # Process cross-references, aggregating multiples into lists
    for child in element:
        if child.tag in cross_ref_types:
            parser_func = cross_ref_types[child.tag]
            parsed = parser_func(child)
            
            if child.tag in result:
                # Multiple elements of same type - convert to list
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(parsed)
            else:
                # First element of this type
                result[child.tag] = parsed
    
    return result
    
def _parse_delete_product(element):
    return _parse_element(
        element,
        attributes=("ID",)
    )

def _parse_values(element):
    values = {}
    for child in element:
        attribute_id = child.get('AttributeID')
        if attribute_id is not None:
            if child.tag == "Value":
                values[attribute_id] = _parse_value(child)
            elif child.tag == "MultiValue":
                multi_value_list = []
                for sub_child in child.findall('Value'):
                    multi_value_list.append(_parse_value(sub_child))
                if multi_value_list:
                    values[attribute_id] = multi_value_list
    return values
                
def _parse_value(element):
    return _parse_leaf_element(
        element,
        name = "value",
        attributes = ("ID",))           
    
def _parse_asset_reference(element):
    """Parse AssetCrossReference or DeleteAssetCrossReference elements.
    
    Handles:
    - Attributes: AssetID, Type, Changed, QualifierID
    - Children: KeyValue (multiple), MetaData
    """
    result = _parse_element(
        element,
        attributes=("AssetID", "Changed", "Type", "QualifierID"),
        specials={"MetaData": _parse_metadata},
        conversions={"Changed": (_str_to_bool, False)}
    )
    
    # Parse KeyValue elements (can be multiple)
    key_values = []
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result


def _parse_product_cross_reference(element):
    """Parse ProductCrossReference or DeleteProductCrossReference elements.
    
    Handles:
    - Attributes: ProductID, Type, Changed, QualifierID, MountLocation
    - Children: KeyValue (multiple), MetaData
    """
    result = _parse_element(
        element,
        attributes=("ProductID", "Changed", "Type", "QualifierID", "MountLocation"),
        specials={"MetaData": _parse_metadata},
        conversions={"Changed": (_str_to_bool, False)}
    )
    
    # Parse KeyValue elements (can be multiple)
    key_values = []
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result


def _parse_classification_reference(element):
    """Parse ClassificationReference or DeleteClassificationReference elements.
    
    Handles:
    - Attributes: ClassificationID, Type, Changed, QualifierID
    - Children: KeyValue (multiple), MetaData
    """
    result = _parse_element(
        element,
        attributes=("ClassificationID", "Changed", "Type", "QualifierID"),
        specials={"MetaData": _parse_metadata},
        conversions={"Changed": (_str_to_bool, False)}
    )
    
    # Parse KeyValue elements (can be multiple)
    key_values = []
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result


def _parse_entity_cross_reference(element):
    """Parse EntityCrossReference or DeleteEntityCrossReference elements.
    
    Handles:
    - Attributes: EntityID, Type, Changed, QualifierID
    - Children: KeyValue (multiple), MetaData
    """
    result = _parse_element(
        element,
        attributes=("EntityID", "Changed", "Type", "QualifierID"),
        specials={"MetaData": _parse_metadata},
        conversions={"Changed": (_str_to_bool, False)}
    )
    
    # Parse KeyValue elements (can be multiple)
    key_values = []
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result


def _parse_key_value(element):
    """Parse KeyValue element used for alternate object identification.
    
    Returns dict with KeyID attribute and text value.
    """
    return {
        "KeyID": element.get("KeyID"),
        "value": element.text
    }


def _parse_metadata(element):
    """Parse MetaData element with nested Value/MultiValue/ValueGroup.
    
    Returns dict with attribute IDs as keys and values.
    """
    metadata = {}
    for child in element:
        attribute_id = child.get('AttributeID')
        if attribute_id is not None:
            if child.tag == "Value":
                metadata[attribute_id] = _parse_value(child)
            elif child.tag == "MultiValue":
                multi_value_list = []
                for sub_child in child.findall('Value', STEPXML_NS):
                    multi_value_list.append(_parse_value(sub_child))
                if multi_value_list:
                    metadata[attribute_id] = multi_value_list
    return metadata if metadata else None


def _parse_classification(element):
    """Parse Classification element with support for nested classifications and cross-references.
    
    Handles:
    - Attributes: ID, ParentID, UserTypeID, QualifierID, Changed, Republished, Selected, Referenced
    - Children: KeyValue (multiple), ParentKeyValue (multiple)
    - Children: Name (text), nested Classification (hierarchical)
    - Cross-references: ProductReference, ProductCrossReference (suppressed/delete variants)
    - Cross-references: ClassificationCrossReference (classification-to-classification)
    - Cross-references: EntityCrossReference
    - Cross-references: AssetCrossReference
    - Other: MetaData, AttributeLink, DataContainerTypeLink
    """
    result = _parse_element(
        element,
        attributes=("ID", "ParentID", "UserTypeID", "QualifierID", "Changed", "Republished", "Selected", "Referenced"),
        texts=("Name",),
        conversions={
            "Changed": (_str_to_bool, False),
            "Republished": (_str_to_bool, False),
            "Selected": (_str_to_bool, True),
            "Referenced": (_str_to_bool, False)
        }
    )
    
    # Parse KeyValue and ParentKeyValue elements (can be multiple)
    key_values = []
    parent_key_values = []
    nested_classifications = []
    
    # Define all cross-reference types supported by classifications
    cross_ref_types = {
        "ProductReference": _parse_product_cross_reference,
        "DeleteProductReference": _parse_product_cross_reference,
        "SuppressedProductReference": _parse_product_cross_reference,
        "DeleteSuppressedProductReference": _parse_product_cross_reference,
        "ProductCrossReference": _parse_product_cross_reference,
        "DeleteProductCrossReference": _parse_product_cross_reference,
        "SuppressedProductCrossReference": _parse_product_cross_reference,
        "DeleteSuppressedProductCrossReference": _parse_product_cross_reference,
        "ClassificationCrossReference": _parse_classification_reference,
        "DeleteClassificationCrossReference": _parse_classification_reference,
        "SuppressedClassificationCrossReference": _parse_classification_reference,
        "DeleteSuppressedClassificationCrossReference": _parse_classification_reference,
        "EntityCrossReference": _parse_entity_cross_reference,
        "DeleteEntityCrossReference": _parse_entity_cross_reference,
        "SuppressedEntityCrossReference": _parse_entity_cross_reference,
        "DeleteSuppressedEntityCrossReference": _parse_entity_cross_reference,
        "AssetCrossReference": _parse_asset_reference,
        "DeleteAssetCrossReference": _parse_asset_reference,
        "SuppressedAssetCrossReference": _parse_asset_reference,
        "DeleteSuppressedAssetCrossReference": _parse_asset_reference,
    }
    
    # Process child elements, handling special cases
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
        elif child.tag == "ParentKeyValue":
            parent_key_values.append(_parse_key_value(child))
        elif child.tag == "Classification":
            # Nested classifications (hierarchical)
            nested_classifications.append(_parse_classification(child))
        elif child.tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
        elif child.tag in cross_ref_types:
            # Cross-references - aggregate multiple into lists
            parser_func = cross_ref_types[child.tag]
            parsed = parser_func(child)
            
            if child.tag in result:
                # Multiple elements of same type - convert to list
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(parsed)
            else:
                # First element of this type
                result[child.tag] = parsed
    
    # Add aggregated lists to result if present
    if key_values:
        result["KeyValue"] = key_values
    if parent_key_values:
        result["ParentKeyValue"] = parent_key_values
    if nested_classifications:
        result["Classification"] = nested_classifications
    
    return result
    