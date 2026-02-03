# STEP XML Parser - Usage Guide

**Last Updated:** February 3, 2026  
**Parser Version:** Phase 14 Complete  
**Coverage:** ~80% of STEP-XML schema (223 tests passing)

---

## Quick Start

```python
from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET

# Parse from file
parser = Parser()
parser.parse_file('step_export.xml')

# Or parse from string
parser = Parser()
xml_string = '<STEP-ProductInformation>...</STEP-ProductInformation>'
parser.parse(ET.fromstring(xml_string))

# Access parsed data
print(f"Products: {len(parser.products)}")
print(f"Assets: {len(parser.assets)}")
print(f"Classifications: {len(parser.classifications)}")

# Inspect a product
if parser.products:
    product = parser.products[0]
    print(f"Product ID: {product['ID']}")
    print(f"Product Name: {product['Name']}")
```

---

## Parser Data Structure

The parser maintains the following data attributes, all initialized as empty lists (or dicts for singletons) in `__init__()`:

```python
parser.products                      # List[dict] - Product definitions
parser.assets                        # List[dict] - Asset definitions
parser.classifications               # List[dict] - Classification hierarchies
parser.entities                      # List[dict] - Entity definitions
parser.delete_products               # List[dict] - Product deletion instructions
parser.delete_assets                 # List[dict] - Asset deletion instructions
parser.delete_classifications        # List[dict] - Classification deletion specs
parser.delete_entities               # List[dict] - Entity deletion specs
parser.attributes                    # List[dict] - Attribute/property definitions
parser.attribute_groups              # List[dict] - Attribute group hierarchies
parser.list_of_values_groups         # List[dict] - LOV group hierarchies
parser.list_of_values                # List[dict] - LOV enumeration definitions
parser.user_types                    # List[dict] - Object type definitions
parser.contexts                      # List[dict] - Multi-language/dimensional contexts
parser.link_types                    # List[dict] - Relation type definitions
parser.business_rules                # List[dict] - Business rule definitions
parser.event_queues                  # List[dict] - Event queue configurations
parser.workflows                     # List[dict] - Workflow definitions
parser.export_configurations         # List[dict] - Export/integration configs
parser.cross_reference_types         # List[dict] - Cross-reference type definitions
parser.qualifiers                    # List[dict] - Multi-dimensional qualifiers
parser.dimensions                    # List[dict] - Dimension axes (e.g., Market, Color)
parser.tags                          # List[dict] - Tag definitions
parser.tag_groups                    # List[dict] - Tag group hierarchies
parser.units                         # List[dict] - Measurement unit definitions
parser.replacement_rules             # dict - Bulk replacement operation rules (singleton)
parser.collections                   # List[dict] - Data collection definitions
parser.collection_groups             # List[dict] - Collection group hierarchies
parser.bulk_update_configurations    # List[dict] - Bulk update configs
parser.derived_event_types           # List[dict] - Event system extensions
parser.global_settings               # dict - System-wide settings (singleton)
parser.import_configurations         # List[dict] - Import configuration definitions
parser.portal_configurations         # List[dict] - Portal/UI configuration definitions
parser.keys                          # List[dict] - Key (unique identifier) definitions
parser.cross_contexts                # List[dict] - Cross-context definitions
parser.business_libraries            # List[dict] - Business rule library definitions
parser.setup_groups                  # List[dict] - Setup group hierarchies
parser.action_sets                   # List[dict] - Action set definitions
parser.status_flags                  # List[dict] - Status flag definitions
parser.integration_endpoints         # List[dict] - Integration endpoint definitions
```

---

## What Gets Parsed

### 1. Core Entities

#### **Products** (`parser.products`)
Root-level product definitions with hierarchical support (parent-child relationships).

