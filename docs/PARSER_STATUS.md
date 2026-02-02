# STEP XML Parser - Feature Status & Roadmap

**Last Updated:** February 2, 2026  
**Current Version:** Early Development (Phase 1)  
**Coverage:** ~5% of STEP-XML schema

---

## ✅ Currently Implemented

### Core Entity Parsing
- **Products** - Partial support
  - Attributes parsed: `ID`, `ParentId`, `UserTypeID`
  - Child text: `Name`
  - Child structures: `Values`
  - Relations parsed: `AssetCrossReference`, `DeleteAssetCrossReference` ✓
  - Relations NOT parsed: `ProductCrossReference`, `ClassificationReference`, `ClassificationCrossReference`, `EntityCrossReference` (see ❌ below)

- **Assets** - Partial support
  - Attributes parsed: `ID`
  - Child text: `Name`, `KeyValue`
  - Child structures: `Values`
  - Relations: None applicable to assets at top level

### Deletion Operations
- **DeleteAsset** - Fully supported
  - Attribute: `ID`
  - Alternative identification: `KeyValue`

- **DeleteProduct** - Fully supported
  - Attribute: `ID`
  - Alternative identification: `KeyValue`

### Attribute Values
- **Values** - Fully supported
  - Parse attribute-value pairs (AttributeID → value)
  - Support single-valued attributes
  - Support multi-valued attributes (MultiValue > Value elements)
  - Nested value structure with optional `ID` attributes

### Utility Functions
- **Parser class methods**
  - `parse_file(file_path)` - Parse from XML file
  - `parse_str(xml_str)` - Parse from XML string
  - `parse(root_element)` - Parse from ElementTree element
  
- **Internal helpers**
  - `_parse_item_list()` - Generic batch item parsing
  - `_parse_element()` - Flexible element parser with attributes/texts/specials
  - `_parse_value()` - Value element parser with ID attribute support
  - `_parse_values()` - Container parser for single/multi-valued attributes

---

## ✅ Fully Implemented

### Asset Cross-References (within Product)
- ✅ **AssetCrossReference** - Complete support
  - Attributes parsed: `AssetID`, `Changed`, `Type`, `QualifierID`
  - Type conversion: `Changed` → boolean with default `False`
  - Children parsed: `KeyValue` (multiple), `MetaData`

- ✅ **DeleteAssetCrossReference** - Complete support
  - Attributes parsed: `AssetID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

### Product Cross-References (Product-to-Product)
- ✅ **ProductCrossReference** - Complete support
  - Attributes parsed: `ProductID`, `Changed`, `Type`, `QualifierID`, `MountLocation`
  - Children parsed: `KeyValue` (multiple), `MetaData`

- ✅ **DeleteProductCrossReference** - Complete support
  - Attributes parsed: `ProductID`, `Changed`, `Type`, `QualifierID`, `MountLocation`
  - Children parsed: `KeyValue` (multiple), `MetaData`

### Classification References (Product-to-Classification)
- ✅ **ClassificationReference** - Complete support
  - Attributes parsed: `ClassificationID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

- ✅ **ClassificationCrossReference** - Complete support (same as ClassificationReference in parser)
  - Attributes parsed: `ClassificationID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

- ✅ **DeleteClassificationReference** - Complete support
  - Attributes parsed: `ClassificationID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

- ✅ **DeleteClassificationCrossReference** - Complete support
  - Attributes parsed: `ClassificationID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

### Entity Cross-References (Product-to-Entity)
- ✅ **EntityCrossReference** - Complete support
  - Attributes parsed: `EntityID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

- ✅ **DeleteEntityCrossReference** - Complete support
  - Attributes parsed: `EntityID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`

---

## ⚠️ Partially Implemented

## ❌ Not Yet Implemented

### Core Entity Types (High Priority)
- **Classifications** - Product categorization/hierarchy
  - ❌ NOT PARSED at all
  - Structure: Similar to Product but for classification hierarchies
  - Status: **High priority** - critical MDM entity

- **Entities** - Generic MDM objects
  - ❌ NOT PARSED at all
  - Structure: Like Products but more flexible for custom types
  - Status: **High priority** - flexible entity support

