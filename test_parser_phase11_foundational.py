#!/usr/bin/env python3
"""
Phase 11 Parser Tests: Foundational Elements

Tests for parsing foundational system elements including:
- Dimensions: Multi-dimensional data organization axes
- DimensionPoints: Individual dimension values
- Tags: Flexible object categorization
- TagGroups: Hierarchical tag organization
- Units: Measurement units for quantitative data

These tests ensure proper parsing of Phase 11 foundational elements from STEP-XML documents.
"""

import pytest
from stepxmlclient.parser import Parser


class TestParseDimension:
    """Tests for Dimension element parsing."""
    
    def test_parse_dimension_minimal(self):
        """Test parsing Dimension with ID only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Color"/>
            </DimensionList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 1
        dim = parser.dimensions[0]
        assert dim["ID"] == "Color"
    
    def test_parse_dimension_with_name(self):
        """Test parsing Dimension with Name elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Market">
                    <Name>Market Segment</Name>
                    <Name>Segment</Name>
                </Dimension>
            </DimensionList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 1
        dim = parser.dimensions[0]
        assert dim["ID"] == "Market"
        assert dim["Name"] == ["Market Segment", "Segment"]
    
    def test_parse_dimension_with_dimension_points(self):
        """Test parsing Dimension with DimensionPoint children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Size">
                    <Name>Size</Name>
                    <DimensionPoint ID="Small">
                        <Name>Small</Name>
                    </DimensionPoint>
                    <DimensionPoint ID="Medium">
                        <Name>Medium</Name>
                    </DimensionPoint>
                    <DimensionPoint ID="Large">
                        <Name>Large</Name>
                    </DimensionPoint>
                </Dimension>
            </DimensionList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 1
        dim = parser.dimensions[0]
        assert dim["ID"] == "Size"
        assert len(dim["DimensionPoint"]) == 3
        assert dim["DimensionPoint"][0]["ID"] == "Small"
        assert dim["DimensionPoint"][1]["ID"] == "Medium"
        assert dim["DimensionPoint"][2]["ID"] == "Large"
    
    def test_parse_dimension_with_metadata(self):
        """Test parsing Dimension with MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Region">
                    <Name>Region</Name>
                    <MetaData>
                        <Attribute ID="Type" Value="Geographic"/>
                    </MetaData>
                </Dimension>
            </DimensionList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 1
        dim = parser.dimensions[0]
        assert "MetaData" in dim
    
    def test_parse_multiple_dimensions(self):
        """Test parsing multiple Dimension elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Color">
                    <Name>Color</Name>
                </Dimension>
                <Dimension ID="Size">
                    <Name>Size</Name>
                </Dimension>
                <Dimension ID="Material">
                    <Name>Material</Name>
                </Dimension>
            </DimensionList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 3
        assert parser.dimensions[0]["ID"] == "Color"
        assert parser.dimensions[1]["ID"] == "Size"
        assert parser.dimensions[2]["ID"] == "Material"


class TestParseTag:
    """Tests for Tag element parsing."""
    
    def test_parse_tag_minimal(self):
        """Test parsing Tag with ID and Name only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagList>
                <Tag ID="Bestseller">
                    <Name>Bestseller</Name>
                </Tag>
            </TagList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tags) == 1
        tag = parser.tags[0]
        assert tag["ID"] == "Bestseller"
        assert tag["Name"] == ["Bestseller"]
    
    def test_parse_tag_multiple_names(self):
        """Test parsing Tag with multiple Name elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagList>
                <Tag ID="NewProduct">
                    <Name>New Product</Name>
                    <Name>Novo Produto</Name>
                </Tag>
            </TagList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tags) == 1
        tag = parser.tags[0]
        assert tag["ID"] == "NewProduct"
        assert len(tag["Name"]) == 2
        assert "New Product" in tag["Name"]
        assert "Novo Produto" in tag["Name"]
    
    def test_parse_tag_with_metadata(self):
        """Test parsing Tag with MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagList>
                <Tag ID="Premium">
                    <Name>Premium</Name>
                    <MetaData>
                        <Attribute ID="Priority" Value="High"/>
                    </MetaData>
                </Tag>
            </TagList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tags) == 1
        tag = parser.tags[0]
        assert "MetaData" in tag
    
    def test_parse_multiple_tags(self):
        """Test parsing multiple Tag elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagList>
                <Tag ID="T1">
                    <Name>Tag One</Name>
                </Tag>
                <Tag ID="T2">
                    <Name>Tag Two</Name>
                </Tag>
                <Tag ID="T3">
                    <Name>Tag Three</Name>
                </Tag>
            </TagList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tags) == 3
        assert parser.tags[0]["ID"] == "T1"
        assert parser.tags[1]["ID"] == "T2"
        assert parser.tags[2]["ID"] == "T3"


class TestParseTagGroup:
    """Tests for TagGroup element parsing."""
    
    def test_parse_tag_group_minimal(self):
        """Test parsing TagGroup with ID and Name only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagGroupList>
                <TagGroup ID="Promotions">
                    <Name>Promotions</Name>
                </TagGroup>
            </TagGroupList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tag_groups) == 1
        group = parser.tag_groups[0]
        assert group["ID"] == "Promotions"
        assert group["Name"] == ["Promotions"]
    
    def test_parse_tag_group_with_tags(self):
        """Test parsing TagGroup with nested Tag elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagGroupList>
                <TagGroup ID="Special">
                    <Name>Special Items</Name>
                    <Tag ID="Limited">
                        <Name>Limited Edition</Name>
                    </Tag>
                    <Tag ID="Exclusive">
                        <Name>Exclusive</Name>
                    </Tag>
                </TagGroup>
            </TagGroupList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tag_groups) == 1
        group = parser.tag_groups[0]
        assert group["ID"] == "Special"
        assert len(group["Tag"]) == 2
        assert group["Tag"][0]["ID"] == "Limited"
        assert group["Tag"][1]["ID"] == "Exclusive"
    
    def test_parse_tag_group_nested_hierarchy(self):
        """Test parsing TagGroup with nested TagGroup elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagGroupList>
                <TagGroup ID="Categories">
                    <Name>Categories</Name>
                    <TagGroup ID="Fashion">
                        <Name>Fashion</Name>
                        <Tag ID="Clothing">
                            <Name>Clothing</Name>
                        </Tag>
                    </TagGroup>
                    <TagGroup ID="Electronics">
                        <Name>Electronics</Name>
                        <Tag ID="Gadgets">
                            <Name>Gadgets</Name>
                        </Tag>
                    </TagGroup>
                </TagGroup>
            </TagGroupList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tag_groups) == 1
        group = parser.tag_groups[0]
        assert group["ID"] == "Categories"
        assert len(group["TagGroup"]) == 2
        assert group["TagGroup"][0]["ID"] == "Fashion"
        assert group["TagGroup"][1]["ID"] == "Electronics"
    
    def test_parse_tag_group_with_metadata(self):
        """Test parsing TagGroup with MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagGroupList>
                <TagGroup ID="Sales">
                    <Name>Sales Tags</Name>
                    <MetaData>
                        <Attribute ID="Owner" Value="SalesTeam"/>
                    </MetaData>
                </TagGroup>
            </TagGroupList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tag_groups) == 1
        group = parser.tag_groups[0]
        assert "MetaData" in group
    
    def test_parse_multiple_tag_groups(self):
        """Test parsing multiple TagGroup elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagGroupList>
                <TagGroup ID="Group1">
                    <Name>Group One</Name>
                </TagGroup>
                <TagGroup ID="Group2">
                    <Name>Group Two</Name>
                </TagGroup>
                <TagGroup ID="Group3">
                    <Name>Group Three</Name>
                </TagGroup>
            </TagGroupList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tag_groups) == 3
        assert parser.tag_groups[0]["ID"] == "Group1"
        assert parser.tag_groups[1]["ID"] == "Group2"
        assert parser.tag_groups[2]["ID"] == "Group3"