**Dictionary Structure:**
```python
{
    "ID": "PROD001",                              # Product unique identifier
    "ParentId": "PARENT_PROD",                    # Parent product ID (optional)
    "UserTypeID": "ProductType1",                 # Object type definition reference
    "Name": "Product Name",                       # Simple text (not list)
    "Values": [                                   # Attribute values container
        {
            "AttributeID": "Description",
            "value": "Product description text",
            "QualifierID": "en_US",               # Language/context qualifier
            "ContextID": "MarketUS"               # Context/dimension
        }
    ],
    "AssetCrossReference": {                      # Single or list depending on count
        "AssetID": "ASSET123",
        "Type": "image",                          # Relation type
        "Changed": True,                          # Boolean
        "QualifierID": "en_US",                   # Optional context
        "KeyValue": [                             # Alternative identification
            {"KeyID": "externalKey", "value": "ext_value"}
        ],
        "MetaData": { ... }                       # Optional metadata
    },
    "ProductCrossReference": [                    # Multiple references as list
        {
            "ProductID": "COMP001",
            "Type": "component",
            "MountLocation": "/variants[0]",      # Hierarchy positioning
            "Changed": False,
            "QualifierID": "en_US"
        }
    ],
    "ClassificationReference": { ... },          # Classification link
    "EntityCrossReference": { ... }               # Entity link
    "DeleteAssetCrossReference": { ... },         # Asset deletion instruction
    "DeleteProductCrossReference": { ... },       # Product deletion instruction
    "MetaData": { ... }                           # Optional metadata
}
```

**Key Points:**
- Single references returned as dict (e.g., `AssetCrossReference`)
- Multiple references returned as list (e.g., `ProductCrossReference[]`)
- Name is simple text string (not list of dicts)
- All boolean attributes converted from "true"/"false" strings to Python bool
- Values container holds all attribute values for the product
- Optional QualifierID and ContextID indicate language/market-specific data

---

#### **Assets** (`parser.assets`)
Media/file asset definitions with reference capabilities.

**Dictionary Structure:**
```python
{
    "ID": "ASSET001",                            # Asset unique identifier
    "Name": "Asset Name",                        # Simple text
    "KeyValue": [                                # Alternative identifiers
        {"KeyID": "fileId", "value": "file123"}
    ],
    "Values": [                                  # Metadata values
        {
            "AttributeID": "FileSize",
            "value": "1024KB",
            "QualifierID": "en_US"
        }
    ],
    "MetaData": { ... }                          # Optional metadata
}
```

---

#### **Classifications** (`parser.classifications`)
Hierarchical classification/category structures with multiple relation types.

**Dictionary Structure:**
```python
{
    "ID": "CAT001",                              # Classification ID
    "ParentID": "ROOT_CAT",                      # Parent classification
    "UserTypeID": "CategoryType",                # Object type
    "QualifierID": "Context1",                   # Context qualifier
    "Changed": True,                             # Boolean flag
    "Republished": False,                        # Boolean flag
    "Selected": True,                            # Boolean flag
    "Referenced": False,                         # Boolean flag
    "Name": "Category Name",                     # Text
    "KeyValue": [                                # Alternative IDs
        {"KeyID": "legacyCode", "value": "LEG001"}
    ],
    "ParentKeyValue": [                          # Parent alternative IDs
        {"KeyID": "parentCode", "value": "PAR001"}
    ],
    "Classification": [                          # Nested classifications (hierarchical)
        {
            "ID": "CAT001_SUB",
            "Name": "Sub-Category",
            # ... recursive structure
        }
    ],
    "ProductReference": { ... },                 # Product links
    "ProductCrossReference": { ... },            # Additional product links
    "ClassificationCrossReference": { ... },     # Classification links
    "EntityCrossReference": { ... },             # Entity links
    "AssetCrossReference": { ... },              # Asset links
    "MetaData": { ... }
}
```

---

#### **Entities** (`parser.entities`)
Master data entities with extensive relation support (20+ relation types).

**Dictionary Structure:**
```python
{
    "ID": "SUPPLIER001",                         # Entity ID
    "ParentID": "SUPPLIERS",                     # Parent entity
    "UserTypeID": "SupplierType",                # Object type
    "QualifierID": "RegionEU",                   # Qualifier
    "Changed": False,
    "Name": "Entity Name",
    "KeyValue": [ ... ],                         # Alternative IDs
    "ParentKeyValue": [ ... ],                   # Parent alternative IDs
    "Entity": [ ... ],                           # Nested entities (hierarchical)
    
    # Standard relation types (20+ possible)
    "ProductReference": { ... },
    "ProductCrossReference": { ... },
    "DeleteProductCrossReference": { ... },
    "ClassificationCrossReference": { ... },
    "EntityCrossReference": { ... },
    "AssetCrossReference": { ... },
    "ContextCrossReference": { ... },
    "WorkspaceCrossReference": { ... },
    
    # Suppressed variants (context-specific suppression)
    "SuppressedProductCrossReference": { ... },  # Not yet parsed (Phase 15+)
    "SuppressedAssetCrossReference": { ... },    # Not yet parsed (Phase 15+)
    
    "MetaData": { ... }
}
```

