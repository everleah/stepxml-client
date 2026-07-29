#!/usr/bin/env python3
"""Unit and integration tests for Phase 8 Link Type parsing."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_single_link_type():
    """Test parsing a single LinkType element."""
    xml_str = '''
    <STEP-ProductInformation>
        <EdgeTypes>
            <LinkType LinkTypeID="PA"/>
        </EdgeTypes>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 1, f"Expected 1 link type, got {len(parser.link_types)}"
    link_type = parser.link_types[0]
    
    assert link_type["LinkTypeID"] == "PA", "LinkTypeID not parsed"
    
    print("✓ Single LinkType parsed correctly")
    return True


def test_parse_multiple_link_types():
    """Test parsing multiple LinkType elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <EdgeTypes>
            <LinkType LinkTypeID="PA"/>
            <LinkType LinkTypeID="CA"/>
        </EdgeTypes>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 2, f"Expected 2 link types, got {len(parser.link_types)}"
    
    link_type_ids = [lt["LinkTypeID"] for lt in parser.link_types]
    assert "PA" in link_type_ids, "PA link type not found"
    assert "CA" in link_type_ids, "CA link type not found"
    
    print("✓ Multiple LinkTypes parsed correctly")
    return True


def test_parse_link_type_ca():
    """Test parsing Classification-to-Attribute link type."""
    xml_str = '''
    <STEP-ProductInformation>
        <EdgeTypes>
            <LinkType LinkTypeID="CA"/>
        </EdgeTypes>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 1, "Expected 1 link type"
    link_type = parser.link_types[0]
    
    assert link_type["LinkTypeID"] == "CA", "CA link type ID incorrect"
    
    print("✓ CA (Classification-to-Attribute) link type parsed correctly")
    return True


def test_parse_empty_edge_types():
    """Test parsing empty EdgeTypes element."""
    xml_str = '''
    <STEP-ProductInformation>
        <EdgeTypes/>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 0, "Expected 0 link types with empty EdgeTypes"
    
    print("✓ Empty EdgeTypes handled correctly")
    return True


def test_parse_no_edge_types():
    """Test parsing STEP XML with no EdgeTypes element."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 0, "Expected 0 link types with no EdgeTypes"
    
    print("✓ Missing EdgeTypes handled correctly")
    return True


def test_parse_with_namespaces():
    """Test parsing LinkTypes with XML namespaces."""
    xml_str = '''
    <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
        <EdgeTypes>
            <LinkType LinkTypeID="PA"/>
            <LinkType LinkTypeID="CA"/>
        </EdgeTypes>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 2, f"Expected 2 link types with namespace, got {len(parser.link_types)}"
    
    link_type_ids = [lt["LinkTypeID"] for lt in parser.link_types]
    assert "PA" in link_type_ids, "PA link type not found with namespace"
    assert "CA" in link_type_ids, "CA link type not found with namespace"
    
    print("✓ LinkTypes with XML namespace parsed correctly")
    return True


def test_link_types_with_other_elements():
    """Test parsing LinkTypes alongside other system elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <EdgeTypes>
            <LinkType LinkTypeID="PA"/>
        </EdgeTypes>
        <UserTypes>
            <UserType ID="Product">
                <Name>Product Type</Name>
            </UserType>
        </UserTypes>
        <ContextList>
            <Context ID="en">
                <Name>English</Name>
            </Context>
        </ContextList>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 1, "LinkTypes not parsed correctly"
    assert len(parser.user_types) == 1, "UserTypes not parsed correctly"
    assert len(parser.contexts) == 1, "Contexts not parsed correctly"
    
    assert parser.link_types[0]["LinkTypeID"] == "PA", "LinkType ID incorrect"
    assert parser.user_types[0]["ID"] == "Product", "UserType ID incorrect"
    assert parser.contexts[0]["ID"] == "en", "Context ID incorrect"
    
    print("✓ LinkTypes parsed correctly alongside other system elements")
    return True


def test_all_link_type_combinations():
    """Test parsing all possible LinkType combinations (PA and CA)."""
    xml_str = '''
    <STEP-ProductInformation>
        <EdgeTypes>
            <LinkType LinkTypeID="PA"/>
            <LinkType LinkTypeID="CA"/>
            <LinkType LinkTypeID="PA"/>
        </EdgeTypes>
        <Products/>
        <Assets/>
        <Classifications/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Attributes/>
        <AttributeGroups/>
        <ListOfValuesGroupList/>
        <ListsOfValues/>
        <UserTypes/>
        <ContextList/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.link_types) == 3, f"Expected 3 link types, got {len(parser.link_types)}"
    
    # Check that we can have duplicates (same type multiple times)
    pa_count = sum(1 for lt in parser.link_types if lt["LinkTypeID"] == "PA")
    ca_count = sum(1 for lt in parser.link_types if lt["LinkTypeID"] == "CA")
    
    assert pa_count == 2, f"Expected 2 PA link types, got {pa_count}"
    assert ca_count == 1, f"Expected 1 CA link type, got {ca_count}"
    
    print("✓ All LinkType combinations parsed correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 8 Link Type Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_single_link_type()
        print()
        test_parse_multiple_link_types()
        print()
        test_parse_link_type_ca()
        print()
        test_parse_empty_edge_types()
        print()
        test_parse_no_edge_types()
        print()
        test_parse_with_namespaces()
        print()
        test_link_types_with_other_elements()
        print()
        test_all_link_type_combinations()
        
        print()
        print("=" * 70)
        print("✓ All Phase 8 link type tests passed (8/8)!")
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
