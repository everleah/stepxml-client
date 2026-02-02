# STEP XML Creator - Feature Status & Roadmap

**Last Updated:** February 2, 2026  
**Current Version:** Early Development (Phase 1)  
**Coverage:** ~10% of STEP-XML schema

---

## ✅ Currently Implemented

### Core Entity Types
- **Products** - Full support
  - Attributes: ID, ParentId, UserTypeID, Name
  - Values (attribute data)
  - Cross-references (see Relations below)
  - Replacement rules for bulk operations
- **Assets** - Full support
  - Attributes: ID, Name, KeyValue
  - Values (attribute data)
  - Cross-references (see Relations below)

### Relations (Cross-References)
- **AssetCrossReference** - Link products to assets
  - Attributes: AssetID, Type, QualifierID
  - Optional metadata and key-value pairs
- **ProductCrossReference** - Link products to other products
  - Attributes: ProductID, Type, QualifierID, MountLocation
  - Parent/child hierarchies, related products, bundles
- **ClassificationCrossReference** - Link to classifications
  - Attributes: ClassificationID, Type, QualifierID, MountLocation
- **EntityCrossReference** - Link to generic entities
  - Attributes: EntityID, Type, QualifierID, MountLocation

### Deletion Operations
- **Top-Level Deletion Structures**
  - `DeleteAsset` - Move asset to recycle bin
  - `DeleteProduct` - Move product to recycle bin
  - Both support KeyValue for alternate identification

- **Link Severance (Relation Deletion)**
  - `DeleteAssetCrossReference` - Remove asset link from product
  - `DeleteProductCrossReference` - Remove product link from product
  - Both preserve parent object while severing relationship
  - Support Type, QualifierID, MountLocation attributes
  - Metadata tracking (Changed flag)

### Creator Capabilities
- **Document Structure**
  - STEP-ProductInformation root element
  - ContextID and WorkspaceID attributes
  - Automatic XML tree building
  
- **Builder Pattern**
  - `creator.add()` - Add individual objects
  - `creator.add_list()` - Batch add objects
  - `creator.build()` - Generate XML structure
  - `creator.to_bytes()` / `creator.to_string()` - Export as XML

- **Convenience Methods** (on Product and Asset)
  - `add_asset_reference()` - Fluent API for asset links
  - `add_product_reference()` - Product-to-product links
  - `delete_asset_reference()` - Sever asset links
  - `delete_product_reference()` - Sever product links

---

## ⚠️ Partially Implemented

### Product Replacement Rules
- ✅ Created and added to XML
- ⚠️ Limited to just `Values` child elements
- ❌ Full replacement rule control (ReplaceValues, ReplaceAttributeLinks, etc.) not exposed

---

## ❌ Not Yet Implemented

### Core Entity Types (High Priority)
- **Classifications** - Product categorization
  - Hierarchy structures
  - Classification-to-product mappings
  - Classification attributes and values
- **Entities** - Generic MDM objects
  - Flexible attribute systems
  - Entity-to-entity relations
  - Dynamic object types

### Attribute System (High Priority)
- **Attributes** - Property definitions
  - Type system (text, number, date, etc.)
  - Validation rules
  - Multi-language support
  - User type restrictions
- **AttributeGroups** - Logical attribute organization
  - Group hierarchy
  - UI/form layouts
- **ListOfValues (LOVs)** - Enumerated values
  - Controlled vocabularies
  - Multi-language labels
  - Hierarchical LOVs

### Organizational Structure (High Priority)
- **Qualifiers & Dimensions** - Multi-dimensional data
  - Language dimensions
  - Market/region dimensions
  - Channel dimensions
  - Context-based data filtering
- **Contexts** - Workspace segmentation
  - Qualifier combinations
  - Attribute value scoping
- **UserTypes** - Entity type definitions
  - Type restrictions
  - Inheritance

### Link & Relationship Management (Medium Priority)
- **LinkTypes** - Define relationship semantics
  - Parent/child vs. related vs. bundled, etc.
  - Link direction and cardinality
  - Link-specific attributes
- **Keys** - Unique product/entity identifiers
  - Multi-key definitions
  - Key formula support
- **Product & Classification References**
  - ReferenceType definitions
  - Reference-specific attributes

### Configuration Elements (Medium Priority)
- **BusinessRules** - Logic enforcement
  - Validation rules
  - Derived attributes
  - Workflow automation
- **SetupGroups & SetupEntities** - Metadata definitions
- **Users & UserGroups** - Access management
- **ActionSets** - Workflow automation definitions

