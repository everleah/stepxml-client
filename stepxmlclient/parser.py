import xml.etree.ElementTree as ET
from typing import Any, Callable, List, Optional
from . import STEPXML_NS


def _str_to_bool(value: str) -> bool:
    """Convert XML boolean string ('true'/'false') to Python bool."""
    return value.lower() == 'true'


def _get_local_tag(element: ET.Element) -> str:
    """Extract local tag name from potentially namespaced tag.
    
    Handles both namespaced tags (e.g., '{http://...}Value') and 
    unnamespaced tags (e.g., 'Value').
    """
    tag = element.tag
    if '}' in tag:
        return tag.split('}', 1)[1]
    return tag


def _get_namespace_from_tag(tag: str) -> Optional[str]:
    """Extract namespace URL from a namespaced tag.
    
    Handles both namespaced tags (e.g., '{http://...}Value') and 
    unnamespaced tags (e.g., 'Value').
    Returns None if tag is unnamespaced.
    """
    if not tag or '}' not in tag:
        return None
    # Extract namespace from {namespace}localname format
    return tag[1:tag.index('}')]


class Parser:
    
    def __init__(self):
        self._tree = None
        self._root: Optional[ET.Element] = None
        self.products: List[dict] = []
        self.assets: List[dict] = []
        self.classifications: List[dict] = []
        self.entities: List[dict] = []
        self.attributes: List[dict] = []
        self.attribute_groups: List[dict] = []
        self.list_of_values_groups: List[dict] = []
        self.list_of_values: List[dict] = []
        self.user_types: List[dict] = []
        self.contexts: List[dict] = []
        self.link_types: List[dict] = []
        self.delete_products: List[dict] = []
        self.delete_assets: List[dict] = []
        self.delete_classifications: List[dict] = []
        self.delete_entities: List[dict] = []
        self.business_rules: List[dict] = []
        self.event_queues: List[dict] = []
        self.workflows: List[dict] = []
        self.export_configurations: List[dict] = []
        self.cross_reference_types: List[dict] = []
        self.qualifiers: List[dict] = []
        self.dimensions: List[dict] = []
        self.tags: List[dict] = []
        self.tag_groups: List[dict] = []
        self.units: List[dict] = []
        self.replacement_rules: List[dict] = []
        self.collections: List[dict] = []
        self.collection_groups: List[dict] = []
        self.bulk_update_configurations: List[dict] = []
        self.derived_event_types: List[dict] = []
        self.global_settings: dict = {}
        self.import_configurations: List[dict] = []
        self.portal_configurations: List[dict] = []
        return

    def parse_file(self, file_path: str):
        self._tree = ET.parse(file_path)
        return self.parse(self._tree.getroot())

    def parse_str(self, xml_str: str):
        return self.parse(ET.fromstring(xml_str))

    def parse(self, root: ET.Element):
        # Handle both namespaced and unnamespaced root elements
        local_tag = _get_local_tag(root)
        assert local_tag == 'STEP-ProductInformation', f"Expected STEP-ProductInformation, got {local_tag}"
        self._root = root
        self.assets = self._parse_item_list(
            'Assets', 'Asset', _parse_asset)
        self.products = self._parse_item_list(
            'Products', 'Product', _parse_product)
        self.classifications = self._parse_item_list(
            'Classifications', 'Classification', _parse_classification
        )
        self.entities = self._parse_item_list(
            'Entities', 'Entity', _parse_entity
        )
        self.attributes = self._parse_item_list(
            'AttributeList', 'Attribute', _parse_attribute
        )
        self.attribute_groups = self._parse_item_list(
            'AttributeGroupList', 'AttributeGroup', _parse_attribute_group
        )
        self.list_of_values_groups = self._parse_item_list(
            'ListOfValuesGroupList', 'ListOfValuesGroup', _parse_list_of_values_group
        )
        self.list_of_values = self._parse_item_list(
            'ListsOfValues', 'ListOfValue', _parse_list_of_value
        )
        self.user_types = self._parse_item_list(
            'UserTypes', 'UserType', _parse_user_type
        )
        self.contexts = self._parse_item_list(
            'ContextList', 'Context', _parse_context
        )
        self.link_types = self._parse_item_list(
            'EdgeTypes', 'LinkType', _parse_link_type
        )
        self.delete_assets = self._parse_item_list(
            'DeleteAssets', 'DeleteAsset', _parse_delete_asset
        )
        self.delete_products = self._parse_item_list(
            'DeleteProducts', 'DeleteProduct', _parse_delete_product
        )
        self.delete_classifications = self._parse_item_list(
            'DeleteClassifications', 'DeleteClassification', _parse_delete_classification
        )
        self.delete_entities = self._parse_item_list(
            'DeleteEntities', 'DeleteEntity', _parse_delete_entity
        )
        self.business_rules = self._parse_item_list(
            'BusinessRules', 'BusinessRule', _parse_business_rule
        )
        self.event_queues = self._parse_item_list(
            'EventQueues', 'EventQueue', _parse_event_queue
        )
        self.workflows = self._parse_item_list(
            'STEPWorkflows', 'STEPWorkflow', _parse_workflow
        )
        self.export_configurations = self._parse_item_list(
            'ExportConfigurations', 'ExportConfiguration', _parse_export_configuration
        )
        self.cross_reference_types = self._parse_item_list(
            'CrossReferenceTypes', 'CrossReferenceType', _parse_cross_reference_type
        )
        self.qualifiers = self._parse_item_list(
            'Qualifiers', 'Qualifier', _parse_qualifier
        )
        self.dimensions = self._parse_item_list(
            'DimensionList', 'Dimension', _parse_dimension
        )
        self.tags = self._parse_item_list(
            'TagList', 'Tag', _parse_tag
        )
        self.tag_groups = self._parse_item_list(
            'TagGroupList', 'TagGroup', _parse_tag_group
        )
        self.units = self._parse_item_list(
            'UnitList', 'Unit', _parse_unit
        )
        self.replacement_rules = self._parse_replacement_rules()
        self.collections, self.collection_groups = self._parse_collections()
        self.bulk_update_configurations = self._parse_item_list(
            'BulkUpdateConfigurations', 'BulkUpdateConfiguration', _parse_bulk_update_configuration
        )
        self.derived_event_types = self._parse_derived_event_types()
        self.global_settings = self._parse_global_settings()
        self.import_configurations = self._parse_item_list(
            'ImportConfigurations', 'ImportConfiguration', _parse_import_configuration
        )
        self.portal_configurations = self._parse_item_list(
            'PortalConfigurations', 'PortalConfiguration', _parse_portal_configuration
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
        
        # Try to find the item list by local tag name, ignoring namespace
        item_list = None
        
        # First try with explicit namespace (for prefixed XML like step:Products)
        item_list = self._root.find(list_name, STEPXML_NS)
        
        # If not found, search by local tag name (handles default namespaces)
        if item_list is None:
            for child in self._root:
                if _get_local_tag(child) == list_name:
                    item_list = child
                    break
        
        if item_list is not None:
            # Collect items, trying both namespace-aware and namespace-agnostic approaches
            items = []
            
            # Try with explicit namespace first
            items = list(item_list.findall(item_name, STEPXML_NS))
            
            # If no results, search by local tag name for each child
            if not items:
                for child in item_list:
                    if _get_local_tag(child) == item_name:
                        items.append(child)
            
            for item in items:
                result = parse_fct(item)
                if result is not None:
                   results.append(result)
        
        return results
    
    def _parse_replacement_rules(self) -> dict:
        """Parse replacement rules for products, classifications, entities, assets, attributes, etc."""
        replacement_rules_elem = None
        
        for child in self._root:
            local_tag = _get_local_tag(child)
            if local_tag == "ReplacementRules":
                replacement_rules_elem = child
                break
        
        if replacement_rules_elem is None:
            return {}
        
        result = {}
        
        for child in replacement_rules_elem:
            local_tag = _get_local_tag(child)
            
            if local_tag == "Attributes":
                if "Attributes" not in result:
                    result["Attributes"] = []
                result["Attributes"].append(_parse_replace_attributes(child))
            
            elif local_tag == "Products":
                if "Products" not in result:
                    result["Products"] = []
                result["Products"].append(_parse_replace_products(child))
            
            elif local_tag == "Classifications":
                if "Classifications" not in result:
                    result["Classifications"] = []
                result["Classifications"].append(_parse_replace_classifications(child))
            
            elif local_tag == "Entities":
                if "Entities" not in result:
                    result["Entities"] = []
                result["Entities"].append(_parse_replace_entities(child))
            
            elif local_tag == "Assets":
                if "Assets" not in result:
                    result["Assets"] = []
                result["Assets"].append(_parse_replace_assets(child))
            
            elif local_tag == "LinkTypes":
                if "LinkTypes" not in result:
                    result["LinkTypes"] = []
                result["LinkTypes"].append(_parse_replace_link_types(child))
            
            elif local_tag == "UserTypes":
                if "UserTypes" not in result:
                    result["UserTypes"] = []
                result["UserTypes"].append(_parse_replace_user_types(child))
            
            elif local_tag == "UserGroups":
                if "UserGroups" not in result:
                    result["UserGroups"] = []
                result["UserGroups"].append(_parse_replace_user_groups(child))
        
        return result
    
    def _parse_collections(self) -> tuple:
        """Parse collections and collection groups, returns (collections, collection_groups)."""
        collection_list_elem = None
        
        for child in self._root:
            local_tag = _get_local_tag(child)
            if local_tag == "CollectionList":
                collection_list_elem = child
                break
        
        collections = []
        collection_groups = []
        
        if collection_list_elem is not None:
            for child in collection_list_elem:
                local_tag = _get_local_tag(child)
                if local_tag == "Collection":
                    collections.append(_parse_collection_item(child, is_group=False))
                elif local_tag == "CollectionGroup":
                    collection_groups.append(_parse_collection_item(child, is_group=True))
        
        return collections, collection_groups
    
    def _parse_derived_event_types(self) -> list:
        """Parse derived event types (simple text elements)."""
        result = []
        
        for child in self._root:
            local_tag = _get_local_tag(child)
            if local_tag == "DerivedEventTypes":
                # DerivedEventTypes contains DerivedEventType text elements
                for event_child in child:
                    event_tag = _get_local_tag(event_child)
                    if event_tag == "DerivedEventType":
                        event_text = event_child.text
                        if event_text:
                            result.append({"value": event_text})
                break
        
        return result
    
    def _parse_global_settings(self) -> dict:
        """Parse global settings (system configuration)."""
        for child in self._root:
            local_tag = _get_local_tag(child)
            if local_tag == "GlobalSettings":
                result = {}
                # Parse CalculatedAttributeSettings
                for settings_child in child:
                    settings_tag = _get_local_tag(settings_child)
                    if settings_tag == "CalculatedAttributeSettings":
                        result["CalculatedAttributeSettings"] = _parse_element(settings_child, attributes=[], texts=[])
                    elif settings_tag == "AssetSettings":
                        result["AssetSettings"] = _parse_element(settings_child, attributes=[], texts=[])
                return result
        
        return {}
    
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
        # Use local tag name to handle both namespaced and unnamespaced XML
        local_tag = _get_local_tag(child)
        key = local_tag
        
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
        # Use local tag name to handle both namespaced and unnamespaced XML
        local_tag = _get_local_tag(child)
        if local_tag in cross_ref_types:
            parser_func = cross_ref_types[local_tag]
            parsed = parser_func(child)
            
            if local_tag in result:
                # Multiple elements of same type - convert to list
                if not isinstance(result[local_tag], list):
                    result[local_tag] = [result[local_tag]]
                result[local_tag].append(parsed)
            else:
                # First element of this type
                result[local_tag] = parsed
    
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
            local_tag = _get_local_tag(child)
            if local_tag == "Value":
                values[attribute_id] = _parse_value(child)
            elif local_tag == "MultiValue":
                multi_value_list = []
                for sub_child in child.findall('Value'):
                    multi_value_list.append(_parse_value(sub_child))
                # Also check for namespaced Value elements
                for sub_child in child.findall('{http://www.stibosystems.com/step}Value'):
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

def _parse_entity(element):
    """Parse Entity element with support for nested entities and cross-references.
    
    Handles:
    - Attributes: ID, ParentID, UserTypeID, QualifierID, Changed, Republished, Selected, Referenced
    - Children: KeyValue (multiple), ParentKeyValue (multiple), Name (text)
    - Children: Nested Entity (hierarchical)
    - Cross-references: ProductCrossReference (suppressed/delete variants)
    - Cross-references: ClassificationCrossReference (suppressed/delete variants)
    - Cross-references: EntityCrossReference (entity-to-entity)
    - Cross-references: AssetCrossReference (suppressed/delete variants)
    - Cross-references: ContextCrossReference, WorkspaceCrossReference
    - Other: MetaData, Values, DataContainers
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
    nested_entities = []
    
    # Define all cross-reference types supported by entities
    cross_ref_types = {
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
        "ContextCrossReference": _parse_context_cross_reference,
        "SuppressedContextCrossReference": _parse_context_cross_reference,
        "WorkspaceCrossReference": _parse_workspace_cross_reference,
        "SuppressedWorkspaceCrossReference": _parse_workspace_cross_reference,
    }
    
    # Process child elements, handling special cases
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
        elif child.tag == "ParentKeyValue":
            parent_key_values.append(_parse_key_value(child))
        elif child.tag == "Entity":
            # Nested entities (hierarchical)
            nested_entities.append(_parse_entity(child))
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
    if nested_entities:
        result["Entity"] = nested_entities
    
    return result


def _parse_context_cross_reference(element):
    """Parse ContextCrossReference or SuppressedContextCrossReference elements.
    
    Handles:
    - Attributes: ContextID, Type, QualifierID
    - Children: KeyValue (multiple), MetaData
    """
    result = _parse_element(
        element,
        attributes=("ContextID", "Type", "QualifierID"),
        specials={"MetaData": _parse_metadata}
    )
    
    # Parse KeyValue elements (can be multiple)
    key_values = []
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result


def _parse_workspace_cross_reference(element):
    """Parse WorkspaceCrossReference or SuppressedWorkspaceCrossReference elements.
    
    Handles:
    - Attributes: WorkspaceID, Type, QualifierID
    - Children: KeyValue (multiple), MetaData
    """
    result = _parse_element(
        element,
        attributes=("WorkspaceID", "Type", "QualifierID"),
        specials={"MetaData": _parse_metadata}
    )
    
    # Parse KeyValue elements (can be multiple)
    key_values = []
    for child in element:
        if child.tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result


def _parse_attribute(element: ET.Element) -> dict:
    """Parse Attribute element with ID, names, validation/LOV link, and metadata.
    
    Attributes:
    - ID, DefaultUnitID, ProductMode (Normal/Property), CryptographicKeyID
    - HierarchicalFiltering, ClassificationHierarchicalFiltering, ExternallyMaintained
    - FullTextIndexed, MultiValued, Mandatory, Derived
    - Selected (default True), Referenced (default False), Changed, Deleted
    
    Children:
    - Name (text), Validation OR ListOfValueLink
    - ValueTemplate/UnitTemplate (multiple), DimensionLink (multiple)
    - MetaData, AttributeGroupLink (multiple), UserTypeLink (multiple)
    - LinkType (multiple), ValueFilter, CurrentTasks
    """
    result = _parse_element(
        element,
        attributes=("ID", "DefaultUnitID", "ProductMode", "CryptographicKeyID",
                   "HierarchicalFiltering", "ClassificationHierarchicalFiltering",
                   "ExternallyMaintained", "FullTextIndexed", "MultiValued",
                   "Mandatory", "Derived", "Selected", "Referenced", "Changed", "Deleted"),
        texts=("Name",),
        conversions={
            "HierarchicalFiltering": (_str_to_bool, False),
            "ClassificationHierarchicalFiltering": (_str_to_bool, False),
            "ExternallyMaintained": (_str_to_bool, False),
            "FullTextIndexed": (_str_to_bool, False),
            "MultiValued": (_str_to_bool, False),
            "Mandatory": (_str_to_bool, False),
            "Derived": (_str_to_bool, False),
            "Selected": (_str_to_bool, True),
            "Referenced": (_str_to_bool, False),
            "Changed": (_str_to_bool, False),
            "Deleted": (_str_to_bool, False),
        }
    )
    
    # Parse Validation or ListOfValueLink (choice)
    for child in element:
        if child.tag.endswith("Validation"):
            result["Validation"] = child.attrib.get("Base", "")
        elif child.tag.endswith("ListOfValueLink"):
            result["ListOfValueLink"] = child.attrib.get("LOVID", "")
    
    # Parse DimensionLink elements (multiple)
    dim_links = []
    for child in element:
        if child.tag.endswith("DimensionLink"):
            dim_links.append(child.attrib.get("DimensionID", ""))
    if dim_links:
        result["DimensionLink"] = dim_links
    
    # Parse MetaData
    for child in element:
        if child.tag.endswith("MetaData"):
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse AttributeGroupLink elements (multiple)
    attr_group_links = []
    for child in element:
        if child.tag.endswith("AttributeGroupLink"):
            attr_group_links.append(child.attrib.get("AttributeGroupID", ""))
    if attr_group_links:
        result["AttributeGroupLink"] = attr_group_links
    
    # Parse UserTypeLink elements (multiple)
    user_type_links = []
    for child in element:
        if child.tag.endswith("UserTypeLink"):
            user_type_links.append(child.attrib.get("UserTypeID", ""))
    if user_type_links:
        result["UserTypeLink"] = user_type_links
    
    # Parse LinkType elements (multiple)
    link_types = []
    for child in element:
        if child.tag.endswith("LinkType"):
            link_types.append(child.attrib.get("ID", ""))
    if link_types:
        result["LinkType"] = link_types
    
    return result


def _parse_attribute_group(element: ET.Element) -> dict:
    """Parse AttributeGroup element with ID, ParentID, names, and nested groups.
    
    Attributes:
    - ID, ParentID
    - ShowInWorkbench (default True), ExcludeFromProfiling
    - Referenced (default False), ManuallySorted (default False)
    - Selected (default True), Changed (default False), Deleted (default False)
    
    Children:
    - Name (text), MetaData, Configuration
    - AttributeSequence, nested AttributeGroup (multiple)
    """
    result = _parse_element(
        element,
        attributes=("ID", "ParentID", "ShowInWorkbench", "ExcludeFromProfiling",
                   "Referenced", "ManuallySorted", "Selected", "Changed", "Deleted"),
        texts=("Name",),
        conversions={
            "ShowInWorkbench": (_str_to_bool, True),
            "ExcludeFromProfiling": (_str_to_bool, False),
            "Referenced": (_str_to_bool, False),
            "ManuallySorted": (_str_to_bool, False),
            "Selected": (_str_to_bool, True),
            "Changed": (_str_to_bool, False),
            "Deleted": (_str_to_bool, False),
        }
    )
    
    # Parse MetaData
    for child in element:
        if child.tag.endswith("MetaData"):
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse Configuration (encoded view definition)
    for child in element:
        if child.tag.endswith("Configuration") and child.text:
            result["Configuration"] = child.text
            break
    
    # Parse nested AttributeGroup elements (hierarchical)
    nested_groups = []
    for child in element:
        if child.tag.endswith("AttributeGroup"):
            nested_groups.append(_parse_attribute_group(child))
    if nested_groups:
        result["AttributeGroup"] = nested_groups
    
    return result


def _parse_list_of_values_group(element: ET.Element) -> dict:
    """Parse ListOfValuesGroup element with ID, ParentID, names, and nested groups.
    
    Attributes:
    - ID, ParentID
    - Selected (default True), Referenced (default False), Changed (default False)
    
    Children:
    - Name (text), MetaData
    - AttributeGroupLink (multiple), nested ListOfValuesGroup (multiple)
    """
    result = _parse_element(
        element,
        attributes=("ID", "ParentID", "Selected", "Referenced", "Changed"),
        texts=("Name",),
        conversions={
            "Selected": (_str_to_bool, True),
            "Referenced": (_str_to_bool, False),
            "Changed": (_str_to_bool, False),
        }
    )
    
    # Parse MetaData
    for child in element:
        if child.tag.endswith("MetaData"):
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse AttributeGroupLink elements (multiple)
    attr_group_links = []
    for child in element:
        if child.tag.endswith("AttributeGroupLink"):
            attr_group_links.append(child.attrib.get("AttributeGroupID", ""))
    if attr_group_links:
        result["AttributeGroupLink"] = attr_group_links
    
    # Parse nested ListOfValuesGroup elements (hierarchical)
    nested_groups = []
    for child in element:
        if child.tag.endswith("ListOfValuesGroup"):
            nested_groups.append(_parse_list_of_values_group(child))
    if nested_groups:
        result["ListOfValuesGroup"] = nested_groups
    
    return result


def _parse_list_of_value(element: ET.Element) -> dict:
    """Parse ListOfValue element with ID, ParentID, validation, and value items.
    
    Attributes:
    - ID, ParentID
    - AllowUserValueAddition (default: False), UseValueID (default: False)
    - IDPattern, ReplaceListOfValuesValues (default: False), DefaultUnitID
    
    Children:
    - Name (text, multiple), Validation
    - DimensionLink (multiple), MetaData, AttributeGroupLink (multiple)
    - Value (multiple), ValueGroup (multiple) - choice
    - DeleteValue (multiple)
    """
    result = _parse_element(
        element,
        attributes=("ID", "ParentID", "AllowUserValueAddition", "UseValueID",
                   "IDPattern", "ReplaceListOfValuesValues", "DefaultUnitID"),
        texts=("Name",),
        conversions={
            "AllowUserValueAddition": (_str_to_bool, False),
            "UseValueID": (_str_to_bool, False),
            "ReplaceListOfValuesValues": (_str_to_bool, False),
        }
    )
    
    # Parse Validation element
    validation_elem = None
    for child in element:
        if child.tag.endswith("Validation"):
            result["Validation"] = child.attrib.get("Base", "")
            validation_elem = child
            break
    
    # Parse DimensionLink elements (multiple)
    dim_links = []
    for child in element:
        if child.tag.endswith("DimensionLink"):
            dim_links.append(child.attrib.get("DimensionID", ""))
    if dim_links:
        result["DimensionLink"] = dim_links
    
    # Parse MetaData
    metadata_elem = None
    for child in element:
        if child.tag.endswith("MetaData"):
            result["MetaData"] = _parse_metadata(child)
            metadata_elem = child
            break
    
    # Parse AttributeGroupLink elements (multiple)
    attr_group_links = []
    for child in element:
        if child.tag.endswith("AttributeGroupLink"):
            attr_group_links.append(child.attrib.get("AttributeGroupID", ""))
    if attr_group_links:
        result["AttributeGroupLink"] = attr_group_links
    
    # Parse Value and ValueGroup elements (choice - not from MetaData or other containers)
    # We need to exclude Value elements that are direct children of containers like MetaData
    values = []
    value_groups = []
    for child in element:
        # Skip elements we've already processed above
        if child.tag.endswith(("Validation", "DimensionLink", "MetaData", "AttributeGroupLink", 
                               "Name", "DeleteValue")):
            continue
        
        # Now parse Value and ValueGroup from direct children only
        if child.tag.endswith("Value"):
            values.append(_parse_list_of_value_item(child))
        elif child.tag.endswith("ValueGroup"):
            value_groups.append(_parse_value_group(child))
    
    if values:
        result["Value"] = values
    if value_groups:
        result["ValueGroup"] = value_groups
    
    # Parse DeleteValue elements (multiple)
    delete_values = []
    for child in element:
        if child.tag.endswith("DeleteValue"):
            delete_values.append(_parse_delete_value(child))
    if delete_values:
        result["DeleteValue"] = delete_values
    
    return result


def _parse_list_of_value_item(element: ET.Element) -> dict:
    """Parse Value element within a LOV.
    
    Attributes:
    - ID (value ID), UnitID, UnitName
    - AttributeID, LOVQualifierID, QualifierID
    - Changed (default: False), Derived (default: False)
    - DerivedContextID, InheritedFrom, Inherited
    
    Text Content:
    - The actual value (mixed content)
    """
    result = _parse_element(
        element,
        attributes=("ID", "UnitID", "UnitName", "AttributeID", "LOVQualifierID",
                   "QualifierID", "DerivedContextID", "InheritedFrom", "Inherited"),
        conversions={
            "Changed": (_str_to_bool, False),
            "Derived": (_str_to_bool, False),
        }
    )
    
    # Capture text content (mixed type element)
    if element.text and element.text.strip():
        result["value"] = element.text.strip()
    
    return result


def _parse_value_group(element: ET.Element) -> dict:
    """Parse ValueGroup element (container for qualifier-specific values).
    
    Attributes:
    - ID (group ID)
    - Changed (default: False), Inherited, AttributeID
    
    Children:
    - Value (multiple) - values within this group
    """
    result = _parse_element(
        element,
        attributes=("ID", "Inherited", "AttributeID"),
        conversions={
            "Changed": (_str_to_bool, False),
        }
    )
    
    # Parse Value elements (multiple within the group)
    values = []
    for child in element:
        if child.tag.endswith("Value"):
            values.append(_parse_list_of_value_item(child))
    
    if values:
        result["Value"] = values
    
    return result


def _parse_delete_value(element: ET.Element) -> dict:
    """Parse DeleteValue element (deletion instruction for LOV value).
    
    Attributes:
    - Force (default: False) - delete despite usage
    - GenerateEvents (default: False) - generate events during deletion
    
    Text Content:
    - The value ID to delete (mixed content)
    """
    result = _parse_element(
        element,
        attributes=(),
        conversions={
            "Force": (_str_to_bool, False),
            "GenerateEvents": (_str_to_bool, False),
        }
    )
    
    # Parse boolean attributes manually since they're not in attributes tuple
    result["Force"] = _str_to_bool(element.attrib.get("Force", "false"))
    result["GenerateEvents"] = _str_to_bool(element.attrib.get("GenerateEvents", "false"))
    
    # Capture text content (value ID to delete)
    if element.text and element.text.strip():
        result["value"] = element.text.strip()
    
    return result


def _parse_user_type(element: ET.Element) -> dict:
    """Parse UserType element (object type definition).
    
    Attributes (15 total):
    - ID (required): Object type identifier
    - AllowOverlappingTerms, AllowQuarkTemplate, AllowInDesignTemplate (optional booleans)
    - Revisability (optional enum)
    - IsCategory (optional boolean, default False)
    - DefaultProfileConfiguration, NamePattern, IDPattern (optional strings)
    - ClassificationOwnsProductLinks (optional boolean)
    - ManuallySorted (optional boolean, default False)
    - ReferenceTargetLockPolicy (optional enum)
    - Selected (optional boolean, default True)
    - Referenced (optional boolean, default False)
    - Changed (optional boolean, default False)
    - Deleted (optional boolean, default False)
    
    Child Elements:
    - Name (text, multiple) - UserType display name
    - Icon (base64) - Custom icon
    - VisibleTermFields (element) - Term configuration
    - MetaData (element) - Metadata
    - DimensionLink (multiple) - Associated dimensions
    - UserTypeLink (multiple) - Parent object type links
    - AttributeLink (multiple) - Valid attributes for this type
    - Validation (element) - Validation rules
    - MIMEType (multiple) - Supported MIME types
    """
    result = _parse_element(
        element,
        attributes=("ID", "AllowOverlappingTerms", "AllowQuarkTemplate", 
                   "AllowInDesignTemplate", "Revisability", "IsCategory",
                   "DefaultProfileConfiguration", "ClassificationOwnsProductLinks",
                   "NamePattern", "IDPattern", "ManuallySorted", 
                   "ReferenceTargetLockPolicy", "Selected", "Referenced", 
                   "Changed", "Deleted"),
        specials={
            "MetaData": _parse_metadata,
            "Validation": lambda elem: elem.attrib.get("Base", "")
        },
        conversions={
            "AllowOverlappingTerms": (_str_to_bool, False),
            "AllowQuarkTemplate": (_str_to_bool, False),
            "AllowInDesignTemplate": (_str_to_bool, False),
            "IsCategory": (_str_to_bool, False),
            "ClassificationOwnsProductLinks": (_str_to_bool, False),
            "ManuallySorted": (_str_to_bool, False),
            "Selected": (_str_to_bool, True),
            "Referenced": (_str_to_bool, False),
            "Changed": (_str_to_bool, False),
            "Deleted": (_str_to_bool, False),
        }
    )
    
    # Parse Name elements (text, multiple)
    names = []
    for child in element:
        if child.tag.endswith("Name"):
            if child.text:
                names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse Icon (base64)
    for child in element:
        if child.tag.endswith("Icon"):
            if child.text:
                result["Icon"] = child.text
            break
    
    # Parse VisibleTermFields
    for child in element:
        if child.tag.endswith("VisibleTermFields"):
            result["VisibleTermFields"] = child.attrib.copy()
            break
    
    # Parse DimensionLink (multiple)
    dim_links = []
    for child in element:
        if child.tag.endswith("DimensionLink"):
            dim_links.append(child.attrib.get("DimensionID", ""))
    if dim_links:
        result["DimensionLink"] = dim_links
    
    # Parse UserTypeLink (multiple) - parent type links
    user_type_links = []
    for child in element:
        if child.tag.endswith("UserTypeLink"):
            user_type_links.append(child.attrib.get("UserTypeID", ""))
    if user_type_links:
        result["UserTypeLink"] = user_type_links
    
    # Parse AttributeLink (multiple) - valid attributes for this type
    attr_links = []
    for child in element:
        if child.tag.endswith("AttributeLink"):
            attr_links.append(child.attrib.get("AttributeID", ""))
    if attr_links:
        result["AttributeLink"] = attr_links
    
    # Parse MIMEType (multiple)
    mime_types = []
    for child in element:
        if child.tag.endswith("MIMEType"):
            mime_type_dict = {"MIMEType": child.text or ""}
            mime_type_dict.update(child.attrib.copy())
            mime_types.append(mime_type_dict)
    if mime_types:
        result["MIMEType"] = mime_types
    
    return result


def _parse_context(element: ET.Element) -> dict:
    """Parse Context element (multi-language/multi-dimensional context).
    
    Attributes (5 total):
    - ID (required): Context identifier (e.g., "en_US", "fr_FR")
    - Priority (optional, default "0") - Cross-context priority
    - Locale (optional string) - Locale code for language/region
    - Selected (optional boolean, default True)
    - Referenced (optional boolean, default False)
    - Changed (optional boolean, default False)
    - Deleted (optional boolean, default False)
    
    Child Elements:
    - Name (text, multiple) - Context display name
    - DimensionPointLink (multiple) - Associated dimension points
    """
    result = _parse_element(
        element,
        attributes=("ID", "Priority", "Locale", "Selected", "Referenced", 
                   "Changed", "Deleted"),
        conversions={
            "Priority": (lambda x: x, "0"),
            "Selected": (_str_to_bool, True),
            "Referenced": (_str_to_bool, False),
            "Changed": (_str_to_bool, False),
            "Deleted": (_str_to_bool, False),
        }
    )
    
    # Parse Name elements (text, multiple)
    names = []
    for child in element:
        if child.tag.endswith("Name"):
            if child.text:
                names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse DimensionPointLink (multiple)
    dim_point_links = []
    for child in element:
        if child.tag.endswith("DimensionPointLink"):
            dim_point_links.append(child.attrib.get("DimensionPointID", ""))
    if dim_point_links:
        result["DimensionPointLink"] = dim_point_links
    
    return result

def _parse_link_type(element: ET.Element) -> dict:
    """Parse LinkType element (cross-reference type definition).
    
    Note: In STEP XML, LinkType elements appear within other structures
    to indicate which link types (CA=Classification-to-Attribute or 
    PA=Product-to-Attribute) are valid for an attribute.
    
    Attributes (1 total):
    - LinkTypeID (required): Either "CA" or "PA"
      - CA: Classification-to-Attribute link type
      - PA: Product-to-Attribute link type
    """
    return _parse_element(
        element,
        attributes=("LinkTypeID",)
    )

def _parse_business_rule(element: ET.Element) -> dict:
    """Parse BusinessRule element (business rule definition).
    
    Business rules can be Actions, Conditions, Functions, or Libraries.
    They contain business logic that executes within STEP.
    
    Attributes (4 total):
    - ID (required): Unique identifier for the business rule
    - Type (required): Rule type - Action, Condition, Function, or Library
    - Scope (optional): Local or Global (only for Actions/Conditions)
    - RunPrivileged (optional): Boolean, default False
    
    Child elements:
    - Name (multiple): Display name in different languages
    - Description (optional): Rule description
    - Dependency (multiple): Dependencies on other rules
    - FunctionDependency (multiple): Dependencies on functions
    - OnApprove (optional): Execution on approval
    - Configuration (optional): Encoded configuration data
    - ValidObjectTypes (optional): Object types this rule applies to
    - SetupGroupLink (optional): Setup group link
    """
    result = _parse_element(
        element,
        attributes=("ID", "Type", "Scope", "RunPrivileged"),
        conversions={
            "RunPrivileged": (lambda x: x.lower() == "true", False)
        }
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse Description
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Description" and child.text:
            result["Description"] = child.text
            break
    
    return result

def _parse_event_queue(element: ET.Element) -> dict:
    """Parse EventQueue element (event queue configuration).
    
    Event queues store events generated by STEP system operations.
    They can be read/processed or discarded.
    
    Attributes (7 total):
    - ID (optional): Unique identifier for the event queue
    - QueueStatus (optional): Read or Discard, default Read
    - DaysRetained (optional): Number of days to retain events
    - Selected (optional): Boolean, default True
    - Referenced (optional): Boolean, default False
    - Changed (optional): Boolean, default False
    - Deleted (optional): Boolean, default False
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    - Configuration (required): Encoded configuration data
    """
    result = _parse_element(
        element,
        attributes=("ID", "QueueStatus", "DaysRetained", "Selected", "Referenced", "Changed", "Deleted"),
        conversions={
            "Selected": (lambda x: x.lower() == "true", True),
            "Referenced": (lambda x: x.lower() == "true", False),
            "Changed": (lambda x: x.lower() == "true", False),
            "Deleted": (lambda x: x.lower() == "true", False)
        }
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    return result

def _parse_workflow(element: ET.Element) -> dict:
    """Parse STEPWorkflow element (workflow definition).
    
    Workflows orchestrate business processes in STEP.
    They define states, transitions, and validations.
    
    Attributes (3 total):
    - ID (required): Unique identifier for the workflow
    - Selected (optional): Boolean, default True
    - Referenced (optional): Boolean, default False
    - Changed (optional): Boolean, default False
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    - ValidUserTypeLink (multiple): Object types valid in workflow
    - StartCondition (optional): Condition for workflow start
    - Configuration (optional): Encoded configuration data
    - LocalBusinessRule (multiple): Embedded business rules
    - BusinessRuleLink (multiple): References to business rules
    - SetupGroupLink (optional): Setup group link
    """
    result = _parse_element(
        element,
        attributes=("ID", "Selected", "Referenced", "Changed"),
        conversions={
            "Selected": (lambda x: x.lower() == "true", True),
            "Referenced": (lambda x: x.lower() == "true", False),
            "Changed": (lambda x: x.lower() == "true", False)
        }
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse ValidUserTypeLink elements (multiple)
    user_type_links = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "ValidUserTypeLink":
            user_type_links.append(child.attrib.get("UserTypeID", ""))
    if user_type_links:
        result["ValidUserTypeLink"] = user_type_links
    
    return result

def _parse_export_configuration(element: ET.Element) -> dict:
    """Parse ExportConfiguration element (export/integration configuration).
    
    Export configurations define how data is exported from STEP.
    They specify output format, target systems, and mapping rules.
    
    Attributes (1 total):
    - ID (optional): Unique identifier for the configuration
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    - ClassificationReference (multiple): Classifications this applies to
    - Configuration (optional): Encoded configuration data
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse ClassificationReference elements (multiple)
    class_refs = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "ClassificationReference":
            class_refs.append(child.attrib.get("ClassificationID", ""))
    if class_refs:
        result["ClassificationReference"] = class_refs
    
    return result

def _parse_delete_classification(element: ET.Element) -> dict:
    """Parse DeleteClassification element (Phase 10: Organizational Structure).
    
    Specifies deletion of a classification and optionally its values/subtypes.
    Attributes include the classification identifier and its type.
    
    Attributes (2 total):
    - ID (required): Classification identifier to delete
    - Type (required): Type of deletion ('All', 'SubTypes', or 'Values')
    
    Child elements:
    - KeyValue (multiple): Specific values/keys to delete
    """
    result = _parse_element(
        element,
        attributes=("ID", "Type")
    )
    
    # Parse KeyValue elements (multiple)
    key_values = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result

def _parse_delete_entity(element: ET.Element) -> dict:
    """Parse DeleteEntity element (Phase 10: Organizational Structure).
    
    Specifies deletion of an entity and optionally its records/relationships.
    Attributes include the entity identifier.
    
    Attributes (1 total):
    - ID (required): Entity identifier to delete
    
    Child elements:
    - KeyValue (multiple): Entity records/keys to delete
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse KeyValue elements (multiple)
    key_values = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "KeyValue":
            key_values.append(_parse_key_value(child))
    if key_values:
        result["KeyValue"] = key_values
    
    return result

def _parse_cross_reference_type(element: ET.Element) -> dict:
    """Parse CrossReferenceType element (Phase 10: Organizational Structure).
    
    Defines a type of cross-reference relationship between objects.
    Cross-reference types specify how different entities relate to each other.
    
    Attributes (1 total):
    - ID (required): Unique identifier for the cross-reference type
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    return result

def _parse_qualifier(element: ET.Element) -> dict:
    """Parse Qualifier element (Phase 10: Organizational Structure).
    
    Represents a dimension qualifier or multi-dimensional data point.
    Qualifiers enable multi-dimensional attribute management in STEP.
    
    Attributes (1 total):
    - ID (required): Unique identifier for the qualifier
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    - DimensionPointLink (multiple): Dimension point references
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse DimensionPointLink elements (multiple)
    dim_links = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "DimensionPointLink":
            dim_links.append({
                "DimensionID": child.attrib.get("DimensionID", ""),
                "DimensionPointID": child.attrib.get("DimensionPointID", "")
            })
    if dim_links:
        result["DimensionPointLink"] = dim_links
    
    return result

def _parse_dimension(element: ET.Element) -> dict:
    """Parse Dimension element (Phase 11: Foundational Elements).
    
    Represents a dimension for multi-dimensional data organization.
    Dimensions define axes along which data can be organized (e.g., Market, Color).
    
    Attributes (2 total):
    - ID (required): Unique identifier for the dimension
    - AllowDuplicates (optional): Whether duplicate dimension points are allowed
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    - DimensionPoint (multiple): Points/values for this dimension
    """
    result = _parse_element(
        element,
        attributes=("ID", "AllowDuplicates")
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse DimensionPoint elements (multiple)
    dim_points = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "DimensionPoint":
            dim_points.append(_parse_dimension_point(child))
    if dim_points:
        result["DimensionPoint"] = dim_points
    
    return result

def _parse_dimension_point(element: ET.Element) -> dict:
    """Parse DimensionPoint element (Phase 11: Foundational Elements).
    
    Represents a point/value within a dimension.
    
    Attributes (1 total):
    - ID (required): Unique identifier for this dimension point
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    return result

def _parse_tag(element: ET.Element) -> dict:
    """Parse Tag element (Phase 11: Foundational Elements).
    
    Represents a flexible tag for object categorization.
    Tags enable custom classification independent of the fixed hierarchy.
    
    Attributes (1 total):
    - ID (required): Unique identifier for the tag
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    return result

def _parse_tag_group(element: ET.Element) -> dict:
    """Parse TagGroup element (Phase 11: Foundational Elements).
    
    Represents a hierarchical grouping of tags.
    Tag groups organize tags into logical collections.
    
    Attributes (1 total):
    - ID (required): Unique identifier for the tag group
    
    Child elements:
    - Name (multiple): Display name in different languages
    - MetaData (optional): Metadata attributes and values
    - TagGroup (multiple): Nested tag groups (hierarchical)
    - Tag (multiple): Tags in this group
    """
    result = _parse_element(
        element,
        attributes=("ID",)
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name" and child.text:
            names.append(child.text)
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse nested TagGroup elements (multiple)
    tag_groups = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "TagGroup":
            tag_groups.append(_parse_tag_group(child))
    if tag_groups:
        result["TagGroup"] = tag_groups
    
    # Parse Tag elements (multiple)
    tags = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Tag":
            tags.append(_parse_tag(child))
    if tags:
        result["Tag"] = tags
    
    return result

def _parse_unit(element: ET.Element) -> dict:
    """Parse Unit element (Phase 11: Foundational Elements).
    
    Represents a measurement unit (e.g., meters, kilograms, liters).
    Units are used for quantitative attribute values.
    
    Attributes (4 total):
    - ID (required): Unique identifier for the unit
    - Name (optional): Display name of the unit
    - Symbol (optional): Unit symbol (e.g., 'm', 'kg', 'l')
    - Formula (optional): Conversion formula to base unit
    
    Child elements:
    - MetaData (optional): Metadata attributes and values
    """
    result = _parse_element(
        element,
        attributes=("ID", "Name", "Symbol", "Formula")
    )
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    return result


# Phase 12: Replacement Rules and Collections



def _parse_replace_attributes(element: ET.Element) -> dict:
    """Parse replacement rules for attributes."""
    return _parse_element(element, attributes=[], texts=[], specials={})


def _parse_replace_products(element: ET.Element) -> dict:
    """Parse replacement rules for products."""
    result = {}
    
    for child in element:
        local_tag = _get_local_tag(child)
        
        if local_tag == "ReplaceValues":
            if "ReplaceValues" not in result:
                result["ReplaceValues"] = []
            result["ReplaceValues"].append(_parse_replace_values(child))
        
        elif local_tag == "ReplaceCrossReferences":
            if "ReplaceCrossReferences" not in result:
                result["ReplaceCrossReferences"] = []
            result["ReplaceCrossReferences"].append(_parse_replace_cross_references(child))
        
        elif local_tag == "ReplaceAttributeLinks":
            if "ReplaceAttributeLinks" not in result:
                result["ReplaceAttributeLinks"] = []
            result["ReplaceAttributeLinks"].append(_parse_replace_attribute_links(child))
        
        elif local_tag == "ReplaceClassificationReferences":
            if "ReplaceClassificationReferences" not in result:
                result["ReplaceClassificationReferences"] = []
            result["ReplaceClassificationReferences"].append(_parse_replace_classification_references(child))
    
    return result


def _parse_replace_classifications(element: ET.Element) -> dict:
    """Parse replacement rules for classifications."""
    result = {}
    
    for child in element:
        local_tag = _get_local_tag(child)
        
        if local_tag == "ReplaceValues":
            if "ReplaceValues" not in result:
                result["ReplaceValues"] = []
            result["ReplaceValues"].append(_parse_replace_values(child))
        
        elif local_tag == "ReplaceCrossReferences":
            if "ReplaceCrossReferences" not in result:
                result["ReplaceCrossReferences"] = []
            result["ReplaceCrossReferences"].append(_parse_replace_cross_references(child))
        
        elif local_tag == "ReplaceAttributeLinks":
            if "ReplaceAttributeLinks" not in result:
                result["ReplaceAttributeLinks"] = []
            result["ReplaceAttributeLinks"].append(_parse_replace_attribute_links(child))
    
    return result


def _parse_replace_entities(element: ET.Element) -> dict:
    """Parse replacement rules for entities."""
    result = {}
    
    for child in element:
        local_tag = _get_local_tag(child)
        
        if local_tag == "ReplaceValues":
            if "ReplaceValues" not in result:
                result["ReplaceValues"] = []
            result["ReplaceValues"].append(_parse_replace_values(child))
        
        elif local_tag == "ReplaceCrossReferences":
            if "ReplaceCrossReferences" not in result:
                result["ReplaceCrossReferences"] = []
            result["ReplaceCrossReferences"].append(_parse_replace_cross_references(child))
    
    return result


def _parse_replace_assets(element: ET.Element) -> dict:
    """Parse replacement rules for assets."""
    result = {}
    
    for child in element:
        local_tag = _get_local_tag(child)
        
        if local_tag == "ReplaceValues":
            if "ReplaceValues" not in result:
                result["ReplaceValues"] = []
            result["ReplaceValues"].append(_parse_replace_values(child))
        
        elif local_tag == "ReplaceCrossReferences":
            if "ReplaceCrossReferences" not in result:
                result["ReplaceCrossReferences"] = []
            result["ReplaceCrossReferences"].append(_parse_replace_cross_references(child))
    
    return result


def _parse_replace_link_types(element: ET.Element) -> dict:
    """Parse replacement rules for link types."""
    return _parse_element(element, attributes=[], texts=[], specials={})


def _parse_replace_user_types(element: ET.Element) -> dict:
    """Parse replacement rules for user types."""
    return _parse_element(element, attributes=[], texts=[], specials={})


def _parse_replace_user_groups(element: ET.Element) -> dict:
    """Parse replacement rules for user groups."""
    return _parse_element(element, attributes=[], texts=[], specials={})


def _parse_replace_values(element: ET.Element) -> dict:
    """Parse replacement values instruction for attributes."""
    return _parse_element(
        element,
        attributes=["AttributeID", "AttributeGroupID", "ContextID"],
        texts=[]
    )


def _parse_replace_cross_references(element: ET.Element) -> dict:
    """Parse replacement cross references instruction."""
    return _parse_element(
        element,
        attributes=["CrossReferenceID", "ContextID", "MountLocation"],
        texts=[]
    )


def _parse_replace_attribute_links(element: ET.Element) -> dict:
    """Parse replacement attribute links instruction."""
    return _parse_element(
        element,
        attributes=["AttributeID"],
        texts=[]
    )


def _parse_replace_classification_references(element: ET.Element) -> dict:
    """Parse replacement classification references instruction."""
    return _parse_element(element, attributes=[], texts=[])


def _parse_collection_item(element: ET.Element, is_group: bool = False) -> dict:
    """Parse collection or collection group element."""
    result = _parse_element(
        element,
        attributes=["ID", "ParentID"] + (["QueryURL"] if not is_group else []),
        texts=[]
    )
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name":
            name_text = child.text
            if name_text:
                name_dict = {"value": name_text}
                # Get attributes (Locale, etc.)
                for attr_name, attr_value in child.attrib.items():
                    local_attr = _get_local_tag(attr_name)
                    name_dict[local_attr] = attr_value
                names.append(name_dict)
    
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # For collection groups, parse nested groups and collections
    if is_group:
        collection_groups = []
        collections = []
        for child in element:
            local_tag = _get_local_tag(child)
            if local_tag == "CollectionGroup":
                collection_groups.append(_parse_collection_item(child, is_group=True))
            elif local_tag == "Collection":
                collections.append(_parse_collection_item(child, is_group=False))
        
        if collection_groups:
            result["CollectionGroup"] = collection_groups
        if collections:
            result["Collection"] = collections
    
    return result


# Phase 13: Advanced Configuration Elements

def _parse_bulk_update_configuration(element: ET.Element) -> dict:
    """Parse bulk update configuration."""
    result = _parse_element(element, attributes=["ID"], texts=[])
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name":
            name_text = child.text
            if name_text:
                names.append({"value": name_text})
    
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse ClassificationReference elements (multiple)
    class_refs = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "ClassificationReference":
            class_refs.append(_parse_classification_reference(child))
    
    if class_refs:
        result["ClassificationReference"] = class_refs
    
    # Parse Configuration element
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Configuration":
            result["Configuration"] = _parse_element(child, attributes=[], texts=[])
            break
    
    return result


def _parse_derived_event_type(element: ET.Element) -> dict:
    """Parse derived event type (simple text)."""
    event_text = element.text
    if event_text:
        return {"value": event_text}
    return {}


def _parse_import_configuration(element: ET.Element) -> dict:
    """Parse import configuration."""
    result = _parse_element(element, attributes=["ID"], texts=[])
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name":
            name_text = child.text
            if name_text:
                names.append({"value": name_text})
    
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse ClassificationReference elements (multiple)
    class_refs = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "ClassificationReference":
            class_refs.append(_parse_classification_reference(child))
    
    if class_refs:
        result["ClassificationReference"] = class_refs
    
    # Parse Configuration element
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Configuration":
            result["Configuration"] = _parse_element(child, attributes=[], texts=[])
            break
    
    return result


def _parse_portal_configuration(element: ET.Element) -> dict:
    """Parse portal/web UI configuration."""
    result = _parse_element(
        element,
        attributes=["ID", "Selected", "Referenced", "Changed"],
        texts=[],
        conversions={
            "Selected": (bool, True),
            "Referenced": (bool, False),
            "Changed": (bool, False)
        }
    )
    
    # Parse SetupGroupLink
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "SetupGroupLink":
            result["SetupGroupLink"] = _parse_element(child, attributes=["ID"], texts=[])
            break
    
    # Parse Name elements (multiple)
    names = []
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Name":
            name_text = child.text
            if name_text:
                names.append({"value": name_text})
    
    if names:
        result["Name"] = names
    
    # Parse MetaData
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "MetaData":
            result["MetaData"] = _parse_metadata(child)
            break
    
    # Parse Configuration element
    for child in element:
        local_tag = _get_local_tag(child)
        if local_tag == "Configuration":
            result["Configuration"] = _parse_element(child, attributes=[], texts=[])
            break
    
    return result

