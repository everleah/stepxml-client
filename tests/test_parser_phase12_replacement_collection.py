"""
Phase 12: Replacement Rules and Collections Parsing Tests

Tests for:
- ReplacementRules (bulk operation rules for Products, Classifications, Entities, Assets, Attributes)
- Collections and CollectionGroups (data grouping elements)
"""

import pytest
from stepxmlclient.parser import Parser


class TestParseReplacementRules:
    """Test parsing of replacement rules for various entity types."""
    
    def test_parse_replacement_rules_minimal(self):
        """Test parsing empty ReplacementRules."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.replacement_rules, dict)
        assert len(parser.replacement_rules) == 0
    
    def test_parse_replacement_rules_with_products(self):
        """Test parsing ReplacementRules with Products element."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products/>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Products" in parser.replacement_rules
        assert isinstance(parser.replacement_rules["Products"], list)
    
    def test_parse_replacement_rules_with_multiple_products(self):
        """Test parsing ReplacementRules with multiple Products elements."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products/>
                <Products/>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Products" in parser.replacement_rules
        assert len(parser.replacement_rules["Products"]) == 2
    
    def test_parse_replacement_rules_with_replace_values(self):
        """Test parsing ReplaceValues within Products."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products>
                    <ReplaceValues AttributeID="Description" ContextID="DefaultContext"/>
                </Products>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Products" in parser.replacement_rules
        products = parser.replacement_rules["Products"][0]
        assert "ReplaceValues" in products
        assert products["ReplaceValues"][0]["AttributeID"] == "Description"
        assert products["ReplaceValues"][0]["ContextID"] == "DefaultContext"
    
    def test_parse_replacement_rules_with_replace_cross_references(self):
        """Test parsing ReplaceCrossReferences within Products."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products>
                    <ReplaceCrossReferences CrossReferenceID="ProductRelated" ContextID="DefaultContext"/>
                </Products>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        products = parser.replacement_rules["Products"][0]
        assert "ReplaceCrossReferences" in products
        assert products["ReplaceCrossReferences"][0]["CrossReferenceID"] == "ProductRelated"
    
    def test_parse_replacement_rules_with_classifications(self):
        """Test parsing ReplacementRules with Classifications."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Classifications>
                    <ReplaceValues AttributeGroupID="BasicInfo"/>
                </Classifications>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Classifications" in parser.replacement_rules
        classifications = parser.replacement_rules["Classifications"][0]
        assert "ReplaceValues" in classifications
    
    def test_parse_replacement_rules_with_entities(self):
        """Test parsing ReplacementRules with Entities."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Entities>
                    <ReplaceValues AttributeID="EntityName"/>
                </Entities>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Entities" in parser.replacement_rules
    
    def test_parse_replacement_rules_with_assets(self):
        """Test parsing ReplacementRules with Assets."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Assets>
                    <ReplaceValues AttributeID="AssetName"/>
                </Assets>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Assets" in parser.replacement_rules
    
    def test_parse_replacement_rules_with_attributes(self):
        """Test parsing ReplacementRules with Attributes."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Attributes/>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Attributes" in parser.replacement_rules


class TestParseCollections:
    """Test parsing of collections and collection groups."""
    
    def test_parse_collections_minimal(self):
        """Test parsing empty CollectionList."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.collections, list)
        assert isinstance(parser.collection_groups, list)
        assert len(parser.collections) == 0
        assert len(parser.collection_groups) == 0
    
    def test_parse_single_collection(self):
        """Test parsing single collection."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001"/>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.collections) == 1
        assert parser.collections[0]["ID"] == "COLL001"
    
    def test_parse_collection_with_name(self):
        """Test parsing collection with Name element."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>My Collection</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        collection = parser.collections[0]
        assert collection["ID"] == "COLL001"
        assert "Name" in collection
        assert len(collection["Name"]) == 1
        assert collection["Name"][0]["value"] == "My Collection"
    
    def test_parse_collection_with_multiple_names(self):
        """Test parsing collection with multiple Name elements (multi-language)."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>English Name</Name>
                    <Name>French Name</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        collection = parser.collections[0]
        assert len(collection["Name"]) == 2
    
    def test_parse_collection_with_parent_id(self):
        """Test parsing collection with ParentID for hierarchy."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001" ParentID="PARENT001">
                    <Name>Child Collection</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        collection = parser.collections[0]
        assert collection["ParentID"] == "PARENT001"
    
    def test_parse_collection_with_query_url(self):
        """Test parsing collection with QueryURL for search-based collections."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001" QueryURL="search?type=Product&amp;status=Active">
                    <Name>Active Products</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        collection = parser.collections[0]
        assert collection["QueryURL"] == "search?type=Product&status=Active"
    
    def test_parse_collection_with_metadata(self):
        """Test parsing collection with MetaData."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>Collection with Metadata</Name>
                    <MetaData>
                        <Attribute Name="Status" Value="Active"/>
                    </MetaData>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        collection = parser.collections[0]
        assert "MetaData" in collection
    
    def test_parse_single_collection_group(self):
        """Test parsing single collection group."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <CollectionGroup ID="GROUP001">
                    <Name>Group Name</Name>
                </CollectionGroup>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.collection_groups) == 1
        assert parser.collection_groups[0]["ID"] == "GROUP001"
    
    def test_parse_collection_group_with_nested_collections(self):
        """Test parsing collection group with nested collections."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <CollectionGroup ID="GROUP001">
                    <Name>Parent Group</Name>
                    <Collection ID="COLL001">
                        <Name>Child Collection</Name>
                    </Collection>
                </CollectionGroup>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        group = parser.collection_groups[0]
        assert "Collection" in group
        assert len(group["Collection"]) == 1
        assert group["Collection"][0]["ID"] == "COLL001"
    
    def test_parse_collection_group_with_nested_groups(self):
        """Test parsing collection group with nested collection groups (hierarchical)."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <CollectionGroup ID="GROUP001">
                    <Name>Parent Group</Name>
                    <CollectionGroup ID="GROUP002">
                        <Name>Child Group</Name>
                    </CollectionGroup>
                </CollectionGroup>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        parent_group = parser.collection_groups[0]
        assert "CollectionGroup" in parent_group
        assert len(parent_group["CollectionGroup"]) == 1
        assert parent_group["CollectionGroup"][0]["ID"] == "GROUP002"
    
    def test_parse_complex_collection_hierarchy(self):
        """Test parsing complex hierarchy with multiple levels of nesting."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <CollectionGroup ID="GROUP001">
                    <Name>Level 1</Name>
                    <CollectionGroup ID="GROUP002">
                        <Name>Level 2</Name>
                        <Collection ID="COLL001">
                            <Name>Leaf Collection</Name>
                        </Collection>
                    </CollectionGroup>
                    <Collection ID="COLL002">
                        <Name>Direct Child Collection</Name>
                    </Collection>
                </CollectionGroup>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        parent_group = parser.collection_groups[0]
        assert parent_group["ID"] == "GROUP001"
        assert "CollectionGroup" in parent_group
        assert "Collection" in parent_group
        assert len(parent_group["Collection"]) == 1
    
    def test_parse_multiple_collections_and_groups(self):
        """Test parsing multiple collections and groups at root level."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>Collection 1</Name>
                </Collection>
                <CollectionGroup ID="GROUP001">
                    <Name>Group 1</Name>
                </CollectionGroup>
                <Collection ID="COLL002">
                    <Name>Collection 2</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.collections) == 2
        assert len(parser.collection_groups) == 1


class TestPhase12Integration:
    """Integration tests for ReplacementRules and Collections together."""
    
    def test_parse_with_replacement_rules_and_collections(self):
        """Test parsing document with both ReplacementRules and Collections."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products>
                    <ReplaceValues AttributeID="Name"/>
                </Products>
            </ReplacementRules>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>Products</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.replacement_rules) > 0
        assert len(parser.collections) == 1
    
    def test_parse_replacement_rules_with_all_entity_types(self):
        """Test parsing ReplacementRules with all entity types together."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Attributes/>
                <Products/>
                <Classifications/>
                <Entities/>
                <Assets/>
                <LinkTypes/>
                <UserTypes/>
                <UserGroups/>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "Attributes" in parser.replacement_rules
        assert "Products" in parser.replacement_rules
        assert "Classifications" in parser.replacement_rules
        assert "Entities" in parser.replacement_rules
        assert "Assets" in parser.replacement_rules
        assert "LinkTypes" in parser.replacement_rules
        assert "UserTypes" in parser.replacement_rules
        assert "UserGroups" in parser.replacement_rules
    
    def test_parse_with_other_phases_and_phase12(self):
        """Test parsing document with earlier phase elements plus Phase 12."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <Products>
                <Product ID="PROD001">
                    <Name>Product 1</Name>
                </Product>
            </Products>
            <ReplacementRules>
                <Products>
                    <ReplaceValues AttributeID="Description"/>
                </Products>
            </ReplacementRules>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>Product Collection</Name>
                </Collection>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        # Verify earlier phases still work
        assert len(parser.products) == 1
        # Verify Phase 12 works
        assert len(parser.replacement_rules) > 0
        assert len(parser.collections) == 1


