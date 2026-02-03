#!/usr/bin/env python3
"""
Phase 10 Parser Tests: Organizational Structure Support

Tests for parsing organizational structure elements including:
- DeleteClassifications: Deletion specifications for classifications
- DeleteEntities: Deletion specifications for entities  
- CrossReferenceTypes: Relation type definitions
- Qualifiers: Multi-dimensional data qualifiers

These tests ensure proper parsing of Phase 10 elements from STEP-XML documents.
"""

import pytest
from stepxmlclient.parser import Parser


class TestParseDeleteClassification:
    """Tests for DeleteClassification element parsing."""
    
    def test_parse_delete_classification_minimal(self):
        """Test parsing DeleteClassification with required attributes only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications>
                <DeleteClassification ID="Color" Type="All"/>
            </DeleteClassifications>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_classifications) == 1
        delc = parser.delete_classifications[0]
        assert delc["ID"] == "Color"
        assert delc["Type"] == "All"
    
    def test_parse_delete_classification_with_key_values(self):
        """Test parsing DeleteClassification with KeyValue children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications>
                <DeleteClassification ID="Size" Type="Values">
                    <KeyValue>Small</KeyValue>
                    <KeyValue>Medium</KeyValue>
                    <KeyValue>Large</KeyValue>
                </DeleteClassification>
            </DeleteClassifications>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_classifications) == 1
        delc = parser.delete_classifications[0]
        assert delc["ID"] == "Size"
        assert delc["Type"] == "Values"
        assert len(delc["KeyValue"]) == 3
        assert delc["KeyValue"][0]["value"] == "Small"
        assert delc["KeyValue"][1]["value"] == "Medium"
        assert delc["KeyValue"][2]["value"] == "Large"
    
    def test_parse_delete_classification_subtypes(self):
        """Test parsing DeleteClassification with SubTypes deletion type."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications>
                <DeleteClassification ID="ProductType" Type="SubTypes">
                    <KeyValue>Electronics</KeyValue>
                </DeleteClassification>
            </DeleteClassifications>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_classifications) == 1
        delc = parser.delete_classifications[0]
        assert delc["Type"] == "SubTypes"
        assert len(delc["KeyValue"]) == 1
        assert delc["KeyValue"][0]["value"] == "Electronics"
    
    def test_parse_multiple_delete_classifications(self):
        """Test parsing multiple DeleteClassification elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications>
                <DeleteClassification ID="Color" Type="All"/>
                <DeleteClassification ID="Size" Type="Values">
                    <KeyValue>XL</KeyValue>
                </DeleteClassification>
                <DeleteClassification ID="Brand" Type="All"/>
            </DeleteClassifications>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_classifications) == 3
        assert parser.delete_classifications[0]["ID"] == "Color"
        assert parser.delete_classifications[1]["ID"] == "Size"
        assert parser.delete_classifications[2]["ID"] == "Brand"


