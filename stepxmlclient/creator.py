
import xml.etree.ElementTree as ET
from typing import List, Optional
from . import STEPXML_NS
from .model import BaseObject

class Creator:
    def __init__(
            self,
            context_id: str,
            workspace_id: str = 'Main') -> None:
        self.context_id: str = context_id
        self.workspace_id: str = workspace_id
        self.root: Optional[ET.Element] = None
        self.tree: Optional[ET.ElementTree] = None
        self.products: List[BaseObject] = []
        self.assets: List[BaseObject] = []
        self.classifications: List[BaseObject] = []
        self.entities: List[BaseObject] = []
        self.deletedproducts: List[BaseObject] = []
        self.deletedassets: List[BaseObject] = []
        self.product_replacement_rules: List[BaseObject] = []
        return
    
    def build(self) -> None:
        self.root = ET.Element(
            'STEP-ProductInformation',
            {
                "ContextID": self.context_id,
                "WorkspaceID": self.workspace_id
            }
        )
        self.tree = ET.ElementTree(self.root)
        # product replacement rules
        if self.product_replacement_rules:
            rules = ET.SubElement(self.root, 'ReplacementRules')
            self._build_element_list(
                rules, "Products", self.product_replacement_rules)
        # others - map XML element names to attribute names
        element_mapping = {
            "Assets": "assets",
            "Products": "products",
            "Classifications": "classifications",
            "Entities": "entities",
            "DeletedAssets": "deletedassets",
            "DeletedProducts": "deletedproducts"
        }
        for xml_name, attr_name in element_mapping.items():
            values = getattr(self, attr_name)
            if values:
                self._build_element_list(self.root, xml_name, values)
        return
        
    def _build_element_list(self, parent: ET.Element,
                            list_name: str,
                            objs: List[BaseObject]) -> None:
        list_element = ET.SubElement(parent, list_name)
        for obj in objs:
            obj.to_element(list_element)
        return
            
        
    def add(self, obj: BaseObject) -> bool:
        if obj._GROUP_NAME is None:
            return False
        list_attr = getattr(self, obj._GROUP_NAME)
        if isinstance(list_attr, list):
            list_attr.append(obj)
            return True
        return False
    
    def add_list(self, obj_list: List[BaseObject]) -> List[BaseObject]:
        not_added: List[BaseObject] = []
        for obj in obj_list:
            if not self.add(obj):
                not_added.append(obj)
        return not_added

    def to_bytes(self, encoding: str = 'utf-8') -> bytes:
        if self.root is None:
            raise RuntimeError("XML tree not built yet. Call build() first.")
        return ET.tostring(
            self.root,
            encoding=encoding,
            xml_declaration=True
        )  
    
    def to_string(self, encoding: str = 'utf-8') -> str:
        return self.to_bytes(encoding).decode(encoding)
        
     
        
    
