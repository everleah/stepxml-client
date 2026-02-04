# STEP XML Creator - Feature Status & Roadmap

**Last Updated:** February 4, 2026  
**Current Version:** Phase 1 Complete - Phase 2 Planning  
**Parser Coverage:** ~80% of STEP-XML schema  
**Creator Coverage:** ~10% of STEP-XML schema

---

## Executive Summary

The **Parser** has been extensively developed and now supports ~80% of STEP-XML entities, including:
- Core entities (Products, Assets, Classifications, Entities)
- Attributes system (Attributes, AttributeGroups, ListOfValues)
- Configuration elements (Contexts, Qualifiers, Dimensions, LinkTypes, UserTypes)
- Deletion operations and replacement rules
- Advanced features (Tags, Units, BusinessRules, Workflows)

The **Creator** currently supports only ~10% and focuses on the basic entities. This document outlines the **full expansion plan** to bring Creator coverage to match Parser capabilities.

---

## ✅ Currently Implemented in Creator

### Tier 1: Core Entities (Phase 1 - COMPLETE)

#### Product & Asset Management
- ✅ **Products**
  - Attributes: ID, ParentId, UserTypeID, Name
  - Values (attribute data)
  - All 4 cross-reference types (Asset, Product, Classification, Entity)
  - Both deletion types (full deletion + link severance)
  
- ✅ **Assets**
  - Attributes: ID, Name, KeyValue
  - Values (attribute data)
  - Product, Classification, Entity cross-references
  - Deletion operations

#### Relations
- ✅ **AssetCrossReference** - Product → Asset links
- ✅ **ProductCrossReference** - Product → Product links
- ✅ **ClassificationCrossReference** - Product/Asset → Classification
- ✅ **EntityCrossReference** - Product/Asset → Entity

#### Deletion Operations
- ✅ **DeleteAsset** - Top-level asset deletion
- ✅ **DeleteProduct** - Top-level product deletion
- ✅ **DeleteAssetCrossReference** - Link severance
- ✅ **DeleteProductCrossReference** - Link severance

#### Creator Infrastructure
- ✅ Document building (`build()`)
- ✅ Batch operations (`add()`, `add_list()`)
- ✅ XML export (`to_bytes()`, `to_string()`)
- ✅ Convenience methods for all relation types
- ✅ Dynamic class loading (`get_model_class()`)

---

## ⚠️ Parser-Ready Features (Ready for Creator Implementation)

### Tier 2: Classification & Entity Hierarchy (Parser Ready - Creator Needed)

#### Classifications
**Parser Status:** ✅ Full support including:
- Attributes: ID, ParentID, UserTypeID, QualifierID, Changed, Republished, Selected, Referenced
- Nested classifications (hierarchical)
- KeyValue and ParentKeyValue (alternate identification)
- All cross-reference types (Product, Classification, Entity, Asset)
- MetaData, AttributeLink, DataContainerTypeLink

**Creator Status:** ❌ Not implemented

**Implementation Notes:**
- Similar pattern to Product but with more complex attributes
- Support for hierarchical nesting
- Additional Boolean attributes (Changed, Republished, Selected, Referenced)

#### Entities
**Parser Status:** ✅ Full support including:
- Attributes: ID, ParentID, UserTypeID, QualifierID, Changed, Republished, Selected, Referenced
- Nested entities (hierarchical)
- KeyValue and ParentKeyValue
- All cross-reference types plus Context and Workspace
- Values, DataContainers, MetaData

**Creator Status:** ❌ Not implemented

**Implementation Notes:**
- Similar to Classification but supports Context/Workspace cross-references
- More flexible than Product for generic MDM objects

#### Deletion for Classifications & Entities
**Parser Status:** ✅ DeleteClassification, DeleteEntity, plus suppressed variants

**Creator Status:** ❌ Not implemented

### Tier 3: Attribute System (Parser Ready - Creator Needed)

#### Attributes Definition
**Parser Status:** ✅ Full attribute parsing including:
- AttributeID, DataType, QualifierID, Changed, Republished
- AttributeType, AttributeSequence, UserTypeLinks
- Default values, validation rules
- Multi-language support

**Creator Status:** ❌ Not implemented

#### AttributeGroups
**Parser Status:** ✅ Full support including:
- GroupID, QualifierID, Changed, Republished
- Nested groups (hierarchical)
- AttributeLinks
- Sequence information

**Creator Status:** ❌ Not implemented

#### List of Values (LOVs)
**Parser Status:** ✅ Full support including:
- LOVID, QualifierID, Type, Changed, Republished
- LOVItems with IDs and multi-language labels
- Hierarchical LOVs (ValueGroups)
- LOVValueGroups and nesting

