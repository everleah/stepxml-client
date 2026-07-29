#!/usr/bin/env python
"""Phase 7 System Configuration Tests - UserType and Context Parsing"""

import xml.etree.ElementTree as ET
from stepxmlclient.parser import Parser


def test_parse_single_user_type():
    """Test parsing a single UserType element."""
    xml = '''<STEP-ProductInformation>
        <UserTypes>
            <UserType ID="Product">
                <Name>Product Object Type</Name>
            </UserType>
        </UserTypes>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.user_types) == 1
    user_type = parser.user_types[0]
    assert user_type["ID"] == "Product"
    assert user_type["Name"][0] == "Product Object Type"
    assert user_type["Selected"] == True
    print("✓ Single UserType parsed correctly")


def test_parse_user_type_with_all_attributes():
    """Test UserType with all attribute types."""
    xml = '''<STEP-ProductInformation>
        <UserTypes>
            <UserType ID="Classification" AllowOverlappingTerms="true" AllowQuarkTemplate="false" AllowInDesignTemplate="true" IsCategory="true" ClassificationOwnsProductLinks="true" ManuallySorted="true" Selected="true" Referenced="false" Changed="true" Deleted="false">
                <Name>Classification Type</Name>
            </UserType>
        </UserTypes>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.user_types) == 1
    user_type = parser.user_types[0]
    assert user_type["ID"] == "Classification"
    assert user_type["AllowOverlappingTerms"] == True
    assert user_type["AllowQuarkTemplate"] == False
    assert user_type["IsCategory"] == True
    assert user_type["Selected"] == True
    assert user_type["Changed"] == True
    print("✓ UserType with all attributes parsed correctly")


def test_parse_user_type_with_links():
    """Test UserType with dimension, user type, and attribute links."""
    xml = '''<STEP-ProductInformation>
        <UserTypes>
            <UserType ID="Supplier">
                <Name>Supplier Object Type</Name>
                <DimensionLink DimensionID="Context"/>
                <DimensionLink DimensionID="Language"/>
                <UserTypeLink UserTypeID="Organization"/>
                <AttributeLink AttributeID="SupplierName"/>
                <AttributeLink AttributeID="SupplierCode"/>
            </UserType>
        </UserTypes>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.user_types) == 1
    user_type = parser.user_types[0]
    assert user_type["ID"] == "Supplier"
    assert len(user_type["DimensionLink"]) == 2
    assert "Context" in user_type["DimensionLink"]
    assert len(user_type["UserTypeLink"]) == 1
    assert len(user_type["AttributeLink"]) == 2
    print("✓ UserType with links parsed correctly")


def test_parse_single_context():
    """Test parsing a single Context element."""
    xml = '''<STEP-ProductInformation>
        <ContextList>
            <Context ID="en_US">
                <Name>English (US)</Name>
            </Context>
        </ContextList>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.contexts) == 1
    context = parser.contexts[0]
    assert context["ID"] == "en_US"
    assert context["Name"][0] == "English (US)"
    assert context["Selected"] == True
    assert context["Priority"] == "0"
    print("✓ Single Context parsed correctly")


def test_parse_context_with_attributes():
    """Test Context with all attributes including locale and priority."""
    xml = '''<STEP-ProductInformation>
        <ContextList>
            <Context ID="fr_FR" Priority="1" Locale="fr_FR" Selected="true" Referenced="false" Changed="true" Deleted="false">
                <Name>French (France)</Name>
            </Context>
        </ContextList>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.contexts) == 1
    context = parser.contexts[0]
    assert context["ID"] == "fr_FR"
    assert context["Priority"] == "1"
    assert context["Locale"] == "fr_FR"
    assert context["Selected"] == True
    assert context["Changed"] == True
    print("✓ Context with attributes parsed correctly")


def test_parse_context_with_dimension_points():
    """Test Context with DimensionPointLink references."""
    xml = '''<STEP-ProductInformation>
        <ContextList>
            <Context ID="CTX001">
                <Name>Context 1</Name>
                <DimensionPointLink DimensionPointID="DP001"/>
                <DimensionPointLink DimensionPointID="DP002"/>
            </Context>
        </ContextList>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.contexts) == 1
    context = parser.contexts[0]
    assert context["ID"] == "CTX001"
    assert len(context["DimensionPointLink"]) == 2
    assert "DP001" in context["DimensionPointLink"]
    print("✓ Context with dimension points parsed correctly")


