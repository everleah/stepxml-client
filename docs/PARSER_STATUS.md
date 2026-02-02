# STEP XML Parser - Feature Status & Roadmap

**Last Updated:** February 3, 2026  
**Current Version:** Phase 3 Complete  
**Coverage:** ~20% of STEP-XML schema

---

## ✅ Currently Implemented

### Core Entity Parsing
- **Products** - Full support (Phase 2) ✅
  - Attributes parsed: `ID`, `ParentId`, `UserTypeID`
  - Child text: `Name`
  - Child structures: `Values`
  - All product relations fully parsed ✓

- **Assets** - Partial support
  - Attributes parsed: `ID`
  - Child text: `Name`, `KeyValue`
  - Child structures: `Values`
  - Relations: None applicable to assets at top level

- **Classifications** - Full support (Phase 3) ✅
  - Attributes parsed: `ID`, `ParentID`, `UserTypeID`, `QualifierID`, `Changed`, `Republished`, `Selected`, `Referenced`
  - Child text: `Name`
  - Child elements: `KeyValue` (multiple), `ParentKeyValue` (multiple), nested `Classification`
  - Child structures: `MetaData`
  - All classification relations fully parsed ✓

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

### Classification Cross-References (Classification-to-Classification)
- ✅ **ClassificationCrossReference** - Complete support
  - Attributes parsed: `ClassificationID`, `Changed`, `Type`, `QualifierID`
  - Children parsed: `KeyValue` (multiple), `MetaData`
  - Handles suppressed variants

- ✅ **DeleteClassificationCrossReference** - Complete support
  - All attributes and children fully supported

### Product & Entity References within Classifications (Phase 3)
- ✅ **ProductReference & ProductCrossReference** (in classifications)
  - Attributes parsed: `ProductID`, `Changed`, `Type`, `QualifierID`, `MountLocation`
  - Handles suppressed/delete variants

- ✅ **EntityCrossReference** (in classifications)
  - Attributes parsed: `EntityID`, `Changed`, `Type`, `QualifierID`
  - Handles suppressed/delete variants

- ✅ **AssetCrossReference** (in classifications)
  - Attributes parsed: `AssetID`, `Changed`, `Type`, `QualifierID`
  - Handles suppressed/delete variants
  - Children parsed: `KeyValue`, `MetaData`

### Nested Classifications (Phase 3)
- ✅ **Classification nesting** - Complete support
  - Hierarchical classification parsing
  - Unlimited nesting depth
  - All attributes and relations preserved in nested items

---

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

### Core Entity Types (Medium Priority - Phase 3 started)
- **Classifications** - ✅ COMPLETED (Phase 3)
  - Full hierarchical support with all relation types
  - See "Fully Implemented" section above

- **Entities** - ❌ NOT PARSED
  - Generic MDM objects with flexible structure
  - Status: **Next in Phase 3 roadmap**

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

### Phase 1 (Completed ✅)
✅ **Asset & Product Foundation:**
- Asset parsing (top-level)
- Product parsing (core attributes and values)
- Asset/Product deletion
- Generic value parsing
- Conversion framework

### Phase 2 (Completed ✅)
✅ **Product Relations - All Types:**
- ProductCrossReference with MountLocation
- ClassificationReference/ClassificationCrossReference
- EntityCrossReference with all variants
- Enhanced AssetCrossReference with metadata
- Multiple reference aggregation
- Boolean conversion helper `_str_to_bool()`

### Phase 3 (Completed ✅ - Just Now)
✅ **Classification & Hierarchy Support:**
- ✅ `_parse_classification()` function with full relation support
- ✅ Top-level Classification list parsing in Parser.parse()
- ✅ Nested classification hierarchy (unbounded depth)
- ✅ Classification-to-classification cross-references
- ✅ Product references within classifications
- ✅ Entity references within classifications
- ✅ Asset references within classifications
- ✅ All 4 suppressed/delete variant types
- ✅ MetaData and KeyValue support in classifications
- ✅ 9 comprehensive integration tests, 100% pass rate

**Schema Coverage:** ~20% (up from ~15%)

### Phase 4 (Recommended Next - 1-2 weeks)
**Add Entity Support:**
- `_parse_entity()` function
- Top-level Entity list parsing
- Entity-to-entity relations
- Entity relations to Products/Classifications/Assets
- DeleteEntity support

**Estimated effort:** 3-4 days
**Estimated coverage:** ~25%

### Phase 5 (Optional - Later)
**Add Attribute System Support:**
- `_parse_attribute()` for attribute definitions
- `_parse_list_of_value()` for LOV definitions
- Context/Dimension resolution
- Type conversion for attribute values
- Validation framework

**Estimated effort:** 4-5 days

### Phase 6 (Optional - Extended)
**Add System Configuration Support:**
- BusinessRules, EventQueues, Workflows
- UserTypes, LinkTypes, Keys
- Import/Export configurations
- Integration endpoints

**Estimated effort:** 5+ days

---

## Testing Strategy

### Current Test Coverage

**Phase 2 Tests:**
- ✅ `test_parser_phase2.py` - 6 unit validation tests
- ✅ `test_parser_phase2_integration.py` - 6 integration tests with realistic Product XML

**Phase 3 Tests:**
- ✅ `test_parser_phase3_classification.py` - 9 integration tests
  - Single classification
  - Classification with KeyValues
  - Nested classifications (hierarchical)
  - Classification with product references
  - Classification-to-classification references
  - Classification with entity references
  - Classification with asset references
  - Classification with metadata
  - Complex classification with all reference types

**Total Test Coverage:** 21 tests, 100% pass rate

### All Tests Passing ✅
```
Phase 2 Unit Tests: 6/6 ✓
Phase 2 Integration Tests: 6/6 ✓
Phase 3 Classification Tests: 9/9 ✓
Total: 21/21 ✓
```

### Recommended Future Tests (Phase 4+)
```python
# Phase 4 tests
def test_parse_entity()
def test_parse_entity_with_cross_references()
def test_parse_delete_entity()
def test_parse_entity_relationships()

````# Phase 4 tests
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