---

### 2. Attribute System

#### **Attributes** (`parser.attributes`)
Property/field definitions for objects.

**Dictionary Structure:**
```python
{
    "ID": "Description",                         # Attribute ID
    "DefaultUnitID": "NoUnit",                   # Unit reference
    "ProductMode": "STORED",                     # Storage mode
    "CryptographicKeyID": "key1",                # Optional encryption key
    "HierarchicalFiltering": False,              # Boolean
    "ClassificationHierarchicalFiltering": True, # Boolean
    "ExternallyMaintained": False,               # Boolean
    "FullTextIndexed": True,                     # Boolean
    "MultiValued": True,                         # Boolean
    "Mandatory": False,                          # Boolean
    "Derived": False,                            # Boolean
    "Selected": True,                            # Boolean
    "Referenced": False,                         # Boolean
    "Changed": False,                            # Boolean
    "Deleted": False,                            # Boolean
    "Name": "Description",                       # Text
    "Validation": {                              # Validation rules
        "base": "xs:string",                     # XSD base type
        "ListOfValueLink": {                     # Enumeration link
            "ListOfValuesID": "StatusValues"
        }
    },
    "DimensionLink": [                           # Multi-dimensional support
        {"DimensionID": "Market"}
    ],
    "MetaData": { ... },
    "AttributeGroupLink": [ ... ],               # Group membership
    "UserTypeLink": [ ... ],                     # Type constraints
    "LinkType": [ ... ]                          # Relation type constraints
}
```

---

#### **AttributeGroups** (`parser.attribute_groups`)
Hierarchical organization of attributes.

**Dictionary Structure:**
```python
{
    "ID": "BasicInfo",                           # Group ID
    "ParentID": "ProductAttributes",             # Parent group
    "ShowInWorkbench": True,                     # Boolean
    "ExcludeFromProfiling": False,               # Boolean
    "Referenced": False,                         # Boolean
    "ManuallySorted": True,                      # Boolean
    "Selected": True,                            # Boolean
    "Changed": False,                            # Boolean
    "Deleted": False,                            # Boolean
    "Name": "Basic Information",                 # Text
    "AttributeGroup": [                          # Nested groups (hierarchical)
        {
            "ID": "BasicInfo_Sub",
            "Name": "Sub-Group",
            # ... recursive structure
        }
    ],
    "MetaData": { ... },
    "Configuration": { ... }
}
```

---

#### **ListOfValuesGroups** (`parser.list_of_values_groups`)
Enumeration group hierarchies.

**Dictionary Structure:**
```python
{
    "ID": "StatusValues",                        # Group ID
    "ParentID": "AllEnumerations",               # Parent group
    "Selected": True,                            # Boolean
    "Referenced": False,                         # Boolean
    "Changed": False,                            # Boolean
    "Name": "Status Enumerations",               # Text
    "ListOfValuesGroup": [ ... ],                # Nested groups (hierarchical)
    "MetaData": { ... },
    "AttributeGroupLink": [ ... ]                # Group linking
}
```

---

#### **ListOfValues** (`parser.list_of_values`)
Enumeration value definitions with choice pattern.

**Dictionary Structure:**
```python
{
    "ID": "YesNoValues",                         # LOV ID
    "ParentID": "BooleanValues",                 # Parent LOV
    "AllowUserValueAddition": False,             # Boolean
    "UseValueID": True,                          # Boolean
    "IDPattern": "YN_*",                         # ID pattern
    "ReplaceListOfValuesValues": False,          # Boolean
    "DefaultUnitID": "NoUnit",                   # Unit reference
    "Name": "Yes/No Enumeration",                # Text
    "Validation": { ... },                       # Validation element
    "DimensionLink": [ ... ],                    # Dimension links
    "MetaData": { ... },
    "AttributeGroupLink": [ ... ],
    
    # Choice: Value elements XOR ValueGroup elements
    "Value": [                                   # Individual values
        {
            "ID": "Y",
            "UnitID": "NoUnit",
            "UnitName": "NoUnit",
            "AttributeID": "Status",
            "Changed": False,
            "Derived": False,
            "value": "Yes",                      # Text content
            "MetaData": { ... }
        }
    ],
    "ValueGroup": [                              # Value groups (for qualifiers)
        {
            "ID": "GroupEN",
            "AttributeID": "Status",
            "Inherited": False,
            "Changed": False,
            "Value": [ ... ]                     # Nested values
        }
    ],
    "DeleteValue": [                             # Deletion instructions
        {
            "Force": False,                      # Boolean
            "GenerateEvents": True,              # Boolean
            "value": "OldValue"                  # Value ID to delete
        }
    ]
}
```

