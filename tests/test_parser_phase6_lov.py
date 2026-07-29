#!/usr/bin/env python3
"""Unit and integration tests for Phase 6 List of Values (LOV) system parser."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_single_list_of_value():
    """Test parsing a single list of value (LOV) with basic properties."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="StatusLOV">
                <Name>Status Values</Name>
                <Validation Base="Text"/>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, f"Expected 1 LOV, got {len(parser.list_of_values)}"
    lov = parser.list_of_values[0]
    
    assert lov["ID"] == "StatusLOV", "LOV ID not parsed"
    assert lov["Name"] == "Status Values", "LOV Name not parsed"
    assert lov["Validation"] == "Text", "Validation not parsed"
    assert lov["AllowUserValueAddition"] is False, "AllowUserValueAddition default incorrect"
    assert lov["UseValueID"] is False, "UseValueID default incorrect"
    
    print("✓ Single LOV parsed correctly")
    return True


def test_parse_lov_with_simple_values():
    """Test parsing LOV with simple value items."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="ColorLOV" UseValueID="true">
                <Name>Colors</Name>
                <Validation Base="Text"/>
                <Value ID="RED">Red</Value>
                <Value ID="GREEN">Green</Value>
                <Value ID="BLUE">Blue</Value>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    assert lov["ID"] == "ColorLOV", "LOV ID not parsed"
    assert lov["UseValueID"] is True, "UseValueID not converted"
    assert "Value" in lov, "Values not parsed"
    assert len(lov["Value"]) == 3, "Expected 3 values"
    
    # Check first value
    assert lov["Value"][0]["ID"] == "RED", "First value ID not correct"
    assert lov["Value"][0]["value"] == "Red", "First value text not correct"
    
    # Check last value
    assert lov["Value"][2]["ID"] == "BLUE", "Last value ID not correct"
    assert lov["Value"][2]["value"] == "Blue", "Last value text not correct"
    
    print("✓ LOV with simple values parsed correctly")
    return True


def test_parse_lov_with_dimension_link():
    """Test parsing LOV with dimension links."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="SizeLOV">
                <Name>Sizes</Name>
                <DimensionLink DimensionID="Length"/>
                <DimensionLink DimensionID="Width"/>
                <Value ID="SMALL">S</Value>
                <Value ID="MEDIUM">M</Value>
                <Value ID="LARGE">L</Value>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    assert "DimensionLink" in lov, "DimensionLinks not parsed"
    assert len(lov["DimensionLink"]) == 2, "Expected 2 dimension links"
    assert lov["DimensionLink"][0] == "Length", "First dimension link not correct"
    assert lov["DimensionLink"][1] == "Width", "Second dimension link not correct"
    
    print("✓ LOV with dimension links parsed correctly")
    return True


def test_parse_lov_with_value_groups():
    """Test parsing LOV with value groups (qualifier-specific values)."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="BrandLOV">
                <Name>Brand Values</Name>
                <ValueGroup ID="Group1">
                    <Value ID="BRAND1">Brand One</Value>
                    <Value ID="BRAND2">Brand Two</Value>
                </ValueGroup>
                <ValueGroup ID="Group2">
                    <Value ID="BRAND3">Brand Three</Value>
                </ValueGroup>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    assert "ValueGroup" in lov, "ValueGroups not parsed"
    assert len(lov["ValueGroup"]) == 2, "Expected 2 value groups"
    
    # Check first group
    assert lov["ValueGroup"][0]["ID"] == "Group1", "First group ID not correct"
    assert len(lov["ValueGroup"][0]["Value"]) == 2, "First group should have 2 values"
    assert lov["ValueGroup"][0]["Value"][0]["ID"] == "BRAND1", "First value in first group not correct"
    
    # Check second group
    assert lov["ValueGroup"][1]["ID"] == "Group2", "Second group ID not correct"
    assert len(lov["ValueGroup"][1]["Value"]) == 1, "Second group should have 1 value"
    
    print("✓ LOV with value groups parsed correctly")
    return True


def test_parse_lov_with_metadata():
    """Test parsing LOV with metadata."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="PriorityLOV">
                <Name>Priority Levels</Name>
                <MetaData>
                    <Value AttributeID="description">System priorities</Value>
                </MetaData>
                <Value ID="HIGH">High</Value>
                <Value ID="NORMAL">Normal</Value>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    assert "MetaData" in lov, "MetaData not parsed"
    assert "description" in lov["MetaData"], "Description metadata not found"
    
    print("✓ LOV with metadata parsed correctly")
    return True