def test_parse_multiple_user_types():
    """Test parsing multiple UserTypes in a single document."""
    xml = '''<STEP-ProductInformation>
        <UserTypes>
            <UserType ID="Product">
                <Name>Product</Name>
                <DimensionLink DimensionID="Context"/>
            </UserType>
            <UserType ID="Classification">
                <Name>Classification</Name>
                <UserTypeLink UserTypeID="Product"/>
            </UserType>
            <UserType ID="Asset">
                <Name>Asset</Name>
                <AttributeLink AttributeID="AssetName"/>
            </UserType>
        </UserTypes>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.user_types) == 3
    ids = [ut["ID"] for ut in parser.user_types]
    assert "Product" in ids
    assert "Classification" in ids
    assert "Asset" in ids
    print("✓ Multiple UserTypes parsed correctly")


def test_parse_multiple_contexts():
    """Test parsing multiple Contexts in a single document."""
    xml = '''<STEP-ProductInformation>
        <ContextList>
            <Context ID="en_US" Priority="0" Locale="en_US">
                <Name>English (US)</Name>
            </Context>
            <Context ID="de_DE" Priority="1" Locale="de_DE">
                <Name>German (Germany)</Name>
            </Context>
            <Context ID="fr_FR" Priority="2" Locale="fr_FR">
                <Name>French (France)</Name>
            </Context>
        </ContextList>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.contexts) == 3
    ids = [ctx["ID"] for ctx in parser.contexts]
    assert "en_US" in ids
    assert "de_DE" in ids
    assert "fr_FR" in ids
    print("✓ Multiple Contexts parsed correctly")


def test_parse_complex_system():
    """Test complex system with multiple UserTypes and Contexts together."""
    xml = '''<STEP-ProductInformation>
        <UserTypes>
            <UserType ID="Product" Selected="true">
                <Name>Product Type</Name>
                <DimensionLink DimensionID="Context"/>
                <DimensionLink DimensionID="Language"/>
                <AttributeLink AttributeID="ProductName"/>
                <AttributeLink AttributeID="ProductCode"/>
                <MIMEType>application/pdf</MIMEType>
            </UserType>
            <UserType ID="Classification" Selected="true">
                <Name>Classification Type</Name>
                <UserTypeLink UserTypeID="Product"/>
                <AttributeLink AttributeID="ClassificationID"/>
            </UserType>
        </UserTypes>
        <ContextList>
            <Context ID="en_US" Priority="0" Locale="en_US">
                <Name>English</Name>
                <DimensionPointLink DimensionPointID="LANG_EN"/>
            </Context>
            <Context ID="de_DE" Priority="1" Locale="de_DE">
                <Name>Deutsch</Name>
                <DimensionPointLink DimensionPointID="LANG_DE"/>
            </Context>
        </ContextList>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.user_types) == 2
    assert len(parser.contexts) == 2
    print("✓ Complex system parsed correctly")


def test_parse_user_type_hierarchy():
    """Test UserType hierarchy with parent type links."""
    xml = '''<STEP-ProductInformation>
        <UserTypes>
            <UserType ID="Entity">
                <Name>Base Entity</Name>
            </UserType>
            <UserType ID="Organization">
                <Name>Organization</Name>
                <UserTypeLink UserTypeID="Entity"/>
            </UserType>
            <UserType ID="Company">
                <Name>Company</Name>
                <UserTypeLink UserTypeID="Organization"/>
                <UserTypeLink UserTypeID="Entity"/>
            </UserType>
        </UserTypes>
    </STEP-ProductInformation>'''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml))
    
    assert len(parser.user_types) == 3
    company = next(ut for ut in parser.user_types if ut["ID"] == "Company")
    assert len(company["UserTypeLink"]) == 2
    print("✓ UserType hierarchy parsed correctly")


if __name__ == '__main__':
    print("\n" + "="*80)
    print("Parser Phase 7 System Configuration Tests")
    print("="*80 + "\n")
    
    tests = [
        test_parse_single_user_type,
        test_parse_user_type_with_all_attributes,
        test_parse_user_type_with_links,
        test_parse_single_context,
        test_parse_context_with_attributes,
        test_parse_context_with_dimension_points,
        test_parse_multiple_user_types,
        test_parse_multiple_contexts,
        test_parse_complex_system,
        test_parse_user_type_hierarchy,
    ]
    
    passed = 0
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} FAILED: {e}")
    
    print("\n" + "="*80)
    print(f"✓ All Phase 7 system tests passed ({passed}/{len(tests)})!")
    print("="*80 + "\n")
