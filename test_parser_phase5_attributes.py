#!/usr/bin/env python3
"""Unit and integration tests for Phase 5 Attribute system parser."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_single_attribute():
    """Test parsing a single attribute with basic properties."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList>
            <Attribute ID="Description" ProductMode="Property" MultiValued="false" ExternallyMaintained="true">
                <Name>Description</Name>
            </Attribute>
        </AttributeList>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attributes) == 1, f"Expected 1 attribute, got {len(parser.attributes)}"
    attr = parser.attributes[0]
    
    assert attr["ID"] == "Description", "Attribute ID not parsed"
    assert attr["ProductMode"] == "Property", "ProductMode not parsed"
    assert attr["MultiValued"] is False, "MultiValued not converted to bool"
    assert attr["ExternallyMaintained"] is True, "ExternallyMaintained not converted"
    assert "Name" in attr, "Name element not parsed"
    
    print("✓ Single attribute parsed correctly")
    return True


def test_parse_attribute_with_validation():
    """Test parsing attribute with Validation element."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList>
            <Attribute ID="Size" MultiValued="false">
                <Name>Size</Name>
                <Validation Base="Text"/>
            </Attribute>
        </AttributeList>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attributes) == 1, "Expected 1 attribute"
    attr = parser.attributes[0]
    
    assert attr["ID"] == "Size", "Attribute ID not parsed"
    assert "Validation" in attr, "Validation element not parsed"
    assert attr["Validation"] == "Text", "Validation Base attribute not parsed"
    
    print("✓ Attribute with validation parsed correctly")
    return True


def test_parse_attribute_with_lov():
    """Test parsing attribute with ListOfValueLink."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList>
            <Attribute ID="Status" MultiValued="false">
                <Name>Status</Name>
                <ListOfValueLink LOVID="StatusLOV"/>
            </Attribute>
        </AttributeList>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attributes) == 1, "Expected 1 attribute"
    attr = parser.attributes[0]
    
    assert "ListOfValueLink" in attr, "ListOfValueLink not parsed"
    assert attr["ListOfValueLink"] == "StatusLOV", "LOVID not extracted"
    
    print("✓ Attribute with LOV link parsed correctly")
    return True


def test_parse_attribute_with_links():
    """Test parsing attribute with various link elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList>
            <Attribute ID="Color" MultiValued="true">
                <Name>Color</Name>
                <Validation Base="Text"/>
                <AttributeGroupLink AttributeGroupID="Appearance"/>
                <AttributeGroupLink AttributeGroupID="Properties"/>
                <UserTypeLink UserTypeID="Product"/>
                <LinkType ID="UseLink"/>
                <DimensionLink DimensionID="Language"/>
                <DimensionLink DimensionID="Context"/>
            </Attribute>
        </AttributeList>
        <AttributeGroupList/>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attributes) == 1, "Expected 1 attribute"
    attr = parser.attributes[0]
    
    assert "AttributeGroupLink" in attr, "AttributeGroupLinks not parsed"
    assert len(attr["AttributeGroupLink"]) == 2, "Should have 2 attribute group links"
    assert attr["AttributeGroupLink"][0] == "Appearance", "First group link not correct"
    
    assert "UserTypeLink" in attr, "UserTypeLinks not parsed"
    assert attr["UserTypeLink"][0] == "Product", "UserTypeLink not correct"
    
    assert "LinkType" in attr, "LinkTypes not parsed"
    assert attr["LinkType"][0] == "UseLink", "LinkType not correct"
    
    assert "DimensionLink" in attr, "DimensionLinks not parsed"
    assert len(attr["DimensionLink"]) == 2, "Should have 2 dimension links"
    
    print("✓ Attribute with links parsed correctly")
    return True


def test_parse_single_attribute_group():
    """Test parsing single attribute group."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList>
            <AttributeGroup ID="BasicInfo" ShowInWorkbench="true" ManuallySorted="false">
                <Name>Basic Information</Name>
            </AttributeGroup>
        </AttributeGroupList>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attribute_groups) == 1, "Expected 1 attribute group"
    group = parser.attribute_groups[0]
    
    assert group["ID"] == "BasicInfo", "Group ID not parsed"
    assert group["ShowInWorkbench"] is True, "ShowInWorkbench not converted"
    assert group["ManuallySorted"] is False, "ManuallySorted not converted"
    assert group["Selected"] is True, "Selected default should be True"
    assert "Name" in group, "Name not parsed"
    
    print("✓ Single attribute group parsed correctly")
    return True


