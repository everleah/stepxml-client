#!/usr/bin/env python3
"""Roundtrip test for Creator Phases 1-7 implementation.

Tests creating XML documents with all supported entity types,
then parsing them back and validating consistency.

Coverage:
  Phase 1: Products, Assets, Relations, Deletions (10%)
  Phase 2: Classifications, Entities (15%)
  Phase 3: Attributes, Values, Groups (20%)
  Phase 4: Contexts, Qualifiers, Dimensions (25%)
  Phase 5: UserTypes, LinkTypes, Tags, Units (30%)
  Phase 6: BusinessRules, Workflows, Collections (35%)
  Phase 7: Replacement Rules (40%)
"""

import sys
from stepxmlclient.creator import Creator
from stepxmlclient.parser import Parser
from stepxmlclient.model import (
    Product, Asset, Classification, Entity,
    Attribute, AttributeGroup, ListOfValues,
    Context, Qualifier, Dimension, DimensionPoint,
    UserType, LinkType, Tag, TagGroup, Unit,
    BusinessRule, Workflow, Collection, CollectionGroup,
    ReplaceProducts, ReplaceValues, ReplaceCrossReferences,
    ReplaceClassifications, ReplaceEntities, ReplaceAssets,
)


def test_phase_1_core_entities():
    """Phase 1: Products, Assets, basic relations and deletions."""
    print("\n" + "="*70)
    print("PHASE 1: Core MDM Entities (Products, Assets)")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Create a product
    product = Product({"ID": "P001", "ParentId": None, "Name": "Laptop Computer"})
    creator.add(product)
    print(f"✓ Created Product: P001")
    
    # Create an asset
    asset = Asset({"ID": "A001", "Name": "Laptop Image"})
    creator.add(asset)
    print(f"✓ Created Asset: A001")
    
    # Link product to asset using the add_asset_reference method
    product.add_asset_reference("A001", "Image")
    print(f"✓ Linked Product to Asset")
    
    # Add product replacement rule
    replace_prod = ReplaceProducts()
    replace_prod.add_replace_values(attribute_id="Description")
    creator.replace_products.append(replace_prod)
    print(f"✓ Added product replacement rule")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Parse it back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - Products: {len(parser.products)}, Assets: {len(parser.assets)}")
    
    assert len(parser.products) == 1, "Expected 1 product"
    assert len(parser.assets) == 1, "Expected 1 asset"
    assert parser.products[0]["ID"] == "P001"
    assert parser.assets[0]["ID"] == "A001"
    print(f"✅ Phase 1: PASS")
    return True


def test_phase_2_hierarchies():
    """Phase 2: Classifications, Entities with nesting."""
    print("\n" + "="*70)
    print("PHASE 2: Hierarchical Organization (Classifications, Entities)")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Create classification hierarchy
    class1 = Classification({"ID": "C001", "Name": "Hardware"})
    class1.add_product_reference("P001")
    creator.add(class1)
    print(f"✓ Created Classification: C001")
    
    # Create nested classification
    class2 = Classification({"ID": "C002", "Name": "Accessories"})
    class1.add_nested_classification(class2)
    print(f"✓ Added nested Classification")
    
    # Create entity
    entity = Entity({"ID": "E001", "Name": "Supplier"})
    entity.add_product_reference("P001")
    creator.add(entity)
    print(f"✓ Created Entity: E001")
    
    # Add nested entity
    entity2 = Entity({"ID": "E002", "Name": "Distributor"})
    entity.add_nested_entity(entity2)
    print(f"✓ Added nested Entity")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Parse back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - Classifications: {len(parser.classifications)}, Entities: {len(parser.entities)}")
    
    assert len(parser.classifications) >= 1
    assert len(parser.entities) >= 1
    print(f"✅ Phase 2: PASS")
    return True