**Creator Status:** ❌ Not implemented

**Dependency:** Required for defining attribute enumerations

### Tier 4: Organizational Structure (Parser Ready - Creator Needed)

#### Contexts
**Parser Status:** ✅ Full support including:
- ContextID, QualifierID, UserTypeID
- Qualifiers, Dimensions
- Description and metadata

**Creator Status:** ❌ Not implemented

#### Qualifiers
**Parser Status:** ✅ Full support including:
- QualifierID, QualifierType
- DimensionID references
- Description

**Creator Status:** ❌ Not implemented

#### Dimensions
**Parser Status:** ✅ Full support including:
- DimensionID, Required, HasDependencies
- DimensionPoints (hierarchy structure)

**Creator Status:** ❌ Not implemented

#### DimensionPoints
**Parser Status:** ✅ Full support including:
- PointID, ParentPointID
- QualifierID association
- Sequence and description

**Creator Status:** ❌ Not implemented

### Tier 5: Metadata & Configuration (Parser Ready - Creator Needed)

#### UserTypes
**Parser Status:** ✅ Full support including:
- UserTypeID, QualifierID, ParentUserTypeID
- AttributeLinks with mandatory/optional flags
- DataContainers, ValidUserTypes
- Nested UserTypes

**Creator Status:** ❌ Not implemented

#### LinkTypes
**Parser Status:** ✅ Full support including:
- LinkTypeID, QualifierID, Description
- Cardinality information
- Bidirectional link support

**Creator Status:** ❌ Not implemented

#### Tags & TagGroups
**Parser Status:** ✅ Full support including:
- TagID, TagGroupID, ParentTagID
- QualifierID, Changed flags
- Name and description

**Creator Status:** ❌ Not implemented

#### Units
**Parser Status:** ✅ Full support including:
- UnitID, ParentUnitID
- QualifierID, Symbol
- Conversion factors

**Creator Status:** ❌ Not implemented

### Tier 6: Business Logic & Workflow (Parser Ready - Creator Needed)

#### BusinessRules
**Parser Status:** ✅ Full support including:
- BusinessRuleID, QualifierID, Changed
- RuleType, Active flag
- Condition and Action logic

**Creator Status:** ❌ Not implemented

#### Workflows
**Parser Status:** ✅ Full support including:
- WorkflowID, Description
- StateflowInformation
- Approvals, Tasks, Permissions

**Creator Status:** ❌ Not implemented

#### EventQueues
**Parser Status:** ✅ Full support including:
- EventQueueID, Description
- Processors, Subscriptions
- Retry policies

**Creator Status:** ❌ Not implemented

### Tier 7: Replacement & Deletion Rules (Parser Ready - Creator Needed)

#### Replacement Rules (Advanced)
**Parser Status:** ✅ Full support including:
- ReplaceProducts, ReplaceClassifications, ReplaceEntities, ReplaceAssets
- ReplaceValues, ReplaceAttributeLinks, ReplaceCrossReferences
- ReplaceClassificationReferences, ReplaceUserTypeLinks

**Creator Status:** ⚠️ Partial - Only basic ProductReplacementRule

**Implementation Notes:**
- Extend replacement rule system to all entity types
- Expose all rule control options

#### Deletion Rules (Advanced)
**Parser Status:** ✅ Full deletion operations plus suppressed variants

**Creator Status:** ⚠️ Partial - Only basic Product/Asset deletion

### Tier 8: Collections (Parser Ready - Creator Needed)

#### Collections
**Parser Status:** ✅ Full support including:
- CollectionID, CollectionItemID
- Nested items, Groups
- Sequence information

**Creator Status:** ❌ Not implemented

#### CollectionGroups
**Parser Status:** ✅ Full support including:
- Nested collection structures
- Sequence and organization

**Creator Status:** ❌ Not implemented

### Tier 9: CrossReference Metadata (Parser Ready - Creator Needed)

#### CrossReferenceTypes
**Parser Status:** ✅ Full support including:
- CrossReferenceTypeID
- SourceType, TargetType
- Cardinality, Bidirectional flag

**Creator Status:** ❌ Not implemented

#### Context/Workspace Cross-References
**Parser Status:** ✅ Full support

**Creator Status:** ❌ Not implemented

---

## 📋 Implementation Roadmap

### Phase 2: Hierarchy Foundations (Recommended: Weeks 1-2)

**Priority 1 - Start Here:**
1. **Classification Model & Creator Support**
   - Create `stepxmlclient/model/classification.py`
   - Add to Creator collections
   - Implement convenience methods
   - Estimated: 2-3 days