def test_parse_lov_with_delete_values():
    """Test parsing LOV with delete value instructions."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="StatusLOV" UseValueID="true">
                <Name>Status</Name>
                <Value ID="ACTIVE">Active</Value>
                <Value ID="INACTIVE">Inactive</Value>
                <DeleteValue Force="false" GenerateEvents="true">DEPRECATED</DeleteValue>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    assert "DeleteValue" in lov, "DeleteValue not parsed"
    assert len(lov["DeleteValue"]) == 1, "Expected 1 delete instruction"
    
    delete_instr = lov["DeleteValue"][0]
    assert delete_instr["Force"] is False, "Force not converted correctly"
    assert delete_instr["GenerateEvents"] is True, "GenerateEvents not converted correctly"
    assert delete_instr["value"] == "DEPRECATED", "Delete value ID not parsed"
    
    print("✓ LOV with delete values parsed correctly")
    return True


def test_parse_multiple_lovs():
    """Test parsing multiple LOVs in single document."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="StatusLOV">
                <Name>Status</Name>
                <Value>Active</Value>
                <Value>Inactive</Value>
            </ListOfValue>
            <ListOfValue ID="ColorLOV">
                <Name>Colors</Name>
                <Value>Red</Value>
                <Value>Blue</Value>
            </ListOfValue>
            <ListOfValue ID="SizeLOV">
                <Name>Sizes</Name>
                <Value>Small</Value>
                <Value>Large</Value>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 3, f"Expected 3 LOVs, got {len(parser.list_of_values)}"
    assert parser.list_of_values[0]["ID"] == "StatusLOV", "First LOV ID not correct"
    assert parser.list_of_values[1]["ID"] == "ColorLOV", "Second LOV ID not correct"
    assert parser.list_of_values[2]["ID"] == "SizeLOV", "Third LOV ID not correct"
    
    print("✓ Multiple LOVs parsed correctly")
    return True