### Attribute System (High Priority)
- **Attributes** - Property definitions
  - ❌ NOT PARSED
  - Required for understanding attribute metadata
  - Status: **High priority** - foundational

- **AttributeGroups** - Attribute organization
  - ❌ NOT PARSED
  - Status: **High priority**

- **ListOfValues (LOVs)** - Enumerated values
  - ❌ NOT PARSED
  - Needed for understanding attribute valid values
  - Status: **High priority**

### Organizational Structure (Medium Priority)
- **Qualifiers & Dimensions**
  - ❌ NOT PARSED
  - QualifierID attributes in relations are present but not resolved
  - Status: **Medium priority** - needed for multi-dimensional data

- **Contexts** - Multi-dimensional data scoping
  - ❌ NOT PARSED
  - Status: **Medium priority**

- **UserTypes** - Entity type definitions
  - ❌ NOT PARSED
  - Status: **Medium priority**

- **CrossReferenceTypes** - Relation type definitions
  - ❌ NOT PARSED
  - Type IDs appear in relations but not resolved/validated
  - Status: **Medium priority** - understanding link semantics

### Suppressed Relations (Advanced)
- **SuppressedProductCrossReference**
  - NOT PARSED - Context-specific relation suppression
  - Status: **Lower priority** - advanced feature

- **SuppressedAssetCrossReference**, **SuppressedClassificationCrossReference**, **SuppressedEntityCrossReference**
  - NOT PARSED
  - Status: **Lower priority** - advanced feature

### Top-Level Collections (Lower Priority)
- **DeleteClassifications** - Classification deletions
  - ❌ NOT PARSED
  
- **DeleteEntities** - Entity deletions
  - ❌ NOT PARSED

- **ReplacementRules** - Bulk operation rules
  - ❌ NOT PARSED - Exists in creator but not handled in parser

- All other top-level structures (BusinessRules, EventQueues, PortalConfigurations, etc.)
  - ❌ NOT PARSED
  - Status: **Lower priority** - configuration elements

---

## Current Parser Architecture

### Class: `Parser`
```python
def __init__(self):
    self._tree = None
    self._root: Optional[ET.Element] = None
    self.products: List[dict] = []
    self.assets: List[dict] = []
    self.delete_products: List[dict] = []
    self.delete_assets: List[dict] = []
```

**State maintained:**
- Parse results stored as lists of dictionaries
- No object instantiation (raw dict output)
- Basic namespace handling via STEPXML_NS

### Parsing Pattern
Each entity type has a dedicated parser function:
```python
def _parse_<element_name>(element) -> dict:
    return _parse_element(
        element,
        attributes=[...],      # XML attributes to extract
        texts=[...],           # Simple text child elements
        specials={...},        # Complex children with custom parsers
        conversions={...}      # Type conversions (e.g., bool)
    )
```

**Conversion Pattern:**
```python
conversions = {
    "AttributeName": (conversion_function, default_value)
}
```
Example: `"Changed": (bool, False)` - converts to boolean, defaults to False

### Generic Helpers
- `_parse_element()` - Handles attributes, text children, special children, type conversions
- `_parse_leaf_element()` - Simple element with optional attributes and single text value
- `_parse_values()` - Specialized for attribute value containers
- `_parse_value()` - Individual value element parser
- `_parse_key_value()` - KeyValue element with KeyID and text value
- `_parse_metadata()` - MetaData container with nested attributes and values

### Cross-Reference Parsers
- `_parse_asset_reference()` - AssetCrossReference and DeleteAssetCrossReference
- `_parse_product_cross_reference()` - ProductCrossReference and DeleteProductCrossReference
- `_parse_classification_reference()` - ClassificationReference/CrossReference and Delete variants
- `_parse_entity_cross_reference()` - EntityCrossReference and DeleteEntityCrossReference

**All cross-reference parsers support:**
- Target ID attributes (AssetID, ProductID, ClassificationID, EntityID)
- Type (relation type)
- Changed (boolean flag)
- QualifierID (context/dimension)
- MountLocation (hierarchy positioning, ProductCrossReference only)
- KeyValue elements (multiple) for alternate identification
- MetaData child element with attribute values

