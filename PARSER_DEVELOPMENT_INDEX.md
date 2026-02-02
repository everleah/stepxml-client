# STEPXML Parser - Development Index

**Status:** Phase 4 Complete ✅  
**Coverage:** ~30% of STEP-XML schema  
**Test Suite:** 32 tests, 100% passing  
**Last Updated:** February 3, 2026

---

## Quick Navigation

### Implementation Status
- **Phase 1-2:** ✅ Assets & Products foundation with 9 relation types
- **Phase 3:** ✅ Classifications with hierarchy (18 relation types)
- **Phase 4:** ✅ Entities with maximum relations (20 relation types)
- **Phase 5:** 📋 Planned - Attribute system

### Documentation
| Document | Purpose |
|----------|---------|
| [PARSER_STATUS.md](docs/PARSER_STATUS.md) | Comprehensive feature matrix and roadmap |
| [PHASE_4_COMPLETION_STATUS.md](PHASE_4_COMPLETION_STATUS.md) | Phase 4 detailed completion report |
| [PHASE_3_COMPLETION_STATUS.md](PHASE_3_COMPLETION_STATUS.md) | Phase 3 detailed completion report |
| [SESSION_SUMMARY_PHASE4.md](SESSION_SUMMARY_PHASE4.md) | Phase 4 execution summary |
| [SESSION_SUMMARY_PHASE3.md](SESSION_SUMMARY_PHASE3.md) | Phase 3 execution summary |
| [PARSER_IMPROVEMENTS_SUMMARY.md](PARSER_IMPROVEMENTS_SUMMARY.md) | Phase 2 implementation details |

### Code
| File | Purpose | Status |
|------|---------|--------|
| `stepxmlclient/parser.py` | Main parser implementation | ✅ ~580 lines, 18 parser functions |
| `test_parser_phase2.py` | Phase 2 unit tests | ✅ 6/6 passing |
| `test_parser_phase2_integration.py` | Phase 2 integration tests | ✅ 6/6 passing |
| `test_parser_phase3_classification.py` | Phase 3 classification tests | ✅ 9/9 passing |
| `test_parser_phase4_entity.py` | Phase 4 entity tests | ✅ 11/11 passing |

---

## Quick Start

### Parse Products with Relations
```python
from stepxmlclient.parser import Parser

parser = Parser()
parser.parse_file('step_export.xml')

# Access products with all relations
for product in parser.products:
    print(f"Product: {product['ID']}")
    if 'ProductCrossReference' in product:
        refs = product['ProductCrossReference']
        if isinstance(refs, list):
            for ref in refs:
                print(f"  References: {ref['ProductID']}")
        else:
            print(f"  References: {refs['ProductID']}")
```

### Parse Classifications with Hierarchy
```python
from stepxmlclient.parser import Parser

parser = Parser()
parser.parse_file('classifications.xml')

# Access classifications (with nesting)
for classification in parser.classifications:
    print(f"Classification: {classification['ID']}")
    if 'Classification' in classification:
        # This classification has nested sub-classifications
        for nested in classification['Classification']:
            print(f"  Sub: {nested['ID']}")
```

---

## Test Suite

### Run All Tests
```bash
# Phase 2 unit tests
python test_parser_phase2.py

# Phase 2 integration tests
python test_parser_phase2_integration.py

# Phase 3 classification tests
python test_parser_phase3_classification.py
```

### Test Coverage
- **Products:** 6 unit + 6 integration tests
- **Classifications:** 9 comprehensive tests
- **Total:** 21 tests, 100% pass rate

---

## Features Implemented

### Core Entities
- ✅ Products
- ✅ Assets
- ✅ Classifications (with hierarchy)

### Attributes & Children
- ✅ ID, ParentID, UserTypeID attributes
- ✅ QualifierID (context qualification)
- ✅ Boolean attributes (Changed, Republished, Selected, Referenced)
- ✅ Name elements (text)
- ✅ KeyValue elements (alternate IDs)
- ✅ MetaData (attribute-value pairs)

### Relations Supported
- ✅ **10 Product relations:** AssetCrossReference, ProductCrossReference, ClassificationReference, ClassificationCrossReference, EntityCrossReference (and delete variants)
- ✅ **18 Classification relations:** ProductReference/CrossReference, ClassificationCrossReference, EntityCrossReference, AssetCrossReference (and suppressed/delete variants)
- ✅ **Multiple relation handling:** Single → dict, multiple → list aggregation