2. **Entity Model & Creator Support**
   - Create `stepxmlclient/model/entity.py`
   - Add to Creator collections
   - Implement convenience methods
   - Estimated: 2-3 days

**Deliverables:**
- Classification and Entity objects can be created and exported to XML
- All relation types supported
- Deletion operations available

### Phase 3: Attribute System (Recommended: Weeks 3-4)

**Priority 2 - Enable Data Structure Definition:**
1. **Attribute Model & Creator**
   - Create `stepxmlclient/model/attribute.py`
   - Support for AttributeType, Validation, UserTypeLinks
   - Estimated: 2-3 days

2. **AttributeGroup Model & Creator**
   - Create `stepxmlclient/model/attribute_group.py`
   - Nested group support
   - Estimated: 1-2 days

3. **ListOfValues & LOVItem Models**
   - Create `stepxmlclient/model/list_of_values.py`
   - Hierarchical LOV support
   - Estimated: 2-3 days

**Deliverables:**
- Complete attribute definition system
- Enumerated values with multi-language support
- Attribute organization via groups

### Phase 4: Organization & Configuration (Recommended: Weeks 5-6)

**Priority 3 - Enable Multi-Dimensional Data:**
1. **Context, Qualifier, Dimension Models**
   - Create `stepxmlclient/model/organization.py`
   - Dimensional data framework
   - Estimated: 2-3 days

2. **UserType, LinkType Models**
   - Create `stepxmlclient/model/metadata.py`
   - Type system implementation
   - Estimated: 1-2 days

3. **Tag, Unit Models**
   - Add to metadata module
   - Estimated: 1 day

**Deliverables:**
- Multi-dimensional product information
- Type governance system
- Organizational hierarchy

### Phase 5: Advanced Features (Weeks 7-8)

**Priority 4 - Extended Capabilities:**
1. **BusinessRule, Workflow, EventQueue Models**
   - Create `stepxmlclient/model/business.py`
   - Automation framework
   - Estimated: 3-4 days

2. **Collection Model**
   - Create `stepxmlclient/model/collection.py`
   - Hierarchical grouping
   - Estimated: 1-2 days

3. **Advanced Replacement Rules**
   - Extend replacement rule system
   - Full rule control options
   - Estimated: 1-2 days

**Deliverables:**
- Business logic definition
- Product grouping/collections
- Advanced bulk operation control

### Phase 6: Completion & Validation (Week 9+)

**Priority 5 - Polish & Testing:**
1. Enhanced parser-creator roundtrip testing
2. Schema validation against STEP.xsd
3. Performance optimization
4. Documentation updates

---

## Architecture for Phase 2+ Implementation

### Model Organization
```
stepxmlclient/model/
├── __init__.py                    (Updated: add new classes)
├── product.py                     ✅ (Already done)
├── asset.py                       ✅ (Already done)
├── relations.py                   ✅ (Already done)
├── deletion.py                    ✅ (Already done)
├── classification.py              📋 (Phase 2)
├── entity.py                      📋 (Phase 2)
├── attribute.py                   📋 (Phase 3)
├── attribute_group.py             📋 (Phase 3)
├── list_of_values.py              📋 (Phase 3)
├── organization.py                📋 (Phase 4)
│   ├── Context
│   ├── Qualifier
│   └── Dimension
├── metadata.py                    📋 (Phase 4)
│   ├── UserType
│   ├── LinkType
│   ├── Tag
│   └── Unit
├── business.py                    📋 (Phase 5)
│   ├── BusinessRule
│   ├── Workflow
│   └── EventQueue
└── collection.py                  📋 (Phase 5)
```

### Creator Extension Pattern

Each new model tier adds:
1. **New collection attribute** in Creator.__init__()
   ```python
   self.classifications: List[BaseObject] = []
   self.entities: List[BaseObject] = []
   ```

2. **Element mapping** in Creator.build()
   ```python
   element_mapping = {
       "Classifications": "classifications",
       "Entities": "entities",
       ...
   }
   ```

3. **Model classes** with:
   - Proper `_GROUP_NAME` and `_TAG_NAME`
   - All `_ATTRIBUTE_NAMES`, `_TEXT_NAMES`, `_CHILDREN_NAMES`
   - Convenience methods for common child operations

---

## Parser-Creator Alignment Status