---

## Known Limitations

1. **Output Format** - Parser returns raw dictionaries, not model objects
   - Requires additional conversion step to use with creator models
   - No type safety/validation

2. **Namespace Handling** - Uses fixed STEPXML_NS namespace dictionary
   - Works for standard STEP-XML but fragile for variants

3. **Attribute Conversions** - Limited type conversion support
   - Only boolean implemented
   - No numeric, date, or enumerated type conversions
   - No validation against AttributeList definitions

4. **Relation Resolution** - Relations are parsed but IDs not validated/resolved
   - ProductID/AssetID/ClassificationID/EntityID present but not cross-referenced
   - Type IDs not validated against CrossReferenceTypes
   - QualifierID context values present but context not resolved

5. **Multi-Language Support** - QualifierID context not handled
   - Relations may have QualifierID for language/region but not resolved to actual context
   - Values may be context-specific but treated as context-free

6. **Suppressed Relations** - Not distinguished from normal relations
   - Suppressed relations exist in XSD but would need separate parsing
   - SuppressedProductCrossReference, SuppressedAssetCrossReference, etc. not yet parsed

7. **No Validation** - Parser accepts any structure, no XSD validation
   - Malformed XML silently parsed as None/empty values
   - No error reporting mechanism

8. **Classification & Entity Parsing** - Not yet implemented
   - Classifications and Entities at top level not parsed
   - Relations within these entities not parsed
   - Planned for Phase 3

---

## Parsing Workflow

### Current Flow
```
XML File/String
    ↓
ElementTree parse
    ↓
Parser.parse(root)
    ↓
    ├─ parse Assets list → parser.assets (list of dict)
    ├─ parse Products list → parser.products (list of dict)
    ├─ parse DeleteAssets list → parser.delete_assets (list of dict)
    └─ parse DeleteProducts list → parser.delete_products (list of dict)
```

### Proposed Enhanced Flow (Future)
```
XML File/String
    ↓
ElementTree parse
    ↓
Parser.parse(root)
    ↓
    ├─ Assets → Asset model objects
    ├─ Products → Product model objects (with all relations)
    ├─ Classifications → Classification model objects
    ├─ Entities → Entity model objects
    ├─ DeleteAssets → deletion directives
    ├─ DeleteProducts → deletion directives
    ├─ DeleteClassifications → deletion directives
    └─ DeleteEntities → deletion directives
```

---

## Development Roadmap

### Phase 1 (Current - In Progress)
✅ **Completed:**
- Asset parsing (top-level)
- Product parsing (core attributes and values)
- Asset/Product deletion
- Generic value parsing
- Conversion framework
- Integration testing with real STEP-XML samples
- Parser error handling improvement

### Phase 2 (Completed - Just Now ✅)
✅ **Add Product Relations:**
- ✅ ProductCrossReference parser (`_parse_product_cross_reference`)
- ✅ DeleteProductCrossReference support
- ✅ ClassificationReference parser
- ✅ ClassificationCrossReference parser
- ✅ DeleteClassificationReference support
- ✅ EntityCrossReference parser
- ✅ DeleteEntityCrossReference support
- ✅ Updated `_parse_product()` to include all relation types
- ✅ Enhanced `_parse_asset_reference()` with KeyValue, MetaData, QualifierID, MountLocation
- ✅ New helper parsers: `_parse_key_value()`, `_parse_metadata()`

**Completed in:** Same session (2024)

### Phase 3 (Recommended Next - 1-2 weeks)
**Add Core Classification & Entity Support:**
- `_parse_classification()` function
- `_parse_entity()` function
- Top-level Classification list parsing
- Top-level Entity list parsing
- DeleteClassification/DeleteEntity support
- Classification-to-classification relations
- Entity-to-entity relations

**Estimated effort:** 3-4 days