def test_parse_lov_with_parent_hierarchy():
    """Test parsing LOV with ParentID for hierarchy."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="VehicleTypeLOV">
                <Name>Vehicle Types</Name>
                <Value>Car</Value>
            </ListOfValue>
            <ListOfValue ID="CarTypeLOV" ParentID="VehicleTypeLOV">
                <Name>Car Types</Name>
                <Value>Sedan</Value>
                <Value>SUV</Value>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 2, "Expected 2 LOVs"
    
    # Check parent LOV
    parent_lov = parser.list_of_values[0]
    assert parent_lov["ID"] == "VehicleTypeLOV", "Parent LOV ID not correct"
    assert "ParentID" not in parent_lov or parent_lov["ParentID"] is None, "Parent LOV should not have ParentID"
    
    # Check child LOV
    child_lov = parser.list_of_values[1]
    assert child_lov["ID"] == "CarTypeLOV", "Child LOV ID not correct"
    assert child_lov["ParentID"] == "VehicleTypeLOV", "Child LOV ParentID not correct"
    
    print("✓ LOV with parent hierarchy parsed correctly")
    return True


def test_parse_complex_lov_system():
    """Test complex LOV with all features combined."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="ProductCategoryLOV" UseValueID="true" AllowUserValueAddition="false" DefaultUnitID="DefaultUnit">
                <Name>Product Categories</Name>
                <Validation Base="Text"/>
                <DimensionLink DimensionID="Region"/>
                <MetaData>
                    <Value AttributeID="source">Master Data</Value>
                </MetaData>
                <AttributeGroupLink AttributeGroupID="ProductProperties"/>
                <Value ID="ELEC">Electronics</Value>
                <Value ID="CLOTH">Clothing</Value>
                <ValueGroup ID="FoodGroup">
                    <Value ID="FOOD_DRY">Dry Foods</Value>
                    <Value ID="FOOD_FRZ">Frozen Foods</Value>
                </ValueGroup>
                <DeleteValue Force="true" GenerateEvents="false">OBSOLETE</DeleteValue>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    # Check attributes
    assert lov["ID"] == "ProductCategoryLOV", "ID not correct"
    assert lov["UseValueID"] is True, "UseValueID not converted"
    assert lov["AllowUserValueAddition"] is False, "AllowUserValueAddition not converted"
    assert lov["DefaultUnitID"] == "DefaultUnit", "DefaultUnitID not parsed"
    
    # Check validation
    assert lov["Validation"] == "Text", "Validation not parsed"
    
    # Check dimension links
    assert len(lov["DimensionLink"]) == 1, "Expected 1 dimension link"
    assert lov["DimensionLink"][0] == "Region", "Dimension link not correct"
    
    # Check metadata
    assert "MetaData" in lov, "MetaData not parsed"
    
    # Check attribute group links
    assert len(lov["AttributeGroupLink"]) == 1, "Expected 1 attribute group link"
    
    # Check values
    assert "Value" in lov, "Values not parsed"
    assert len(lov["Value"]) == 2, "Expected 2 direct values"
    assert lov["Value"][0]["ID"] == "ELEC", "First value ID not correct"
    assert lov["Value"][1]["ID"] == "CLOTH", "Second value ID not correct"
    
    # Check value groups
    assert "ValueGroup" in lov, "ValueGroups not parsed"
    assert len(lov["ValueGroup"]) == 1, "Expected 1 value group"
    assert lov["ValueGroup"][0]["ID"] == "FoodGroup", "ValueGroup ID not correct"
    assert len(lov["ValueGroup"][0]["Value"]) == 2, "Expected 2 values in group"
    
    # Check delete instructions
    assert len(lov["DeleteValue"]) == 1, "Expected 1 delete instruction"
    assert lov["DeleteValue"][0]["Force"] is True, "Force not parsed correctly"
    assert lov["DeleteValue"][0]["GenerateEvents"] is False, "GenerateEvents not parsed correctly"
    
    print("✓ Complex LOV system parsed correctly")
    return True


def test_parse_lov_with_attribute_group_links():
    """Test parsing LOV with multiple attribute group links."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <ListsOfValues>
            <ListOfValue ID="CountryLOV">
                <Name>Countries</Name>
                <AttributeGroupLink AttributeGroupID="Shipping"/>
                <AttributeGroupLink AttributeGroupID="Compliance"/>
                <AttributeGroupLink AttributeGroupID="Localization"/>
                <Value>USA</Value>
                <Value>Canada</Value>
            </ListOfValue>
        </ListsOfValues>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values) == 1, "Expected 1 LOV"
    lov = parser.list_of_values[0]
    
    assert "AttributeGroupLink" in lov, "AttributeGroupLinks not parsed"
    assert len(lov["AttributeGroupLink"]) == 3, "Expected 3 attribute group links"
    assert lov["AttributeGroupLink"][0] == "Shipping", "First link not correct"
    assert lov["AttributeGroupLink"][1] == "Compliance", "Second link not correct"
    assert lov["AttributeGroupLink"][2] == "Localization", "Third link not correct"
    
    print("✓ LOV with attribute group links parsed correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 6 List of Values (LOV) Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_single_list_of_value()
        print()
        test_parse_lov_with_simple_values()
        print()
        test_parse_lov_with_dimension_link()
        print()
        test_parse_lov_with_value_groups()
        print()
        test_parse_lov_with_metadata()
        print()
        test_parse_lov_with_delete_values()
        print()
        test_parse_multiple_lovs()
        print()
        test_parse_lov_with_parent_hierarchy()
        print()
        test_parse_complex_lov_system()
        print()
        test_parse_lov_with_attribute_group_links()
        
        print()
        print("=" * 70)
        print("✓ All Phase 6 LOV tests passed (10/10)!")
        print("=" * 70)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