### System Setup (Lower Priority)
- **GlobalSettings** - System-wide configuration
- **TagGroups & Tags** - Metadata tags
- **DimensionList** - Dimension configuration
- **Collections** - Product groupings
- **Units** - Measurement units
- **StatusFlags** - State management
- **MatchCodes** - Duplicate detection
- **MatchingAlgorithms** - Record matching logic
- **EdgeTypes** - Network relationship types

### Integration & Advanced Features (Lower Priority)
- **ImportConfigurations** - Data import setups
- **ExportConfigurations** - Data export setups
- **IntegrationEndpoints** - OIEP/IIEP definitions
- **EventQueues & EventProcessors** - Event handling
- **AssetPushConfigurations** - Asset distribution
- **PortalConfigurations** - Portal/ecommerce setup
- **ChangePackages** - Change tracking

---

## Development Roadmap

### Phase 1 (Current - In Progress)
✅ **Completed:**
- Products & Assets core
- Asset/Product/Classification/Entity cross-references
- Deletion structures (top-level and link-level)
- Creator document builder

🔄 **In Progress:**
- Parser support for relations and deletions
- Integration tests

### Phase 2 (Recommended Next)
**Estimated: Q1 2026**
- Classifications entity model and parser
- Attributes + ListOfValues system
- Qualifiers & Dimensions framework
- Enhanced product replacement rules

### Phase 3 (Suggested)
**Estimated: Q2 2026**
- Entities (generic MDM objects)
- UserTypes and type system
- LinkTypes relationship definitions
- Keys identifier system

### Phase 4 (Optional)
**Estimated: Q3 2026+**
- BusinessRules, workflows
- Import/Export configurations
- Integration endpoint definitions
- System setup elements

---

## Architecture Notes

### Model Pattern
All entity models follow this pattern:
```python
class MyEntity(BaseObject):
    _GROUP_NAME: str = 'collection_name'  # Creator list attribute
    _TAG_NAME: str = 'XMLElementName'     # XML tag
    _ATTRIBUTE_NAMES: List[str] = [...]   # XML attributes
    _TEXT_NAMES: List[str] = [...]        # Simple text children
    _CHILDREN_NAMES: List[str] = [...]    # Complex children
```

**Relation/Deletion Pattern:**
```python
class ChildRelation(BaseObject):
    _GROUP_NAME: Optional[str] = None     # Not added to Creator directly
    # ... used as children within parent objects
```

### Parser Pattern
Parser functions follow naming convention: `_parse_<element_name>()`

### Creator Pattern
- Top-level objects (with `_GROUP_NAME != None`) → Added via `creator.add()`
- Child objects (with `_GROUP_NAME = None`) → Added via convenience methods on parents
- Replacement rules → Separate list in Creator

---

## Schema Reference
The complete STEP-XML specification is defined in [STEP.xsd](../STEP.xsd) (8500+ lines).
Use this as the authoritative reference for extending the client with new entity types.

---

## Implementation Guidelines for Future Developers

### When Adding a New Entity:
1. Create model class in `stepxmlclient/model/`
2. Define `_GROUP_NAME`, `_TAG_NAME`, `_ATTRIBUTE_NAMES`, `_TEXT_NAMES`, `_CHILDREN_NAMES`
3. Add parser function in `stepxmlclient/parser.py` (if parsing is needed)
4. Add convenience methods on parent classes for common child relationships
5. Export from `stepxmlclient/model/__init__.py`
6. Update Creator if it's a top-level collection
7. Add tests to verify XML generation and parsing

### Entity Complexity Levels:
- **Simple:** Attributes only (Keys, Units) - 1-2 days
- **Moderate:** Attributes + children (Attributes, ListOfValues) - 2-3 days
- **Complex:** Full relations + children (Classifications, Entities) - 4-5 days
- **Very Complex:** Multi-layer nesting + rules (BusinessRules) - 5+ days

---

## Known Limitations

1. **Parser Support** - Currently limited to Products, Assets, and basic deletions
2. **Replacement Rules** - Only basic Values support; advanced rule controls missing
3. **Multi-value Handling** - Values support basic structures; complex multi-language variants need work
4. **Metadata** - MetaData elements accepted but not actively processed
5. **Validation** - No built-in validation against STEP.xsd schema
6. **Type Conversion** - Limited automatic type conversions for attribute values

---

## Contributing

When extending this client:
1. Follow the established model/parser/creator patterns
2. Use `Optional[str]` for nullable `_GROUP_NAME` fields
3. Add convenience methods for common parent-child operations
4. Keep model classes focused on XML serialization/deserialization
5. Use parser functions for XML input processing
6. Reference STEP.xsd for accurate schema compliance