class TestParseDeleteEntity:
    """Tests for DeleteEntity element parsing."""
    
    def test_parse_delete_entity_minimal(self):
        """Test parsing DeleteEntity with ID attribute only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteEntities>
                <DeleteEntity ID="Supplier"/>
            </DeleteEntities>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_entities) == 1
        dele = parser.delete_entities[0]
        assert dele["ID"] == "Supplier"
    
    def test_parse_delete_entity_with_key_values(self):
        """Test parsing DeleteEntity with KeyValue children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteEntities>
                <DeleteEntity ID="Supplier">
                    <KeyValue>SUPP001</KeyValue>
                    <KeyValue>SUPP002</KeyValue>
                </DeleteEntity>
            </DeleteEntities>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_entities) == 1
        dele = parser.delete_entities[0]
        assert dele["ID"] == "Supplier"
        assert len(dele["KeyValue"]) == 2
        assert dele["KeyValue"][0]["value"] == "SUPP001"
        assert dele["KeyValue"][1]["value"] == "SUPP002"
    
    def test_parse_multiple_delete_entities(self):
        """Test parsing multiple DeleteEntity elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteEntities>
                <DeleteEntity ID="Supplier">
                    <KeyValue>S001</KeyValue>
                </DeleteEntity>
                <DeleteEntity ID="Distributor">
                    <KeyValue>D001</KeyValue>
                    <KeyValue>D002</KeyValue>
                </DeleteEntity>
                <DeleteEntity ID="Retailer"/>
            </DeleteEntities>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_entities) == 3
        assert parser.delete_entities[0]["ID"] == "Supplier"
        assert parser.delete_entities[1]["ID"] == "Distributor"
        assert parser.delete_entities[2]["ID"] == "Retailer"
        assert len(parser.delete_entities[2].get("KeyValue", [])) == 0


class TestParseCrossReferenceType:
    """Tests for CrossReferenceType element parsing."""
    
    def test_parse_cross_reference_type_minimal(self):
        """Test parsing CrossReferenceType with ID and Name only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossReferenceTypes>
                <CrossReferenceType ID="Replaces">
                    <Name>Replaces</Name>
                </CrossReferenceType>
            </CrossReferenceTypes>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.cross_reference_types) == 1
        crt = parser.cross_reference_types[0]
        assert crt["ID"] == "Replaces"
        assert crt["Name"] == ["Replaces"]
    
    def test_parse_cross_reference_type_multiple_names(self):
        """Test parsing CrossReferenceType with multiple Name elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossReferenceTypes>
                <CrossReferenceType ID="Compatible">
                    <Name>Compatible With</Name>
                    <Name>Compatible</Name>
                </CrossReferenceType>
            </CrossReferenceTypes>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.cross_reference_types) == 1
        crt = parser.cross_reference_types[0]
        assert crt["ID"] == "Compatible"
        assert crt["Name"] == ["Compatible With", "Compatible"]
    
    def test_parse_cross_reference_type_with_metadata(self):
        """Test parsing CrossReferenceType with MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossReferenceTypes>
                <CrossReferenceType ID="RelatedTo">
                    <Name>Related To</Name>
                    <MetaData>
                        <Attribute ID="Direction" Value="Bidirectional"/>
                    </MetaData>
                </CrossReferenceType>
            </CrossReferenceTypes>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.cross_reference_types) == 1
        crt = parser.cross_reference_types[0]
        assert crt["ID"] == "RelatedTo"
        assert "MetaData" in crt
    
    def test_parse_multiple_cross_reference_types(self):
        """Test parsing multiple CrossReferenceType elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossReferenceTypes>
                <CrossReferenceType ID="Replaces">
                    <Name>Replaces</Name>
                </CrossReferenceType>
                <CrossReferenceType ID="Compatible">
                    <Name>Compatible</Name>
                </CrossReferenceType>
                <CrossReferenceType ID="Accessory">
                    <Name>Accessory For</Name>
                </CrossReferenceType>
            </CrossReferenceTypes>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.cross_reference_types) == 3
        ids = [crt["ID"] for crt in parser.cross_reference_types]
        assert ids == ["Replaces", "Compatible", "Accessory"]


class TestParseQualifier:
    """Tests for Qualifier element parsing."""
    
    def test_parse_qualifier_minimal(self):
        """Test parsing Qualifier with ID and Name only."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Qualifiers>
                <Qualifier ID="SizeQualifier">
                    <Name>Size</Name>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.qualifiers) == 1
        qual = parser.qualifiers[0]
        assert qual["ID"] == "SizeQualifier"
        assert qual["Name"] == ["Size"]
    
    def test_parse_qualifier_multiple_names(self):
        """Test parsing Qualifier with multiple Name elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Qualifiers>
                <Qualifier ID="ColorQualifier">
                    <Name>Color</Name>
                    <Name>Colour</Name>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.qualifiers) == 1
        qual = parser.qualifiers[0]
        assert qual["ID"] == "ColorQualifier"
        assert qual["Name"] == ["Color", "Colour"]
    
    def test_parse_qualifier_with_dimension_point_links(self):
        """Test parsing Qualifier with DimensionPointLink children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Qualifiers>
                <Qualifier ID="SizeColorQualifier">
                    <Name>Size and Color</Name>
                    <DimensionPointLink DimensionID="Size" DimensionPointID="S"/>
                    <DimensionPointLink DimensionID="Color" DimensionPointID="Red"/>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.qualifiers) == 1
        qual = parser.qualifiers[0]
        assert qual["ID"] == "SizeColorQualifier"
        assert len(qual["DimensionPointLink"]) == 2
        assert qual["DimensionPointLink"][0]["DimensionID"] == "Size"
        assert qual["DimensionPointLink"][0]["DimensionPointID"] == "S"
        assert qual["DimensionPointLink"][1]["DimensionID"] == "Color"
        assert qual["DimensionPointLink"][1]["DimensionPointID"] == "Red"
    
    def test_parse_qualifier_with_metadata(self):
        """Test parsing Qualifier with MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Qualifiers>
                <Qualifier ID="Q1">
                    <Name>Qualifier One</Name>
                    <MetaData>
                        <Attribute ID="Type" Value="Standard"/>
                    </MetaData>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.qualifiers) == 1
        qual = parser.qualifiers[0]
        assert qual["ID"] == "Q1"
        assert "MetaData" in qual
    
    def test_parse_multiple_qualifiers(self):
        """Test parsing multiple Qualifier elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Qualifiers>
                <Qualifier ID="Q1">
                    <Name>Qualifier One</Name>
                </Qualifier>
                <Qualifier ID="Q2">
                    <Name>Qualifier Two</Name>
                    <DimensionPointLink DimensionID="D1" DimensionPointID="P1"/>
                </Qualifier>
                <Qualifier ID="Q3">
                    <Name>Qualifier Three</Name>
                    <DimensionPointLink DimensionID="D2" DimensionPointID="P2"/>
                    <DimensionPointLink DimensionID="D3" DimensionPointID="P3"/>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.qualifiers) == 3
        assert parser.qualifiers[0]["ID"] == "Q1"
        assert parser.qualifiers[1]["ID"] == "Q2"
        assert parser.qualifiers[2]["ID"] == "Q3"
        assert len(parser.qualifiers[2]["DimensionPointLink"]) == 2