---

### 3. System Configuration

#### **UserTypes** (`parser.user_types`)
Object type definitions (Products, Assets, Classifications, Entities).

**Dictionary Structure:**
```python
{
    "ID": "ProductType1",                        # Type ID
    "AllowOverlappingTerms": False,              # Boolean
    "AllowQuarkTemplate": False,                 # Boolean
    "AllowInDesignTemplate": False,              # Boolean
    "Revisability": "NonRevisionable",           # Enum
    "IsCategory": False,                         # Boolean
    "DefaultProfileConfiguration": "Default",   # Reference
    "ClassificationOwnsProductLinks": False,    # Boolean
    "NamePattern": "PROD_*",                     # Pattern
    "IDPattern": "ID_*",                         # Pattern
    "ManuallySorted": True,                      # Boolean
    "ReferenceTargetLockPolicy": "NoLock",       # Policy
    "Selected": True,                            # Boolean
    "Referenced": False,                         # Boolean
    "Changed": False,                            # Boolean
    "Deleted": False,                            # Boolean
    "Name": "Product Type 1",                    # Text
    "Icon": "base64_encoded_image",              # Base64
    "VisibleTermFields": { ... },
    "MetaData": { ... },
    "DimensionLink": [ ... ],                    # Dimension links
    "UserTypeLink": [ ... ],                     # Type constraints
    "AttributeLink": [ ... ],                    # Attribute assignments
    "Validation": { ... },
    "MIMEType": [ ... ]
}
```

---

#### **Contexts** (`parser.contexts`)
Multi-language and multi-dimensional contexts.

**Dictionary Structure:**
```python
{
    "ID": "en_US",                               # Context ID
    "Priority": "10",                            # Priority (string)
    "Locale": "en_US",                           # Language/locale
    "Selected": True,                            # Boolean
    "Referenced": False,                         # Boolean
    "Changed": False,                            # Boolean
    "Deleted": False,                            # Boolean
    "Name": "English (US)",                      # Text
    "DimensionPointLink": [                      # Multi-dimensional points
        {
            "DimensionID": "Market",
            "DimensionPointID": "US"
        }
    ]
}
```

---

#### **LinkTypes** (`parser.link_types`)
Relation type definitions (edge types).

**Dictionary Structure:**
```python
{
    "LinkTypeID": "CA"                           # Enumeration: CA or PA
}
# CA = Classification-to-Attribute
# PA = Product-to-Product
```

---

### 4. Deletion Operations

#### **DeleteProducts** (`parser.delete_products`)
Product deletion instructions.

**Dictionary Structure:**
```python
{
    "ID": "PROD_TO_DELETE",                      # Product ID to delete
    # Alternative identification
    "KeyValue": [
        {"KeyID": "legacyId", "value": "OLDID"}
    ]
}
```

#### **DeleteAssets** (`parser.delete_assets`)
Asset deletion instructions.

```python
{
    "ID": "ASSET_TO_DELETE",
    "KeyValue": [ ... ]
}
```

#### **DeleteClassifications** (`parser.delete_classifications`)
Classification deletion specifications.

```python
{
    "ID": "CAT_TO_DELETE",
    "Type": "All",                               # "All", "SubTypes", or "Values"
    "KeyValue": [ ... ]                          # Specific values to delete
}
```

#### **DeleteEntities** (`parser.delete_entities`)
Entity deletion instructions.

```python
{
    "ID": "ENTITY_TO_DELETE",
    "KeyValue": [ ... ]
}
```

---

### 5. Advanced Configuration (Phase 14)

#### **Keys** (`parser.keys`)
Unique identifier definitions.