class TestParseUnit:
    """Tests for Unit element parsing."""
    
    def test_parse_unit_minimal(self):
        """Test parsing Unit with ID only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <UnitList>
                <Unit ID="Meter"/>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.units) == 1
        unit = parser.units[0]
        assert unit["ID"] == "Meter"
    
    def test_parse_unit_with_attributes(self):
        """Test parsing Unit with Name, Symbol, and Formula attributes."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <UnitList>
                <Unit ID="Kilogram" Name="Kilogram" Symbol="kg" Formula="1000*g"/>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.units) == 1
        unit = parser.units[0]
        assert unit["ID"] == "Kilogram"
        assert unit["Name"] == "Kilogram"
        assert unit["Symbol"] == "kg"
        assert unit["Formula"] == "1000*g"
    
    def test_parse_unit_with_metadata(self):
        """Test parsing Unit with MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <UnitList>
                <Unit ID="Liter" Name="Liter" Symbol="L">
                    <MetaData>
                        <Attribute ID="Type" Value="Volume"/>
                    </MetaData>
                </Unit>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.units) == 1
        unit = parser.units[0]
        assert "MetaData" in unit
    
    def test_parse_multiple_units(self):
        """Test parsing multiple Unit elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <UnitList>
                <Unit ID="Meter" Name="Meter" Symbol="m"/>
                <Unit ID="Kilogram" Name="Kilogram" Symbol="kg"/>
                <Unit ID="Second" Name="Second" Symbol="s"/>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.units) == 3
        assert parser.units[0]["ID"] == "Meter"
        assert parser.units[1]["ID"] == "Kilogram"
        assert parser.units[2]["ID"] == "Second"
    
    def test_parse_units_with_various_symbols(self):
        """Test parsing units with various measurement symbols."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <UnitList>
                <Unit ID="Centimeter" Symbol="cm"/>
                <Unit ID="Gram" Symbol="g"/>
                <Unit ID="Milliliter" Symbol="ml"/>
                <Unit ID="Celsius" Symbol="°C"/>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.units) == 4
        assert parser.units[0]["Symbol"] == "cm"
        assert parser.units[1]["Symbol"] == "g"
        assert parser.units[2]["Symbol"] == "ml"
        assert parser.units[3]["Symbol"] == "°C"


class TestPhase11Integration:
    """Integration tests for Phase 11 elements together."""
    
    def test_parse_all_phase11_elements(self):
        """Test parsing all Phase 11 elements in one document."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Color">
                    <Name>Color</Name>
                    <DimensionPoint ID="Red">
                        <Name>Red</Name>
                    </DimensionPoint>
                </Dimension>
            </DimensionList>
            <TagList>
                <Tag ID="Bestseller">
                    <Name>Bestseller</Name>
                </Tag>
            </TagList>
            <TagGroupList>
                <TagGroup ID="Promotions">
                    <Name>Promotions</Name>
                </TagGroup>
            </TagGroupList>
            <UnitList>
                <Unit ID="Meter" Symbol="m"/>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 1
        assert len(parser.tags) == 1
        assert len(parser.tag_groups) == 1
        assert len(parser.units) == 1
    
    def test_parse_phase11_empty_sections(self):
        """Test parsing document with empty Phase 11 sections."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList/>
            <TagList/>
            <TagGroupList/>
            <UnitList/>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert parser.dimensions == []
        assert parser.tags == []
        assert parser.tag_groups == []
        assert parser.units == []
    
    def test_parse_phase11_with_earlier_phases(self):
        """Test that Phase 11 parsing doesn't interfere with earlier phases."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Products>
                <Product ID="P1">
                    <Name>Product 1</Name>
                </Product>
            </Products>
            <DimensionList>
                <Dimension ID="Color">
                    <Name>Color</Name>
                </Dimension>
            </DimensionList>
            <TagList>
                <Tag ID="Featured">
                    <Name>Featured</Name>
                </Tag>
            </TagList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        # Verify earlier phases still work
        assert len(parser.products) == 1
        
        # Verify Phase 11
        assert len(parser.dimensions) == 1
        assert len(parser.tags) == 1


