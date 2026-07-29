#!/usr/bin/env python3
"""Test namespace handling in parser - validates proper support for STEP servers."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_with_namespaces():
    """Test parsing XML with proper STEP namespaces (as sent by real servers)."""
    xml_str = '''
    <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
        <Products>
            <Product ID="Prod1">
                <Name>Product 1</Name>
                <Values>
                    <Value AttributeID="Description">A great product</Value>
                    <MultiValue AttributeID="Tags">
                        <Value>feature1</Value>
                        <Value>feature2</Value>
                    </MultiValue>
                </Values>
                <AssetCrossReference AssetID="Asset1" Type="Image"/>
            </Product>
        </Products>
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
    
    assert len(parser.products) == 1, "Expected 1 product"
    product = parser.products[0]
    
    assert product["ID"] == "Prod1", "Product ID not parsed"
    assert product["Name"] == "Product 1", "Product name not parsed"
    
    # Check that Values were properly parsed despite namespace
    assert "Values" in product, "Values not parsed"
    values = product["Values"]
    assert "Description" in values, "Description attribute value not parsed"
    # Values are returned as dicts with {'value': ...} when parsed
    assert values["Description"]["value"] == "A great product", "Description value incorrect"
    
    # Check multi-value support with namespace
    assert "Tags" in values, "Tags multi-value not parsed"
    assert isinstance(values["Tags"], list), "Tags should be a list"
    assert len(values["Tags"]) == 2, f"Expected 2 tag values, got {len(values['Tags'])}"
    assert values["Tags"][0]["value"] == "feature1", "First tag value incorrect"
    assert values["Tags"][1]["value"] == "feature2", "Second tag value incorrect"
    
    # Check asset reference
    assert "AssetCrossReference" in product, "AssetCrossReference not parsed"
    asset_ref = product["AssetCrossReference"]
    # Single reference is a dict, not a list
    assert asset_ref["AssetID"] == "Asset1", "AssetID not parsed"
    assert asset_ref["Type"] == "Image", "Asset type not parsed"
    
    print("✓ Namespace handling with default namespace works correctly")
    return True


def test_parse_with_prefixed_namespaces():
    """Test parsing XML with namespace prefixes (alternate server format)."""
    xml_str = '''
    <step:STEP-ProductInformation xmlns:step="http://www.stibosystems.com/step"
                                   xmlns:outputtemplate="http://www.stibosystems.com/step/outputtemplate">
        <step:Products>
            <step:Product ID="Prod2">
                <step:Name>Product 2</step:Name>
                <step:Values>
                    <step:Value AttributeID="Size">Large</step:Value>
                    <step:MultiValue AttributeID="Colors">
                        <step:Value>Red</step:Value>
                        <step:Value>Blue</step:Value>
                    </step:MultiValue>
                </step:Values>
            </step:Product>
        </step:Products>
        <step:Assets/>
        <step:Classifications/>
        <step:DeleteAssets/>
        <step:DeleteProducts/>
        <step:Attributes/>
        <step:AttributeGroups/>
        <step:ListOfValuesGroupList/>
        <step:ListsOfValues/>
        <step:UserTypes/>
        <step:ContextList/>
    </step:STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, "Expected 1 product with prefixed namespace"
    product = parser.products[0]
    
    assert product["ID"] == "Prod2", "Product ID not parsed from prefixed namespace"
    assert product["Name"] == "Product 2", "Product name not parsed from prefixed namespace"
    
    # Check values with namespace prefix
    assert "Values" in product, "Values not parsed with namespace prefix"
    values = product["Values"]
    assert "Size" in values, "Size attribute value not parsed with namespace prefix"
    assert values["Size"]["value"] == "Large", "Size value incorrect with namespace prefix"
    
    # Check multi-value with namespace prefix
    assert "Colors" in values, "Colors multi-value not parsed with namespace prefix"
    assert isinstance(values["Colors"], list), "Colors should be a list"
    assert len(values["Colors"]) == 2, f"Expected 2 colors, got {len(values['Colors'])}"
    assert values["Colors"][0]["value"] == "Red", "First color incorrect"
    assert values["Colors"][1]["value"] == "Blue", "Second color incorrect"
    
    print("✓ Namespace handling with namespace prefixes works correctly")
    return True


def test_parse_unnamespaced_fallback():
    """Test that parser still works with unnamespaced XML (backward compatibility)."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="Prod3">
                <Name>Product 3</Name>
                <Values>
                    <Value AttributeID="SKU">SKU-12345</Value>
                    <MultiValue AttributeID="Locales">
                        <Value>en</Value>
                        <Value>de</Value>
                    </MultiValue>
                </Values>
            </Product>
        </Products>
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
    
    assert len(parser.products) == 1, "Expected 1 product without namespace"
    product = parser.products[0]
    
    assert product["ID"] == "Prod3", "Product ID not parsed without namespace"
    assert "Values" in product, "Values not parsed without namespace"
    values = product["Values"]
    assert values["SKU"]["value"] == "SKU-12345", "SKU value incorrect without namespace"
    assert len(values["Locales"]) == 2, "Multi-value not parsed without namespace"
    
    print("✓ Backward compatibility maintained for unnamespaced XML")
    return True


if __name__ == "__main__":
    print("=" * 80)
    print("Namespace Handling Tests - Real Server XML Support")
    print("=" * 80)
    
    try:
        print()
        test_parse_with_namespaces()
        print()
        test_parse_with_prefixed_namespaces()
        print()
        test_parse_unnamespaced_fallback()
        
        print()
        print("=" * 80)
        print("✓ All namespace handling tests passed (3/3)!")
        print("=" * 80)
        print()
        print("Summary:")
        print("  • Default namespace (xmlns='...') - ✓ Supported")
        print("  • Namespace prefixes (step:, outputtemplate:) - ✓ Supported")
        print("  • Unnamespaced XML (backward compatibility) - ✓ Supported")
        print()
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