**Dictionary Structure:**
```python
{
    "ID": "ProductKey",
    "State": "Active",                           # Enum: Inactive, PreInactive, ... Active, ... Deactivating
    "Selected": True,                            # Boolean
    "Referenced": False,                         # Boolean
    "Changed": False,                            # Boolean
    "Deleted": False,                            # Boolean
    "Name": "Product Key Definition",            # Text or list of dicts
    "KeyFormula": "PROD_{ProductID}",            # Formula (text)
    "MetaData": { ... },
    "UserTypeLink": [ ... ],                     # Type links
    "AttributeLink": [ ... ]                     # Attribute links
}
```

---

#### **BusinessLibraries** (`parser.business_libraries`)
Reusable business rule collections.

**Dictionary Structure:**
```python
{
    "ID": "ValidationRules",
    "Type": "Validation",                        # Type enum
    "RunPrivileged": True,                       # Boolean
    "Scope": "Global",                           # Scope enum
    "Selected": True,                            # Boolean
    "Referenced": False,                         # Boolean
    "Changed": False,                            # Boolean
    "Deleted": False,                            # Boolean
    "Name": "Validation Rule Library",
    "SetupGroupLink": { ... },                   # Link to setup group
    "Description": "Library description",        # Text
    "Dependencies": [                            # Library dependencies
        {
            "LibraryID": "BaseRules",
            "LibraryAlias": "base"
        }
    ],
    "MetaData": { ... }
}
```

---

#### **SetupGroups** (`parser.setup_groups`)
Hierarchical organization of setup components.

**Dictionary Structure:**
```python
{
    "ID": "SetupGroup1",
    "UserTypeID": "ProductType1",                # Type reference
    "ParentID": "RootSetup",                     # Parent group
    "Referenced": False,                         # Boolean
    "Selected": True,                            # Boolean
    "Changed": False,                            # Boolean
    "Name": "Setup Group 1",
    "MetaData": { ... },
    "SetupGroup": [                              # Nested groups (hierarchical)
        {
            "ID": "SetupGroup1_Sub",
            "Name": "Sub-Group",
            # ... recursive structure
        }
    ]
}
```

---

#### **IntegrationEndpoints** (`parser.integration_endpoints`)
Integration endpoint definitions with 3 variants.

**Dictionary Structure:**
```python
{
    "Type": "OutBound",                          # "OutBound", "InBound", or "Gateway"
    "ID": "ExportEndpoint1",                     # Endpoint ID
    "Name": "Export Integration",                # Text or list of dicts
    "MetaData": { ... }
}
```

---

### 6. Organizational Structure

#### **CrossReferenceTypes** (`parser.cross_reference_types`)
Relation type definitions.

```python
{
    "ID": "SupplierLink",
    "Name": "Supplier Link",                     # Text or list of dicts
    "MetaData": { ... }
}
```

---

#### **Qualifiers** (`parser.qualifiers`)
Multi-dimensional data qualifiers.

```python
{
    "ID": "RegionQualifier",
    "Name": "Region Qualifier",
    "DimensionPointLink": [                      # Links to dimension points
        {"DimensionID": "Region", "DimensionPointID": "EU"}
    ],
    "MetaData": { ... }
}
```

---

#### **Dimensions** (`parser.dimensions`)
Multi-dimensional data axes.

```python
{
    "ID": "Market",                              # Dimension ID
    "AllowDuplicates": False,                    # Boolean
    "Name": "Market Dimension",
    "DimensionPoint": [                          # Individual points
        {
            "ID": "US",
            "Name": "United States",
            "MetaData": { ... }
        }
    ],
    "MetaData": { ... }
}
```

---

#### **Tags** (`parser.tags`)
Flexible object categorization.

```python
{
    "ID": "HighValue",
    "Name": "High Value Product",
    "MetaData": { ... }
}
```

---

#### **Units** (`parser.units`)
Measurement unit definitions.

```python
{
    "ID": "Meter",
    "Name": "Meter",                             # Text
    "Symbol": "m",                               # Text
    "Formula": "1.0",                            # Text
    "MetaData": { ... }
}
```

---

### 7. Bulk Operations

#### **ReplacementRules** (`parser.replacement_rules`)
Bulk replacement operation rules (singleton dict, not list).

```python
{
    "ReplaceValues": [ ... ],
    "ReplaceCrossReferences": [ ... ],
    "ReplaceAttributeLinks": [ ... ],
    "ReplaceClassificationReferences": [ ... ]
}
```

---

#### **Collections** (`parser.collections`)
Data grouping elements with hierarchical support.

