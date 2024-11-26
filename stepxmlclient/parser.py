import xml.etree.ElementTree as ET

STEPXML_NS = {
    'step' : 'http://www.stibosystems.com/step',
    'outputtemplate' : 'http://www.stibosystems.com/step/outputtemplate'
}

class Parser:
    
    def __init__(self):
        self._tree = None
        self._root = None
        self.products = None
        self.assets = None
        self.delete_products = None
        self.delete_assets = None
        return

    def parse_file(self, file_path):
        self._tree = ET.parse(file_path)
        return self.parse(self._tree.getroot())

    def parse_str(self, xml_str):
        return self.parse(ET.fromstring(xml_str))

    def parse(self, root):
        assert root.tag == 'STEP-ProductInformation'
        self._root = root
        self.assets = self._parse_item_list('Assets', 'Asset', _parse_asset)
        return
    
    def _parse_item_list(self, list_name, item_name, parse_fct):
        results = []
        item_list = self._root.find(list_name, STEPXML_NS)
        if item_list is not None:
            for item in item_list.findall(item_name, STEPXML_NS):
                result = parse_fct(item)
                if result is not None:
                   results.append(result)
        return result
    
    
def _parse_asset(element):
    asset = {}
    for child in element:
        key = child.tag
        if key in ('Name', 'KeyValue'):
            asset[key] = child.text
        elif key == "Values":
            asset[key] = _parse_values(child)
    return asset

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
    value = {'value' : element.text}
    lov_id = element.get("ID")
    if lov_id is not None:
        value['ID'] = lov_id
    return          
        
    
    
    
    