def test_parse_nested_attribute_groups():
    """Test parsing hierarchical attribute groups."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList>
            <AttributeGroup ID="Parent">
                <Name>Parent Group</Name>
                <AttributeGroup ID="Child1">
                    <Name>Child 1</Name>
                </AttributeGroup>
                <AttributeGroup ID="Child2">
                    <Name>Child 2</Name>
                </AttributeGroup>
            </AttributeGroup>
        </AttributeGroupList>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attribute_groups) == 1, "Expected 1 root group"
    parent = parser.attribute_groups[0]
    
    assert parent["ID"] == "Parent", "Parent ID not parsed"
    assert "AttributeGroup" in parent, "Nested groups missing"
    nested = parent["AttributeGroup"]
    assert isinstance(nested, list), "Nested groups should be list"
    assert len(nested) == 2, "Expected 2 nested groups"
    assert nested[0]["ID"] == "Child1", "First child ID not correct"
    assert nested[1]["ID"] == "Child2", "Second child ID not correct"
    
    print("✓ Nested attribute groups parsed correctly")
    return True


def test_parse_attribute_group_with_metadata():
    """Test parsing attribute group with metadata."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList>
            <AttributeGroup ID="Details">
                <Name>Details</Name>
                <MetaData>
                    <Value AttributeID="description">Detailed information</Value>
                    <MultiValue AttributeID="tags">
                        <Value>important</Value>
                        <Value>standard</Value>
                    </MultiValue>
                </MetaData>
            </AttributeGroup>
        </AttributeGroupList>
        <ListOfValuesGroupList/>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.attribute_groups) == 1, "Expected 1 attribute group"
    group = parser.attribute_groups[0]
    
    assert "MetaData" in group, "MetaData not parsed"
    metadata = group["MetaData"]
    assert "description" in metadata, "Description attribute not in metadata"
    
    print("✓ Attribute group with metadata parsed correctly")
    return True


def test_parse_single_lov_group():
    """Test parsing single ListOfValuesGroup."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList>
            <ListOfValuesGroup ID="Colors">
                <Name xml:lang="en">Color Groups</Name>
            </ListOfValuesGroup>
        </ListOfValuesGroupList>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values_groups) == 1, "Expected 1 LOV group"
    group = parser.list_of_values_groups[0]
    
    assert group["ID"] == "Colors", "Group ID not parsed"
    assert group["Selected"] is True, "Selected default should be True"
    assert "Name" in group, "Name not parsed"
    
    print("✓ Single LOV group parsed correctly")
    return True


def test_parse_nested_lov_groups():
    """Test parsing hierarchical ListOfValuesGroups."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList>
            <ListOfValuesGroup ID="Root">
                <Name>Root Group</Name>
                <ListOfValuesGroup ID="Child1">
                    <Name>Child Group 1</Name>
                </ListOfValuesGroup>
                <ListOfValuesGroup ID="Child2">
                    <Name>Child Group 2</Name>
                </ListOfValuesGroup>
            </ListOfValuesGroup>
        </ListOfValuesGroupList>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values_groups) == 1, "Expected 1 root group"
    root = parser.list_of_values_groups[0]
    
    assert root["ID"] == "Root", "Root ID not parsed"
    assert "ListOfValuesGroup" in root, "Nested groups missing"
    nested = root["ListOfValuesGroup"]
    assert len(nested) == 2, "Expected 2 nested groups"
    assert nested[0]["ID"] == "Child1", "First child not correct"
    
    print("✓ Nested LOV groups parsed correctly")
    return True