class TestPhase12EdgeCases:
    """Edge case tests for Phase 12 elements."""
    
    def test_collection_group_with_parent_id(self):
        """Test collection group with ParentID for hierarchy."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <CollectionGroup ID="GROUP001" ParentID="PARENT001">
                    <Name>Child Group</Name>
                </CollectionGroup>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        group = parser.collection_groups[0]
        assert group["ParentID"] == "PARENT001"
    
    def test_empty_collection_with_no_name(self):
        """Test collection with no Name element."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <Collection ID="COLL001"/>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        collection = parser.collections[0]
        assert collection["ID"] == "COLL001"
        assert "Name" not in collection
    
    def test_replacement_rules_with_multiple_replace_values(self):
        """Test Products with multiple ReplaceValues rules."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products>
                    <ReplaceValues AttributeID="Name"/>
                    <ReplaceValues AttributeGroupID="BasicInfo"/>
                    <ReplaceValues AttributeID="Description" ContextID="English"/>
                </Products>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        products = parser.replacement_rules["Products"][0]
        assert len(products["ReplaceValues"]) == 3
        assert products["ReplaceValues"][0]["AttributeID"] == "Name"
        assert products["ReplaceValues"][1]["AttributeGroupID"] == "BasicInfo"
        assert products["ReplaceValues"][2]["ContextID"] == "English"
    
    def test_replacement_rules_with_attribute_links(self):
        """Test replacement rules with ReplaceAttributeLinks."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products>
                    <ReplaceAttributeLinks AttributeID="Description"/>
                </Products>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        products = parser.replacement_rules["Products"][0]
        assert "ReplaceAttributeLinks" in products
        assert products["ReplaceAttributeLinks"][0]["AttributeID"] == "Description"
    
    def test_replacement_rules_with_classification_references(self):
        """Test replacement rules with ReplaceClassificationReferences."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products>
                    <ReplaceClassificationReferences/>
                </Products>
            </ReplacementRules>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        products = parser.replacement_rules["Products"][0]
        assert "ReplaceClassificationReferences" in products
    
    def test_deep_collection_hierarchy_five_levels(self):
        """Test deeply nested collection hierarchy (5 levels)."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <CollectionList>
                <CollectionGroup ID="L1">
                    <CollectionGroup ID="L2">
                        <CollectionGroup ID="L3">
                            <CollectionGroup ID="L4">
                                <Collection ID="L5">
                                    <Name>Deep Collection</Name>
                                </Collection>
                            </CollectionGroup>
                        </CollectionGroup>
                    </CollectionGroup>
                </CollectionGroup>
            </CollectionList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        # Should parse without errors
        assert len(parser.collection_groups) == 1


class TestPhase12BackwardCompatibility:
    """Verify Phase 12 doesn't break earlier phases."""
    
    def test_parse_phase2_without_phase12(self):
        """Test that Phase 2 elements still parse correctly without Phase 12."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <Products>
                <Product ID="PROD001">
                    <Name>Test Product</Name>
                </Product>
            </Products>
            <Assets>
                <Asset ID="ASSET001">
                    <Name>Test Asset</Name>
                </Asset>
            </Assets>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.products) == 1
        assert len(parser.assets) == 1
        # Phase 12 should be empty
        assert isinstance(parser.replacement_rules, dict)
        assert len(parser.replacement_rules) == 0
        assert len(parser.collections) == 0
        assert len(parser.collection_groups) == 0