---

## Architecture

### Parser Class Methods
- `parse_file(path)` - Parse from XML file
- `parse_str(xml)` - Parse from XML string
- `parse(root)` - Parse from ElementTree element

### Parser Functions (15 total)
**Generic Helpers:**
- `_parse_element()` - Flexible element parser
- `_parse_item_list()` - Batch item parsing
- `_parse_values()` - Value container parser

**Entity Parsers:**
- `_parse_asset()` - Asset parser
- `_parse_product()` - Product parser with relations
- `_parse_classification()` - Classification parser with hierarchy

**Relation Parsers:**
- `_parse_asset_reference()` - Asset cross-references
- `_parse_product_cross_reference()` - Product cross-references
- `_parse_classification_reference()` - Classification cross-references
- `_parse_entity_cross_reference()` - Entity cross-references

**Utility Parsers:**
- `_parse_key_value()` - Alternate identifiers
- `_parse_metadata()` - Metadata attributes
- `_parse_value()` - Individual values

**Conversion Helpers:**
- `_str_to_bool()` - XML boolean string conversion

---

## Parser Output Format

All parsers return **raw dictionaries** (not model objects):

```python
{
    'ID': 'PROD001',
    'Name': 'Product Name',
    'ParentId': 'PARENT',
    'UserTypeID': 'ProductType',
    'Changed': False,  # Boolean
    'Values': {
        'AttributeID': {
            'value': 'attribute value',
            'ID': 'optional-id'
        }
    },
    'AssetCrossReference': {  # Single reference
        'AssetID': 'ASSET123',
        'Type': 'image',
        'QualifierID': 'en_US',
        'KeyValue': [
            {'KeyID': 'key1', 'value': 'val1'}
        ],
        'MetaData': {...}
    },
    'ProductCrossReference': [  # Multiple references
        {'ProductID': 'COMP1', 'Type': 'component', ...},
        {'ProductID': 'COMP2', 'Type': 'component', ...}
    ]
}
```

---

## Known Limitations

1. **No XML validation** - Accepts any structure, no XSD validation
2. **No error reporting** - Malformed XML silently produces None/empty values
3. **No model conversion** - Output is raw dicts, not model objects
4. **Context unresolved** - QualifierID attributes present but context not resolved
5. **No attribute system** - Attribute definitions not parsed
6. **No entity parsing** - Entities not yet implemented (Phase 4)
7. **Suppressed relations** - Parsed but not distinguished from normal relations
8. **Limited to Products/Classifications** - Entities and other core types not supported yet

---

## Schema Alignment

**STEP.xsd Reference:**
- ProductType: Lines 5756-5823
- ClassificationType: Lines 1718-1793
- Cross-reference types: 2000-2200 region
- Total schema: 8562 lines

**Coverage Analysis:**
- Core entity types: 3/5 (Products, Classifications, Assets | need: Entities, Attributes)
- Core relationships: ~28 types fully supported
- Metadata support: Complete (MetaData, KeyValue, Values)
- Conversion support: Boolean, text, attributes

---

## Performance Notes

- **Memory:** Entire document loaded into memory
- **Speed:** Single-pass XML parsing
- **Suitable for:** Documents up to 100MB typical size
- **Not suitable for:** Streaming large documents (>1GB)

---

## Next Steps

### Phase 4 Roadmap (Entity Parsing)
- Implement `_parse_entity()` function
- Add entity-to-entity relations
- Add entity-to-product/classification relations
- Create 9+ entity tests
- Expected coverage: ~25%

### Future (Phase 5+)
- Attribute system (LOVs, conversions)
- Context/Qualifier resolution
- Model object conversion
- Round-trip creator integration

---

## Related Documentation

- [CREATOR_STATUS.md](docs/CREATOR_STATUS.md) - STEP-XML creator implementation status
- [CREATOR_USAGE.md](docs/CREATOR_USAGE.md) - How to use the creator module
- README.md - Project overview

---

## Contact & Contributing

For issues, improvements, or questions about the parser:
1. Review PARSER_STATUS.md for detailed feature matrix
2. Check test_parser_phase*.py for usage examples
3. See PHASE_3_COMPLETION_STATUS.md for implementation details