def test_parse_lov_group_with_links():
    """Test parsing LOV group with attribute group links."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList/>
        <AttributeGroupList/>
        <ListOfValuesGroupList>
            <ListOfValuesGroup ID="Status">
                <Name>Status Values</Name>
                <AttributeGroupLink AttributeGroupID="Workflow"/>
                <AttributeGroupLink AttributeGroupID="State"/>
            </ListOfValuesGroup>
        </ListOfValuesGroupList>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.list_of_values_groups) == 1, "Expected 1 LOV group"
    group = parser.list_of_values_groups[0]
    
    assert "AttributeGroupLink" in group, "AttributeGroupLinks not parsed"
    assert len(group["AttributeGroupLink"]) == 2, "Expected 2 links"
    assert group["AttributeGroupLink"][0] == "Workflow", "First link not correct"
    
    print("✓ LOV group with links parsed correctly")
    return True


def test_parse_complex_attribute_system():
    """Test complex attribute system with all three element types."""
    xml_str = '''
    <STEP-ProductInformation>
        <AttributeList>
            <Attribute ID="Dimension" MultiValued="true" Mandatory="true">
                <Name xml:lang="en">Dimension</Name>
                <Validation Base="Number"/>
                <DimensionLink DimensionID="Size"/>
            </Attribute>
            <Attribute ID="Color" MultiValued="false">
                <Name xml:lang="en">Color</Name>
                <ListOfValueLink LOVID="ColorLOV"/>
            </Attribute>
        </AttributeList>
        <AttributeGroupList>
            <AttributeGroup ID="Physical">
                <Name>Physical Properties</Name>
                <AttributeGroup ID="Dimensions">
                    <Name>Dimensions</Name>
                </AttributeGroup>
            </AttributeGroup>
        </AttributeGroupList>
        <ListOfValuesGroupList>
            <ListOfValuesGroup ID="Visual" ParentID="Main">
                <Name>Visual Properties</Name>
                <ListOfValuesGroup ID="Colors">
                    <Name>Color Groups</Name>
                </ListOfValuesGroup>
            </ListOfValuesGroup>
        </ListOfValuesGroupList>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    # Verify attributes
    assert len(parser.attributes) == 2, "Expected 2 attributes"
    assert parser.attributes[0]["ID"] == "Dimension", "First attribute not correct"
    assert parser.attributes[1]["ID"] == "Color", "Second attribute not correct"
    
    # Verify attribute groups
    assert len(parser.attribute_groups) == 1, "Expected 1 root attribute group"
    assert parser.attribute_groups[0]["ID"] == "Physical", "Group ID not correct"
    assert len(parser.attribute_groups[0]["AttributeGroup"]) == 1, "Expected 1 nested group"
    
    # Verify LOV groups
    assert len(parser.list_of_values_groups) == 1, "Expected 1 root LOV group"
    assert parser.list_of_values_groups[0]["ID"] == "Visual", "LOV group ID not correct"
    assert parser.list_of_values_groups[0]["ParentID"] == "Main", "ParentID not parsed"
    
    print("✓ Complex attribute system parsed correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 5 Attribute System Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_single_attribute()
        print()
        test_parse_attribute_with_validation()
        print()
        test_parse_attribute_with_lov()
        print()
        test_parse_attribute_with_links()
        print()
        test_parse_single_attribute_group()
        print()
        test_parse_nested_attribute_groups()
        print()
        test_parse_attribute_group_with_metadata()
        print()
        test_parse_single_lov_group()
        print()
        test_parse_nested_lov_groups()
        print()
        test_parse_lov_group_with_links()
        print()
        test_parse_complex_attribute_system()
        
        print()
        print("=" * 70)
        print("✓ All Phase 5 attribute tests passed (11/11)!")
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
