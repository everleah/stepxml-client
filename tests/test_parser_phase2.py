#!/usr/bin/env python3
"""Quick validation that parser enhancements compile and basic structure works."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import (
    _parse_asset_reference,
    _parse_product_cross_reference,
    _parse_classification_reference,
    _parse_entity_cross_reference,
    _parse_key_value,
    _parse_metadata
)
import xml.etree.ElementTree as ET

def test_parser_functions_exist():
    """Verify all new parser functions are defined and callable."""
    functions = [
        _parse_asset_reference,
        _parse_product_cross_reference,
        _parse_classification_reference,
        _parse_entity_cross_reference,
        _parse_key_value,
        _parse_metadata
    ]
    
    for func in functions:
        assert callable(func), f"{func.__name__} is not callable"
        print(f"✓ {func.__name__} exists and is callable")
    
    return True

def test_parse_key_value():
    """Test KeyValue parsing."""
    xml_str = '<KeyValue KeyID="testKey">testValue</KeyValue>'
    element = ET.fromstring(xml_str)
    result = _parse_key_value(element)
    
    assert result["KeyID"] == "testKey", "KeyID not parsed correctly"
    assert result["value"] == "testValue", "Value not parsed correctly"
    print("✓ _parse_key_value() works correctly")
    
    return True

def test_asset_reference_parsing():
    """Test enhanced AssetCrossReference parsing."""
    xml_str = '''
    <AssetCrossReference AssetID="ASSET123" Type="image" Changed="true" QualifierID="en_US">
        <KeyValue KeyID="assetKey">keyValue</KeyValue>
    </AssetCrossReference>
    '''
    element = ET.fromstring(xml_str)
    result = _parse_asset_reference(element)
    
    assert result["AssetID"] == "ASSET123", "AssetID not parsed"
    assert result["Type"] == "image", "Type not parsed"
    assert result["Changed"] is True, "Changed not converted to bool"
    assert result["QualifierID"] == "en_US", "QualifierID not parsed"
    assert len(result["KeyValue"]) == 1, "KeyValue list not populated"
    assert result["KeyValue"][0]["KeyID"] == "assetKey", "KeyValue KeyID not parsed"
    print("✓ _parse_asset_reference() works with enhanced attributes")
    
    return True

def test_product_cross_reference_parsing():
    """Test ProductCrossReference parsing."""
    xml_str = '''
    <ProductCrossReference ProductID="PROD456" Type="bundle" Changed="false" 
                           QualifierID="en_US" MountLocation="/variants">
    </ProductCrossReference>
    '''
    element = ET.fromstring(xml_str)
    result = _parse_product_cross_reference(element)
    
    assert result["ProductID"] == "PROD456", "ProductID not parsed"
    assert result["Type"] == "bundle", "Type not parsed"
    assert result["Changed"] is False, "Changed not converted to bool"
    assert result["QualifierID"] == "en_US", "QualifierID not parsed"
    assert result["MountLocation"] == "/variants", "MountLocation not parsed"
    print("✓ _parse_product_cross_reference() works correctly")
    
    return True

def test_classification_reference_parsing():
    """Test ClassificationReference parsing."""
    xml_str = '''
    <ClassificationReference ClassificationID="CAT789" Type="category" 
                             QualifierID="fr_FR">
    </ClassificationReference>
    '''
    element = ET.fromstring(xml_str)
    result = _parse_classification_reference(element)
    
    assert result["ClassificationID"] == "CAT789", "ClassificationID not parsed"
    assert result["Type"] == "category", "Type not parsed"
    assert result["QualifierID"] == "fr_FR", "QualifierID not parsed"
    print("✓ _parse_classification_reference() works correctly")
    
    return True

def test_entity_cross_reference_parsing():
    """Test EntityCrossReference parsing."""
    xml_str = '''
    <EntityCrossReference EntityID="ENTITY101" Type="supplier" Changed="true">
    </EntityCrossReference>
    '''
    element = ET.fromstring(xml_str)
    result = _parse_entity_cross_reference(element)
    
    assert result["EntityID"] == "ENTITY101", "EntityID not parsed"
    assert result["Type"] == "supplier", "Type not parsed"
    assert result["Changed"] is True, "Changed not converted to bool"
    print("✓ _parse_entity_cross_reference() works correctly")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Parser Phase 2 Enhancements - Validation Tests")
    print("=" * 60)
    
    try:
        test_parser_functions_exist()
        print()
        test_parse_key_value()
        print()
        test_asset_reference_parsing()
        print()
        test_product_cross_reference_parsing()
        print()
        test_classification_reference_parsing()
        print()
        test_entity_cross_reference_parsing()
        
        print()
        print("=" * 60)
        print("✓ All validation tests passed!")
        print("=" * 60)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
