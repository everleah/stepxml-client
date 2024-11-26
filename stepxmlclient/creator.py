import xml.etree.ElementTree as ET

from . import STEPXML_NS
from .model import BaseObject

class Creator:
    
    def __init__(
            self, 
            context_id : str, 
            workspace_id : str = 'Main' ):
        self.context_id = context_id
        self.workspace_id = workspace_id
        self.root = None
        self.tree = None
        self.products = []
        self.assets = []
        self.deletedproducts = []
        self.deletedassets = []
        self.product_replacement_rules = []
        
        return
    
    def build(self):
        self.root = ET.Element(
            tag='STEP-ProductInformation',
            attrib={
                "ContextID" : self.context_id,
                "WorkspaceID" : self.workspace_id
            })
        self.tree = ET.ElementTree(self.root)
        # product replacement rules
        if self.product_replacement_rules:
            rules = ET.SubElement(self.root, 'ReplacementRules')
            self._build_element_list(
                rules, "Products", self.product_replacement_rules)
        # others
        for name in ("Assets", "Products", "DeletedAssets", "DeletedProducts"):
            values = getattr(self, name.lower())
            if values:
                self._build_element_list(self.root, name, values)
        return
        
    def _build_element_list(self, parent, 
                            list_name : str, 
                            objs : list[BaseObject]):
        list_element = ET.SubElement(parent, list_name)
        for obj in objs:
            objs.to_element(list_element)
        return
            
        
    def add(self, obj : BaseObject):
        list_attr = getattr(self, obj._GROUP_NAME, None)
        if list_attr is not None:
            list_attr.append(obj)
            return True
        return False
    
    def add_list(self, obj_list : list[BaseObject]):
        not_added = []
        for obj in obj_list:
            if not self.add(obj):
                not_added.append(obj)
        return not_added

        
        
    