```python
{
    "ID": "ProductSet1",
    "ParentID": "AllCollections",
    "QueryURL": "/api/query?type=product",      # Optional search-based collections
    "Name": "Product Set 1",
    "Collection": [                              # Nested collections (hierarchical)
        {
            "ID": "ProductSet1_Sub",
            "Name": "Sub-Collection",
            # ... recursive structure
        }
    ],
    "MetaData": { ... }
}
```

---

### 8. Configuration Elements

#### **GlobalSettings** (`parser.global_settings`)
System-wide configuration (singleton dict, not list).

```python
{
    "CalculatedAttributeSettings": { ... },
    "AssetSettings": { ... }
}
```

---

#### **BulkUpdateConfigurations** (`parser.bulk_update_configurations`)
Bulk operation configurations.

```python
{
    "ID": "BulkUpdate1",
    "Name": "Bulk Update Config 1",
    "MetaData": { ... },
    "ClassificationReference": [ ... ],
    "Configuration": { ... }
}
```

---

## Data Structure Patterns

### Common Patterns Across All Element Types

#### **Name Elements**
Names can be:
1. **Simple text** (most elements): Returns string directly
2. **Multi-language list** (some elements): Returns list of dicts

```python
# Simple text (Products, Assets, etc.)
product["Name"] = "Product Name"

# Multi-language list (Contexts, etc.)
user_type["Name"] = [
    {"value": "Product Type", "Locale": "en_US"},
    {"value": "Type de produit", "Locale": "fr_FR"}
]
```

#### **Reference Patterns**
Single vs. Multiple references:
```python
# Single reference
product["AssetCrossReference"] = { "AssetID": "...", ... }

# Multiple references (returned as list)
product["ProductCrossReference"] = [
    { "ProductID": "COMP1", ... },
    { "ProductID": "COMP2", ... }
]
```

#### **Hierarchical Nesting**
Many element types support parent-child hierarchies:
```python
# Classifications with nested classifications
classification["Classification"] = [
    {
        "ID": "CAT_SUB",
        "Classification": [ ... ]  # Further nesting
    }
]
```

#### **Boolean Conversion**
All boolean attributes automatically converted from XML strings:
```python
# Input XML: Changed="true"
product["Changed"] = True          # Python bool

# Input XML: Changed="false"
product["Changed"] = False         # Python bool

# Missing attribute with default
product["Selected"] = True         # Default per element type
```

#### **MetaData Container**
Optional metadata present in most complex elements:
```python
product["MetaData"] = {
    "Attribute": [
        {
            "ID": "CustomField1",
            "Value": [
                {"value": "customValue", "QualifierID": "en_US"}
            ]
        }
    ]
}
```

---

## Usage Examples

### Example 1: Parse and List All Products

```python
from stepxmlclient.parser import Parser
import json

parser = Parser()
parser.parse_file('step_export.xml')

print(f"Total products: {len(parser.products)}")
for product in parser.products:
    print(f"  ID: {product['ID']}")
    print(f"  Name: {product['Name']}")
    print(f"  Parent: {product.get('ParentId', 'None')}")
    print()
```

### Example 2: Find Products with Asset References

```python
parser = Parser()
parser.parse_file('step_export.xml')

for product in parser.products:
    if 'AssetCrossReference' in product:
        asset_ref = product['AssetCrossReference']
        asset_id = asset_ref['AssetID']
        asset_type = asset_ref['Type']
        print(f"Product {product['ID']} has asset: {asset_id} ({asset_type})")
```

### Example 3: Access Multi-Language Context Data

```python
parser = Parser()
parser.parse_file('step_export.xml')

for user_type in parser.user_types:
    names = user_type['Name']
    print(f"UserType {user_type['ID']}:")
    
    # Names can be string or list of dicts
    if isinstance(names, list):
        for name_entry in names:
            locale = name_entry.get('Locale', 'default')
            value = name_entry['value']
            print(f"  [{locale}] {value}")
    else:
        print(f"  {names}")
```

### Example 4: Inspect Attribute Values for a Product

```python
parser = Parser()
parser.parse_file('step_export.xml')

if parser.products:
    product = parser.products[0]
    print(f"Product: {product['ID']}")
    
    if 'Values' in product:
        print("Attributes:")
        for value_entry in product['Values']:
            attr_id = value_entry['AttributeID']
            attr_value = value_entry['value']
            qualifier = value_entry.get('QualifierID', 'default')
            print(f"  {attr_id} [{qualifier}]: {attr_value}")
```