### Phase 4 (Optional - 2-3 weeks after Phase 3)
**Add Attribute System Support:**
- `_parse_attribute()` for attribute definitions
- `_parse_list_of_value()` for LOV definitions
- `_parse_qualifier()` / `_parse_dimension()` for context
- Type conversion support for all attribute types
- Validation against AttributeList definitions

**Estimated effort:** 4-5 days

### Phase 5 (Optional - Extended)
**Add System Configuration Support:**
- Import/Export configurations
- Integration endpoints (OIEP/IIEP)
- BusinessRules, EventQueues
- UserTypes, LinkTypes, Keys
- Other setup elements

**Estimated effort:** 5+ days

---

## Testing Strategy

### Current Test Coverage
- `test.py` - Main integration test against demo STEP server
- `test_creator_xml.py` - Creator-focused XML generation tests
- `test_upload.py` - Upload functionality tests

### Completed Parser Test Recommendations (Phase 2)
```python
# ✅ Now ready to test:
def test_parse_product_cross_reference()
def test_parse_delete_product_cross_reference()
def test_parse_classification_reference()
def test_parse_entity_cross_reference()
def test_parse_key_value()
def test_parse_metadata()
def test_parse_asset_reference_with_metadata()
```

### Recommended Parser Test Additions (Phase 3+)
```python
# Phase 3 tests
def test_parse_classification()
def test_parse_entity()
def test_parse_delete_classification()

# Phase 4 tests
def test_parse_attribute()
def test_parse_list_of_value()
def test_type_conversions()
```

### Test Data Requirements
- Sample XML with ProductCrossReferences ✅ Can use CREATOR_USAGE.md examples
- Sample XML with Classifications and Entities (needed)
- Sample XML with nested structures (needed)
- Malformed XML for error handling tests (needed)

---

## Implementation Guidelines

### When Adding a Parser Function
1. Create function named `_parse_<element_name>(element)`
2. Use `_parse_element()` generic helper when possible
3. Add custom logic only for complex children (use `specials` parameter)
4. Include type conversions for non-string attributes
5. Test against actual STEP-XML examples
6. Add optional parameters for flexibility (e.g., allow skipping certain children)

### Conversion Functions
```python
def bool_converter(value: str) -> bool:
    return value.lower() in ('true', 'yes', '1', 'y')

# Used in conversions dict:
conversions = {
    "AttributeName": (bool_converter, False)  # (converter, default)
}
```

### Handling Unbounded Elements
For elements that can repeat (maxOccurs="unbounded"):
```python
# Option 1: Use findall() in custom parser
def _parse_my_list(element):
    results = []
    for child in element.findall('Item', STEPXML_NS):
        results.append(_parse_item(child))
    return results

# Option 2: Let _parse_element iterate via for child in element
# (elements are visited in order)
```

---

## Schema Reference
The complete STEP-XML specification is defined in [STEP.xsd](../STEP.xsd) (8500+ lines).
Use this as the authoritative reference for what fields should be parsed.

### Key Sections for Parser Development
- ProductType (line 5669) - Product structure
- AssetType (line 439) - Asset structure  
- ClassificationType (line 1719) - Classification structure
- EntityType (line 3711) - Entity structure
- ProductCrossReferenceType (line 5823) - Product-to-product relations
- Cross-reference types in general (lines 569-3210)

---

## Next Immediate Steps

1. **Test Phase 2 Implementation** ✅ Verify new parsers work with real samples
   - Test ProductCrossReference parsing
   - Test KeyValue and MetaData extraction
   - Test QualifierID and MountLocation handling
   
2. **Create Test Suite for Phase 2** - Add unit tests using CREATOR_USAGE.md examples
   - Parse generated XML from creator
   - Verify all attributes and children extracted
   - Round-trip test: creator → XML → parser → dict
   
3. **Parser → Model Conversion** - Create helper to convert dict output to model objects
   - Convert parsed dicts to Product/Asset model instances
   - Enable seamless integration with existing creator models
   
4. **Phase 3 Planning** - Prepare for Classifications and Entities parsing
   - Review STEP.xsd ClassificationType structure (line 1719)
   - Review STEP.xsd EntityType structure (line 3711)
   - Identify differences from ProductType parsing