def test_phase_3_attributes():
    """Phase 3: Attributes with groups and values."""
    print("\n" + "="*70)
    print("PHASE 3: Attributes & Values (Attributes, Groups, ListOfValues)")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Create attribute
    attr = Attribute({"ID": "ATTR_001", "Type": "String", "Name": "Color"})
    creator.add(attr)
    print(f"✓ Created Attribute: ATTR_001")
    
    # Create attribute group
    attr_group = AttributeGroup({"ID": "AG_001", "Name": "Basic Info"})
    attr_group.add_nested_attribute_group(AttributeGroup({"ID": "AG_002", "Name": "Advanced"}))
    creator.add(attr_group)
    print(f"✓ Created AttributeGroup with nesting")
    
    # Create list of values
    lov = ListOfValues({"ID": "LOV_001", "Name": "Colors"})
    lov.add_value("Red")
    lov.add_value("Blue")
    lov.add_value("Green")
    creator.add(lov)
    print(f"✓ Created ListOfValues with 3 values")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Parse back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - Attributes: {len(parser.attributes)}, AttributeGroups: {len(parser.attribute_groups)}, "
          f"ListOfValues: {len(parser.list_of_values)}")
    
    assert len(parser.attributes) >= 1
    assert len(parser.attribute_groups) >= 1
    assert len(parser.list_of_values) >= 1
    print(f"✅ Phase 3: PASS")
    return True


def test_phase_4_organization():
    """Phase 4: Contexts, Qualifiers, Dimensions."""
    print("\n" + "="*70)
    print("PHASE 4: Multi-Dimensional Organization")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Create context
    ctx = Context({"ID": "CTX_001", "Name": "Region"})
    creator.add(ctx)
    print(f"✓ Created Context: CTX_001")
    
    # Create qualifier
    qual = Qualifier({"ID": "QUAL_001", "Name": "Channel"})
    creator.add(qual)
    print(f"✓ Created Qualifier: QUAL_001")
    
    # Create dimension with dimension points
    dim = Dimension({"ID": "DIM_001", "Name": "Geography"})
    dp1 = DimensionPoint({"ID": "DP_001", "Name": "North America"})
    dp2 = DimensionPoint({"ID": "DP_002", "Name": "Europe"})
    dim.add_dimension_point(dp1)
    dim.add_dimension_point(dp2)
    creator.add(dim)
    print(f"✓ Created Dimension with 2 DimensionPoints")
    
    # Link context to dimension points
    ctx.add_dimension_point_link("DIM_001", "DP_001")
    print(f"✓ Linked Context to DimensionPoint")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Parse back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - Contexts: {len(parser.contexts)}, Qualifiers: {len(parser.qualifiers)}, "
          f"Dimensions: {len(parser.dimensions)}")
    
    assert len(parser.contexts) >= 1
    assert len(parser.qualifiers) >= 1
    assert len(parser.dimensions) >= 1
    print(f"✅ Phase 4: PASS")
    return True


def test_phase_5_metadata():
    """Phase 5: UserTypes, LinkTypes, Tags, Units."""
    print("\n" + "="*70)
    print("PHASE 5: Metadata Definitions")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Create user type
    ut = UserType({"ID": "UT_001", "Name": "Product"})
    creator.add(ut)
    print(f"✓ Created UserType: UT_001")
    
    # Create link type
    lt = LinkType({"LinkTypeID": "LT_001", "Name": "RelatedTo"})
    creator.add(lt)
    print(f"✓ Created LinkType: LT_001")
    
    # Create tag with hierarchy
    tg = TagGroup({"ID": "TG_001", "Name": "Quality"})
    tag1 = Tag({"ID": "TAG_001", "Name": "High Quality"})
    tg.add_tag(tag1)
    creator.add(tg)
    print(f"✓ Created TagGroup with Tag")
    
    # Create unit
    unit = Unit({"ID": "UNIT_001", "Name": "Kilogram", "Symbol": "kg"})
    creator.add(unit)
    print(f"✓ Created Unit: UNIT_001")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Parse back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - UserTypes: {len(parser.user_types)}, LinkTypes: {len(parser.link_types)}, "
          f"Tags: {len(parser.tags)}, TagGroups: {len(parser.tag_groups)}, Units: {len(parser.units)}")
    
    assert len(parser.user_types) >= 1
    assert len(parser.link_types) >= 1
    assert len(parser.tag_groups) >= 1
    assert len(parser.units) >= 1
    print(f"✅ Phase 5: PASS")
    return True


