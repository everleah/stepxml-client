import xml.etree.ElementTree as ET
from typing import Any, Callable, List, Optional
from . import STEPXML_NS

class Parser:
    
    def __init__(self):
        self._tree = None
        self._root: Optional[ET.Element] = None
        self.products: List[dict] = []
        self.assets: List[dict] = []
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
    return _parse_element(
        element,
        attributes = ("ID", "ParentId", "UserTypeID"),
        texts = ("Name",),
        specials = {
            "Values" : _parse_values,
            "AssetCrossReference": _parse_asset_reference,
            "DeleteAssetCrossReference": _parse_asset_reference
            }
    )
    
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
    return _parse_element(
        element,
        attributes=("AssetID", "Changed", "Type"),
        conversions= {
            "Changed" : (bool, False)
        }
    )

    
    
    
    