"""
STEP-XML Creator module.

This module provides the Creator class for serializing Python objects into STEP-XML documents.
It takes BaseObject instances representing STEP entities (Products, Assets, Attributes, etc.)
and generates valid STEP-XML that can be imported into STEP MDM systems.

The Creator maintains separate lists for each entity type and handles the complex hierarchical
structure of STEP-XML documents, including replacement rules, nested relationships, and
multi-workspace support.

Example:
    Basic workflow for creating STEP-XML documents::
    
        from stepxmlclient.creator import Creator
        from stepxmlclient.model import Product, Attribute
        
        # Create a creator for a specific context
        creator = Creator(context_id='Context1', workspace_id='Main')
        
        # Add entities
        product = Product({'ID': 'P1', 'Name': {'en_US': 'Example Product'}})
        creator.add(product)
        
        # Generate XML
        creator.build()
        xml_string = creator.to_string()
"""

import xml.etree.ElementTree as ET
from typing import List, Optional
from . import STEPXML_NS
from .model import BaseObject

class Creator:
    """STEP-XML document creator for serializing Python objects.
    
    Generates valid STEP-XML documents from BaseObject instances organized by entity type.
    Supports all STEP entity types and handles the complex XML structure including
    replacement rules, deletions, and multi-context/workspace configurations.
    
    Attributes:
        context_id: STEP Context ID for the document
        workspace_id: STEP Workspace ID for the document
        products: List of Product objects to include
        assets: List of Asset objects to include
        classifications: List of Classification objects to include
        entities: List of Entity objects to include
        attributes: List of Attribute definitions to include
        attributegroups: List of Attribute Group definitions to include
        listofvalues: List of List-of-Values items to include
        contexts: List of Context definitions to include
        qualifiers: List of Qualifier definitions to include
        dimensions: List of Dimension definitions to include
        usertypes: List of User Type definitions to include
        linktypes: List of Link Type definitions to include
        tags: List of Tag definitions to include
        taggroups: List of Tag Group definitions to include
        units: List of Unit definitions to include
        businessrules: List of Business Rule definitions to include
        workflows: List of Workflow definitions to include
        collections: List of Collection objects to include
        collectiongroups: List of Collection Group definitions to include
        deletedproducts: List of Product deletion specifications
        deletedassets: List of Asset deletion specifications
        product_replacement_rules: List of Product replacement rules
        replace_products: List of Products to replace
        replace_classifications: List of Classifications to replace
        replace_entities: List of Entities to replace
        replace_assets: List of Assets to replace
        replace_attributes: List of Attributes to replace
    """
    
    def __init__(
            self,
            context_id: str,
            workspace_id: str = 'Main') -> None:
        """Initialize a Creator instance.
        
        Creates a new Creator for generating STEP-XML documents. All entity lists are
        initialized as empty; populate them by calling add() or add_list() methods.
        
        Args:
            context_id: STEP Context ID to use in the generated document
                       (required, identifies the STEP context for import)
            workspace_id: STEP Workspace ID (default: 'Main')
                         identifies the workspace for multi-workspace environments
        """
        self.context_id: str = context_id
        self.workspace_id: str = workspace_id
        self.root: Optional[ET.Element] = None
        self.tree: Optional[ET.ElementTree] = None
        self.products: List[BaseObject] = []
        self.assets: List[BaseObject] = []
        self.classifications: List[BaseObject] = []
        self.entities: List[BaseObject] = []
        self.attributes: List[BaseObject] = []
        self.attributegroups: List[BaseObject] = []
        self.listofvalues: List[BaseObject] = []
        self.contexts: List[BaseObject] = []
        self.qualifiers: List[BaseObject] = []
        self.dimensions: List[BaseObject] = []
        self.usertypes: List[BaseObject] = []
        self.linktypes: List[BaseObject] = []
        self.tags: List[BaseObject] = []
        self.taggroups: List[BaseObject] = []
        self.units: List[BaseObject] = []
        self.businessrules: List[BaseObject] = []
        self.workflows: List[BaseObject] = []
        self.collections: List[BaseObject] = []
        self.collectiongroups: List[BaseObject] = []
        self.deletedproducts: List[BaseObject] = []
        self.deletedassets: List[BaseObject] = []
        self.product_replacement_rules: List[BaseObject] = []
        self.replace_products: List[BaseObject] = []
        self.replace_classifications: List[BaseObject] = []
        self.replace_entities: List[BaseObject] = []
        self.replace_assets: List[BaseObject] = []
        self.replace_attributes: List[BaseObject] = []
        return
    
    def build(self) -> None:
        """Build the XML document structure from added entities.
        
        Generates the ElementTree representation of the STEP-XML document based on all
        entities currently in the creator's lists. Must be called before to_string()
        or to_bytes(). This method:
        
        1. Creates the root STEP-ProductInformation element
        2. Adds ReplacementRules section if any replacement rules exist
        3. Adds all entity sections in the correct STEP-XML order
        4. Sets the ContextID and WorkspaceID attributes
        
        After calling build(), the XML can be accessed via to_string() or to_bytes().
        
        Note:
            The method only includes sections for entity types that have items.
            Empty lists do not generate corresponding XML elements.
        """
        self.root = ET.Element(    
            'STEP-ProductInformation',
            {
                "ContextID": self.context_id,
                "WorkspaceID": self.workspace_id
            }
        )
        self.tree = ET.ElementTree(self.root)
        # replacement rules section (Phase 1 + Phase 7)
        replacement_rules_collections = {
            "Products": self.product_replacement_rules,
            "Classifications": self.replace_classifications,
            "Entities": self.replace_entities,
            "Assets": self.replace_assets,
            "Attributes": self.replace_attributes
        }
        # Check if any replacement rules exist
        has_replacement_rules = any(replacement_rules_collections.values())
        if has_replacement_rules:
            rules = ET.SubElement(self.root, 'ReplacementRules')
            for xml_name, collection in replacement_rules_collections.items():
                if collection:
                    self._build_element_list(rules, xml_name, collection)
        # others - map XML element names to attribute names
        element_mapping = {
            "Assets": "assets",
            "Products": "products",
            "Classifications": "classifications",
            "Entities": "entities",
            "Attributes": "attributes",
            "AttributeGroups": "attributegroups",
            "ListOfValues": "listofvalues",
            "Contexts": "contexts",
            "Qualifiers": "qualifiers",
            "Dimensions": "dimensions",
            "UserTypes": "usertypes",
            "LinkTypes": "linktypes",
            "Tags": "tags",
            "TagGroups": "taggroups",
            "Units": "units",
            "BusinessRules": "businessrules",
            "Workflows": "workflows",
            "Collections": "collections",
            "CollectionGroups": "collectiongroups",
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
        """Add a collection of objects as child elements to a parent element.
        
        Internal helper method that creates a container element and populates it with
        the serialized representations of the provided objects.
        
        Args:
            parent: Parent ElementTree Element to add the collection to
            list_name: XML tag name for the collection container
            objs: List of BaseObject instances to serialize
        """
        list_element = ET.SubElement(parent, list_name)
        for obj in objs:
            obj.to_element(list_element)
        return    
        
    def add(self, obj: BaseObject) -> bool:
        """Add a single object to the appropriate collection list.
        
        Automatically routes the object to the correct list based on its _GROUP_NAME.
        Objects must be instances of BaseObject subclasses with a valid _GROUP_NAME.
        
        Args:
            obj: BaseObject instance to add
            
        Returns:
            True if the object was successfully added, False if _GROUP_NAME not found
            or is not a list attribute
            
        Example:
            creator = Creator('Context1')
            product = Product({'ID': 'P1', 'Name': {'en_US': 'Product'}})
            if creator.add(product):
                print("Product added successfully")
        """
        if obj._GROUP_NAME is None:    
            return False
        list_attr = getattr(self, obj._GROUP_NAME)
        if isinstance(list_attr, list):
            list_attr.append(obj)
            return True
        return False
    
    def add_list(self, obj_list: List[BaseObject]) -> List[BaseObject]:
        """Add multiple objects at once.
        
        Attempts to add all objects in the provided list. Returns a list of any objects
        that failed to be added (typically due to missing _GROUP_NAME).
        
        Args:
            obj_list: List of BaseObject instances to add
            
        Returns:
            List of objects that failed to be added (empty list if all succeeded)
            
        Example:
            creator = Creator('Context1')
            products = [Product({...}), Product({...})]
            failed = creator.add_list(products)
            if not failed:
                print("All products added successfully")
        """
        not_added: List[BaseObject] = []
        for obj in obj_list:
            if not self.add(obj):
                not_added.append(obj)
        return not_added

    def to_bytes(self, encoding: str = 'utf-8') -> bytes:
        """Serialize the XML document to bytes.
        
        Converts the generated ElementTree to bytes with optional encoding and
        XML declaration.
        
        Args:
            encoding: Character encoding for the output (default: 'utf-8')
            
        Returns:
            Bytes representation of the XML document with declaration
            
        Raises:
            RuntimeError: If build() has not been called yet
            
        Example:
            creator = Creator('Context1')
            creator.add(product)
            creator.build()
            xml_bytes = creator.to_bytes()
        """
        if self.root is None:
            raise RuntimeError("XML tree not built yet. Call build() first.")
        return ET.tostring(
            self.root,
            encoding=encoding,
            xml_declaration=True
        )
        
    def to_string(self, encoding: str = 'utf-8') -> str:
        """Serialize the XML document to a string.
        
        Converts the generated ElementTree to a string representation.
        
        Args:
            encoding: Character encoding to use (default: 'utf-8')
            
        Returns:
            String representation of the XML document
            
        Raises:
            RuntimeError: If build() has not been called yet
            
        Example:
            creator = Creator('Context1')
            creator.add(product)
            creator.build()
            xml_str = creator.to_string()
            print(xml_str)
        """
        return self.to_bytes(encoding).decode(encoding)
    
     
        
    