class TestPhase10Integration:
    """Integration tests for Phase 10 elements together."""
    
    def test_parse_all_phase10_elements(self):
        """Test parsing all Phase 10 elements in one document."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications>
                <DeleteClassification ID="OldColor" Type="All"/>
            </DeleteClassifications>
            <DeleteEntities>
                <DeleteEntity ID="OldSupplier">
                    <KeyValue>S001</KeyValue>
                </DeleteEntity>
            </DeleteEntities>
            <CrossReferenceTypes>
                <CrossReferenceType ID="Replaces">
                    <Name>Replaces</Name>
                </CrossReferenceType>
            </CrossReferenceTypes>
            <Qualifiers>
                <Qualifier ID="SizeColorQualifier">
                    <Name>Size and Color</Name>
                    <DimensionPointLink DimensionID="Size" DimensionPointID="M"/>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_classifications) == 1
        assert len(parser.delete_entities) == 1
        assert len(parser.cross_reference_types) == 1
        assert len(parser.qualifiers) == 1
    
    def test_parse_phase10_empty_sections(self):
        """Test parsing document with empty Phase 10 sections."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications/>
            <DeleteEntities/>
            <CrossReferenceTypes/>
            <Qualifiers/>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert parser.delete_classifications == []
        assert parser.delete_entities == []
        assert parser.cross_reference_types == []
        assert parser.qualifiers == []
    
    def test_parse_phase10_with_earlier_phases(self):
        """Test that Phase 10 parsing doesn't interfere with earlier phases."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Products>
                <Product ID="P1">
                    <Name>Product 1</Name>
                </Product>
            </Products>
            <Assets>
                <Asset ID="A1">
                    <Name>Asset 1</Name>
                </Asset>
            </Assets>
            <DeleteClassifications>
                <DeleteClassification ID="Color" Type="All"/>
            </DeleteClassifications>
            <Qualifiers>
                <Qualifier ID="Q1">
                    <Name>Qualifier 1</Name>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        # Verify earlier phases still work
        assert len(parser.products) == 1
        assert len(parser.assets) == 1
        
        # Verify Phase 10
        assert len(parser.delete_classifications) == 1
        assert len(parser.qualifiers) == 1


class TestPhase10EdgeCases:
    """Edge case tests for Phase 10 parsing."""
    
    def test_parse_delete_classification_empty_key_values(self):
        """Test parsing DeleteClassification with no KeyValue children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteClassifications>
                <DeleteClassification ID="Empty" Type="All"/>
            </DeleteClassifications>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_classifications) == 1
        delc = parser.delete_classifications[0]
        assert "KeyValue" not in delc
    
    def test_parse_qualifier_no_dimension_points(self):
        """Test parsing Qualifier with no DimensionPointLink children."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Qualifiers>
                <Qualifier ID="SimpleQualifier">
                    <Name>Simple</Name>
                </Qualifier>
            </Qualifiers>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.qualifiers) == 1
        qual = parser.qualifiers[0]
        assert "DimensionPointLink" not in qual
    
    def test_parse_delete_entity_multiple_key_values_single(self):
        """Test parsing DeleteEntity with many KeyValue elements."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <DeleteEntities>
                <DeleteEntity ID="Supplier">
                    <KeyValue>S001</KeyValue>
                    <KeyValue>S002</KeyValue>
                    <KeyValue>S003</KeyValue>
                    <KeyValue>S004</KeyValue>
                    <KeyValue>S005</KeyValue>
                </DeleteEntity>
            </DeleteEntities>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.delete_entities) == 1
        dele = parser.delete_entities[0]
        assert len(dele["KeyValue"]) == 5
        assert dele["KeyValue"][0]["value"] == "S001"
        assert dele["KeyValue"][1]["value"] == "S002"
        assert dele["KeyValue"][2]["value"] == "S003"
        assert dele["KeyValue"][3]["value"] == "S004"
        assert dele["KeyValue"][4]["value"] == "S005"
    
    def test_parse_cross_reference_type_no_metadata(self):
        """Test parsing CrossReferenceType without MetaData."""
        xml = """
        <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossReferenceTypes>
                <CrossReferenceType ID="Type1">
                    <Name>Type One</Name>
                </CrossReferenceType>
            </CrossReferenceTypes>
        </STEP-ProductInformation>
        """
        parser = Parser()
        parser.parse_str(xml)
        
        assert len(parser.cross_reference_types) == 1
        crt = parser.cross_reference_types[0]
        assert "MetaData" not in crt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