def test_phase_6_business_logic():
    """Phase 6: BusinessRules, Workflows, Collections."""
    print("\n" + "="*70)
    print("PHASE 6: Business Logic & Collections")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Create business rule
    br = BusinessRule({"ID": "BR_001", "Type": "Action", "Name": "Validate Price"})
    creator.add(br)
    print(f"✓ Created BusinessRule: BR_001")
    
    # Create workflow
    wf = Workflow({"ID": "WF_001", "Name": "Approval Process"})
    wf.add_valid_user_type_link("UT_001")
    wf.add_business_rule_link("BR_001")
    creator.add(wf)
    print(f"✓ Created Workflow with links")
    
    # Create collection with hierarchy
    cg = CollectionGroup({"ID": "CG_001", "Name": "Products by Category"})
    col = Collection({"ID": "COL_001", "Name": "Electronics"})
    cg.add_collection(col)
    creator.add(cg)
    print(f"✓ Created CollectionGroup with Collection")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Parse back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - BusinessRules: {len(parser.business_rules)}, Workflows: {len(parser.workflows)}, "
          f"Collections: {len(parser.collections)}, CollectionGroups: {len(parser.collection_groups)}")
    
    assert len(parser.business_rules) >= 1
    assert len(parser.workflows) >= 1
    print(f"✅ Phase 6: PASS")
    return True


def test_phase_7_replacement_rules():
    """Phase 7: Replacement rules for bulk updates."""
    print("\n" + "="*70)
    print("PHASE 7: Replacement Rules for Bulk Updates")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Add product replacement rules
    replace_prod = ReplaceProducts()
    replace_prod.add_replace_values("ATTR_001", None, "GlobalContext")
    replace_prod.add_replace_cross_references("CrossRef_001", "GlobalContext")
    replace_prod.add_replace_attribute_links("ATTR_002")
    replace_prod.add_replace_classification_references()
    creator.replace_products.append(replace_prod)
    print(f"✓ Created ReplaceProducts with 4 instruction types")
    
    # Add classification replacement rules
    replace_class = ReplaceClassifications()
    replace_class.add_replace_values("ATTR_003")
    creator.replace_classifications.append(replace_class)
    print(f"✓ Created ReplaceClassifications")
    
    # Add entity replacement rules
    replace_entity = ReplaceEntities()
    replace_entity.add_replace_cross_references("CrossRef_002")
    creator.replace_entities.append(replace_entity)
    print(f"✓ Created ReplaceEntities")
    
    # Add asset replacement rules
    replace_asset = ReplaceAssets()
    replace_asset.add_replace_values("ATTR_004")
    creator.replace_assets.append(replace_asset)
    print(f"✓ Created ReplaceAssets")
    
    creator.build()
    xml_str = creator.to_string()
    print(f"✓ Generated XML ({len(xml_str)} bytes)")
    
    # Verify replacement rules section exists
    assert b'<ReplacementRules>' in creator.to_bytes()
    print(f"✓ ReplacementRules section present in XML")
    
    # Parse back
    parser = Parser()
    parser.parse_str(xml_str)
    print(f"✓ Parsed XML back")
    print(f"  - ReplacementRules parsed: {bool(parser.replacement_rules)}")
    
    print(f"✅ Phase 7: PASS")
    return True