### Example 5: Handle Hierarchical Classifications

```python
def print_classification_tree(classification, indent=0):
    """Recursively print classification hierarchy."""
    name = classification['Name']
    print("  " * indent + f"- {name}")
    
    if 'Classification' in classification:
        for sub_class in classification['Classification']:
            print_classification_tree(sub_class, indent + 1)

parser = Parser()
parser.parse_file('step_export.xml')

for classification in parser.classifications:
    print_classification_tree(classification)
```

### Example 6: Check Deletion Instructions

```python
parser = Parser()
parser.parse_file('step_export.xml')

if parser.delete_products:
    print(f"Products to delete: {len(parser.delete_products)}")
    for del_prod in parser.delete_products:
        print(f"  - {del_prod['ID']}")

if parser.delete_classifications:
    print(f"Classifications to delete: {len(parser.delete_classifications)}")
    for del_class in parser.delete_classifications:
        delete_type = del_class['Type']  # "All", "SubTypes", or "Values"
        print(f"  - {del_class['ID']} (Type: {delete_type})")
```

### Example 7: Access Integration Endpoints

```python
parser = Parser()
parser.parse_file('step_export.xml')

print(f"Integration Endpoints: {len(parser.integration_endpoints)}")
for endpoint in parser.integration_endpoints:
    endpoint_type = endpoint['Type']  # OutBound, InBound, or Gateway
    print(f"  {endpoint['ID']} ({endpoint_type})")
```

---

## Performance Considerations

1. **Memory Usage**: Parser stores all parsed data in memory as lists/dicts
   - For large exports (1000+ items), consider batch processing
   - Use `parser.parse_file()` for file-based parsing (more memory efficient)

2. **Parsing Speed**: Dominated by XML ElementTree parsing
   - Namespace handling adds minimal overhead
   - Boolean conversion per attribute adds ~10% overhead

3. **Data Access**: Direct list/dict access is O(n)
   - For frequent lookups, build index: `by_id = {p['ID']: p for p in parser.products}`

---

## Common Issues & Solutions

### Issue: Name as List vs. String
**Problem**: Sometimes `Name` is a string, sometimes a list of dicts
**Solution**: Always check type before accessing
```python
name = product['Name']
if isinstance(name, list):
    values = [n['value'] for n in name]
else:
    values = [name]
```

### Issue: Missing Optional Fields
**Problem**: Optional attributes may not be in dict
**Solution**: Use `.get()` with defaults
```python
parent_id = product.get('ParentId', None)
changed = product.get('Changed', False)
```

### Issue: Boolean Attributes Not Converting
**Problem**: Boolean values still strings
**Solution**: Parser automatically converts all booleans - if this fails, file bug
```python
assert isinstance(product['Changed'], bool), "Boolean not converted"
```

### Issue: Reference Elements as Single or List
**Problem**: Single reference returns dict, multiple returns list
**Solution**: Normalize to list format
```python
refs = product.get('ProductCrossReference', [])
if isinstance(refs, dict):
    refs = [refs]
```

---

## Data Format Summary

| Element Type | Storage | Count | Structure |
|---|---|---|---|
| Products | List[dict] | Multiple | Parent-child hierarchy |
| Classifications | List[dict] | Multiple | Parent-child hierarchy |
| Entities | List[dict] | Multiple | Parent-child hierarchy, 20+ relations |
| Attributes | List[dict] | Multiple | Flat, no hierarchy |
| UserTypes | List[dict] | Multiple | Flat, no hierarchy |
| Contexts | List[dict] | Multiple | Flat (but dimensionally aware) |
| GlobalSettings | dict | Singleton | Single configuration object |
| ReplacementRules | dict | Singleton | Single ruleset object |
| Integration Endpoints | List[dict] | Multiple | 3 variants (OutBound/InBound/Gateway) |

---

## See Also

- [PARSER_STATUS.md](PARSER_STATUS.md) - Feature status and coverage
- [STEP.xsd](../STEP.xsd) - Authoritative STEP-XML schema (8500+ lines)
- Parser source: [stepxmlclient/parser.py](../stepxmlclient/parser.py)
- Tests: `test_parser_*.py` - Comprehensive usage examples