class TestPhase11EdgeCases:
    """Edge case tests for Phase 11 parsing."""
    
    def test_parse_dimension_no_points(self):
        """Test parsing Dimension with no DimensionPoint children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DimensionList>
                <Dimension ID="Empty">
                    <Name>Empty Dimension</Name>
                </Dimension>
            </DimensionList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.dimensions) == 1
        dim = parser.dimensions[0]
        assert "DimensionPoint" not in dim
    
    def test_parse_tag_group_complex_hierarchy(self):
        """Test parsing deeply nested TagGroup hierarchy."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <TagGroupList>
                <TagGroup ID="Root">
                    <Name>Root</Name>
                    <TagGroup ID="Level1">
                        <Name>Level 1</Name>
                        <TagGroup ID="Level2">
                            <Name>Level 2</Name>
                            <Tag ID="DeepTag">
                                <Name>Deep Tag</Name>
                            </Tag>
                        </TagGroup>
                    </TagGroup>
                </TagGroup>
            </TagGroupList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.tag_groups) == 1
        root = parser.tag_groups[0]
        assert root["ID"] == "Root"
        assert len(root["TagGroup"]) == 1
        level1 = root["TagGroup"][0]
        assert level1["ID"] == "Level1"
        assert len(level1["TagGroup"]) == 1
        level2 = level1["TagGroup"][0]
        assert level2["ID"] == "Level2"
        assert len(level2["Tag"]) == 1
    
    def test_parse_unit_partial_attributes(self):
        """Test parsing Unit with only some optional attributes."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <UnitList>
                <Unit ID="U1" Name="Unit One"/>
                <Unit ID="U2" Symbol="x2"/>
                <Unit ID="U3" Formula="x*10"/>
            </UnitList>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.units) == 3
        assert parser.units[0]["Name"] == "Unit One"
        assert "Symbol" not in parser.units[0] or parser.units[0].get("Symbol") is None
        assert parser.units[1]["Symbol"] == "x2"
        assert parser.units[2]["Formula"] == "x*10"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