def test_comprehensive_document():
    """Comprehensive test: Create document with entities from all phases."""
    print("\n" + "="*70)
    print("COMPREHENSIVE TEST: All Phases Combined")
    print("="*70)
    
    creator = Creator("GlobalContext", "Main")
    
    # Phase 1: Core
    product = Product({"ID": "PROD_001", "Name": "Smartphone"})
    asset = Asset({"ID": "ASSET_001", "Name": "Phone Image"})
    creator.add(product)
    creator.add(asset)
    product.add_asset_reference("ASSET_001", "Image")
    
    # Phase 2: Hierarchies
    classification = Classification({"ID": "CLASS_001", "Name": "Electronics"})
    entity = Entity({"ID": "ENTITY_001", "Name": "Manufacturer"})
    creator.add(classification)
    creator.add(entity)
    
    # Phase 3: Attributes
    attribute = Attribute({"ID": "ATTR_PRICE", "Type": "Decimal", "Name": "Price"})
    list_of_values = ListOfValues({"ID": "LOV_BRANDS", "Name": "Phone Brands"})
    creator.add(attribute)
    creator.add(list_of_values)
    
    # Phase 4: Organization
    context = Context({"ID": "CTX_REGION", "Name": "Region"})
    dimension = Dimension({"ID": "DIM_GEO", "Name": "Geography"})
    creator.add(context)
    creator.add(dimension)
    
    # Phase 5: Metadata
    user_type = UserType({"ID": "UT_PRODUCT", "Name": "Product"})
    tag_group = TagGroup({"ID": "TG_STATUS", "Name": "Status"})
    unit = Unit({"ID": "UNIT_CURRENCY", "Name": "USD"})
    creator.add(user_type)
    creator.add(tag_group)
    creator.add(unit)
    
    # Phase 6: Business
    workflow = Workflow({"ID": "WF_APPROVAL", "Name": "Product Approval"})
    collection = Collection({"ID": "COL_FEATURED", "Name": "Featured Products"})
    creator.add(workflow)
    creator.add(collection)
    
    # Phase 7: Replacements
    replace_rules = ReplaceProducts()
    replace_rules.add_replace_values(attribute_id="ATTR_PRICE")
    creator.replace_products.append(replace_rules)
    
    # Build and validate
    creator.build()
    xml_bytes = creator.to_bytes()
    xml_str = creator.to_string()
    
    print(f"✓ Created comprehensive document")
    print(f"  - Total XML size: {len(xml_bytes)} bytes")
    print(f"  - Products: 1, Assets: 1, Classifications: 1, Entities: 1")
    print(f"  - Attributes: 1, Contexts: 1, Dimensions: 1")
    print(f"  - UserTypes: 1, TagGroups: 1, Units: 1")
    print(f"  - Workflows: 1, Collections: 1")
    print(f"  - ReplacementRules: 1")
    
    # Parse it back
    parser = Parser()
    parser.parse_str(xml_str)
    
    print(f"✓ Parsed comprehensive document")
    print(f"  - Products: {len(parser.products)}")
    print(f"  - Assets: {len(parser.assets)}")
    print(f"  - Classifications: {len(parser.classifications)}")
    print(f"  - Entities: {len(parser.entities)}")
    print(f"  - Attributes: {len(parser.attributes)}")
    print(f"  - Contexts: {len(parser.contexts)}")
    print(f"  - Dimensions: {len(parser.dimensions)}")
    print(f"  - UserTypes: {len(parser.user_types)}")
    print(f"  - TagGroups: {len(parser.tag_groups)}")
    print(f"  - Units: {len(parser.units)}")
    print(f"  - Workflows: {len(parser.workflows)}")
    print(f"  - Collections: {len(parser.collections)}")
    
    # Basic validation
    assert len(parser.products) >= 1
    assert len(parser.assets) >= 1
    assert len(parser.classifications) >= 1
    
    print(f"✅ Comprehensive test: PASS")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("CREATOR ROUNDTRIP TEST SUITE - Phases 1-7 (40% coverage)")
    print("="*70)
    
    tests = [
        ("Phase 1: Core Entities", test_phase_1_core_entities),
        ("Phase 2: Hierarchies", test_phase_2_hierarchies),
        ("Phase 3: Attributes", test_phase_3_attributes),
        ("Phase 4: Organization", test_phase_4_organization),
        ("Phase 5: Metadata", test_phase_5_metadata),
        ("Phase 6: Business Logic", test_phase_6_business_logic),
        ("Phase 7: Replacement Rules", test_phase_7_replacement_rules),
        ("Comprehensive", test_comprehensive_document),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_name}: FAIL - {str(e)}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