| Entity Type | Parser | Creator | Gap | Priority |
|---|---|---|---|---|
| Product | ✅ 100% | ✅ 100% | 0% | Complete |
| Asset | ✅ 100% | ✅ 100% | 0% | Complete |
| Classification | ✅ 100% | ❌ 0% | 100% | P1 |
| Entity | ✅ 100% | ❌ 0% | 100% | P1 |
| Attribute | ✅ 100% | ❌ 0% | 100% | P2 |
| AttributeGroup | ✅ 100% | ❌ 0% | 100% | P2 |
| ListOfValues | ✅ 100% | ❌ 0% | 100% | P2 |
| Context | ✅ 100% | ❌ 0% | 100% | P3 |
| Qualifier | ✅ 100% | ❌ 0% | 100% | P3 |
| Dimension | ✅ 100% | ❌ 0% | 100% | P3 |
| UserType | ✅ 100% | ❌ 0% | 100% | P3 |
| LinkType | ✅ 100% | ❌ 0% | 100% | P3 |
| Tag | ✅ 100% | ❌ 0% | 100% | P3 |
| Unit | ✅ 100% | ❌ 0% | 100% | P3 |
| BusinessRule | ✅ 100% | ❌ 0% | 100% | P4 |
| Workflow | ✅ 100% | ❌ 0% | 100% | P4 |
| EventQueue | ✅ 100% | ❌ 0% | 100% | P4 |
| Collection | ✅ 100% | ❌ 0% | 100% | P4 |
| CrossReferenceType | ✅ 100% | ❌ 0% | 100% | P4 |
| Advanced Replacement Rules | ✅ 100% | ⚠️ 10% | 90% | P4 |

**Overall Gap:** 70% of parser capabilities not yet in Creator

---

## Development Guidelines

### When Implementing New Entities

1. **Study the Parser Function**
   - Examine `_parse_<entity>()` in parser.py
   - Note all attributes, child elements, special handling
   - Identify conversion functions needed

2. **Create Model Class**
   ```python
   class MyEntity(BaseObject):
       _GROUP_NAME: str = 'my_entities'
       _TAG_NAME: str = 'MyEntity'
       _ATTRIBUTE_NAMES: List[str] = [...]
       _TEXT_NAMES: List[str] = [...]
       _CHILDREN_NAMES: List[str] = [...]
       
       def __init__(self, data: Dict[str, Any]) -> None:
           super().__init__(data)
           # Initialize child lists
   ```

3. **Add Convenience Methods**
   - Follow Product/Asset pattern
   - Support both parameter and object styles
   - Document with docstrings

4. **Update Creator**
   - Add collection in `__init__()`
   - Add element mapping in `build()`
   - Update `get_model_class()` registry

5. **Add Parser Function**
   - Already exists! Just ensure Creator can consume it

6. **Test Roundtrip**
   - Create → to_string() → Parser → verify

---

## Known Constraints & Considerations

1. **Hierarchical Entities** - Classification, Entity, Dimension support nesting
   - Special handling needed in `_add_children()`
   - Recursive structures

2. **Multi-Language Support** - Qualifier-based variant values
   - Different QualifierID = different language/context
   - Parser already handles; Creator should preserve

3. **Suppressed Variants** - Suppressed references with special handling
   - Parser supports; Creator framework handles generically
   - May need explicit class variants if special behavior needed

4. **Boolean Conversions** - Changed, Republished, Selected, Referenced flags
   - Parser uses `_str_to_bool()`
   - Creator should auto-convert Python bool → string

5. **KeyValue/ParentKeyValue** - Alternate identification systems
   - Multiple values per entity
   - Already supported by Product pattern

---

## Testing Strategy

### Unit Tests
- Each new model class
- Convenience method calls
- XML generation correctness

### Integration Tests
- Add to Creator → build() → to_string()
- Parse output back with Parser
- Roundtrip equality (data in == data out)

### Schema Validation
- Generated XML against STEP.xsd
- Use xmllint or similar validator

---

## Success Criteria

✅ **Phase 2 Success:**
- Classifications and Entities fully creatable
- All relation types work with both
- Deletion operations supported
- Creator coverage: ~20%

✅ **Phase 3 Success:**
- Attribute system complete
- LOVs with hierarchies
- Creator coverage: ~35%

✅ **Phase 4 Success:**
- Multi-dimensional framework
- Type governance
- Creator coverage: ~55%

✅ **Phase 5 Success:**
- Business logic framework
- Collections support
- Creator coverage: ~75%

✅ **Phase 6 Success:**
- 100% roundtrip compatibility with Parser
- Schema validation passing
- Creator coverage: ~80%

---

## References

- [STEP.xsd](../STEP.xsd) - Schema authority
- [Parser Implementation](../stepxmlclient/parser.py) - Parser reference
- [Current Creator](../stepxmlclient/creator.py) - Creator pattern
- [Product Model](../stepxmlclient/model/product.py) - Implementation example
- [CREATOR_USAGE.md](./CREATOR_USAGE.md) - Usage documentation
