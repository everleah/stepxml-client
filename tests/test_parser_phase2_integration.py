#!/usr/bin/env python3
"""Integration tests for Phase 2 parser with realistic XML examples."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET

def test_parse_product_with_asset_reference():
    """Test parsing a product with asset cross-reference."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="PROD001" ParentId="PARENT" UserTypeID="TYPE1">
                <Name>Test Product</Name>
                <AssetCrossReference AssetID="ASSET123" Type="image" 
                                     Changed="true" QualifierID="en_US">
                    <KeyValue KeyID="assetKey">keyValue</KeyValue>
                </AssetCrossReference>
            </Product>
        </Products>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, f"Expected 1 product, got {len(parser.products)}"
    product = parser.products[0]
    
    assert product["ID"] == "PROD001", "Product ID not parsed"
    assert product["Name"] == "Test Product", "Product Name not parsed"
    assert "AssetCrossReference" in product, "AssetCrossReference missing"
    
    asset_ref = product["AssetCrossReference"]
    assert asset_ref["AssetID"] == "ASSET123", "AssetID not parsed"
    assert asset_ref["Type"] == "image", "Type not parsed"
    assert asset_ref["Changed"] is True, "Changed not converted to bool"
    assert asset_ref["QualifierID"] == "en_US", "QualifierID not parsed"
    assert len(asset_ref["KeyValue"]) == 1, "KeyValue list missing"
    
    print("✓ Product with AssetCrossReference parsed correctly")
    return True


def test_parse_product_with_product_reference():
    """Test parsing a product with product cross-reference (bundle)."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="BUNDLE001">
                <Name>Bundle Product</Name>
                <ProductCrossReference ProductID="COMP001" Type="component" 
                                       MountLocation="/components[0]" Changed="false">
                </ProductCrossReference>
                <ProductCrossReference ProductID="COMP002" Type="component" 
                                       MountLocation="/components[1]" Changed="false">
                </ProductCrossReference>
            </Product>
        </Products>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, "Expected 1 product"
    product = parser.products[0]
    
    assert product["ID"] == "BUNDLE001", "Bundle ID not parsed"
    assert isinstance(product["ProductCrossReference"], list), "Multiple ProductCrossReferences should be a list"
    assert len(product["ProductCrossReference"]) == 2, f"Expected 2 component refs, got {len(product['ProductCrossReference'])}"
    
    comp1 = product["ProductCrossReference"][0]
    assert comp1["ProductID"] == "COMP001", "Component 1 ID not parsed"
    assert comp1["Type"] == "component", "Component 1 Type not parsed"
    assert comp1["MountLocation"] == "/components[0]", "Component 1 MountLocation not parsed"
    assert comp1["Changed"] is False, "Component 1 Changed not False"
    
    comp2 = product["ProductCrossReference"][1]
    assert comp2["ProductID"] == "COMP002", "Component 2 ID not parsed"
    assert comp2["MountLocation"] == "/components[1]", "Component 2 MountLocation not parsed"
    
    print("✓ Product with multiple ProductCrossReferences parsed correctly")
    return True


def test_parse_product_with_classification_reference():
    """Test parsing a product with classification reference."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="PROD002">
                <Name>Classified Product</Name>
                <ClassificationReference ClassificationID="CAT001" Type="category" 
                                        QualifierID="en_US" Changed="true">
                </ClassificationReference>
                <ClassificationCrossReference ClassificationID="CAT002" Type="alternate" 
                                             QualifierID="fr_FR">
                </ClassificationCrossReference>
            </Product>
        </Products>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, "Expected 1 product"
    product = parser.products[0]
    
    # Check both types of classification references are parsed
    assert "ClassificationReference" in product, "ClassificationReference missing"
    assert "ClassificationCrossReference" in product, "ClassificationCrossReference missing"
    
    cat_ref = product["ClassificationReference"]
    assert cat_ref["ClassificationID"] == "CAT001", "Classification 1 ID not parsed"
    assert cat_ref["Type"] == "category", "Classification 1 Type not parsed"
    assert cat_ref["Changed"] is True, "Classification 1 Changed not True"
    
    cross_ref = product["ClassificationCrossReference"]
    assert cross_ref["ClassificationID"] == "CAT002", "Classification 2 ID not parsed"
    assert cross_ref["QualifierID"] == "fr_FR", "Classification 2 QualifierID not parsed"
    
    print("✓ Product with ClassificationReferences parsed correctly")
    return True


def test_parse_product_with_entity_reference():
    """Test parsing a product with entity cross-reference."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="PROD003">
                <Name>Product with Entity</Name>
                <EntityCrossReference EntityID="SUPPLIER001" Type="supplier" Changed="false">
                </EntityCrossReference>
                <DeleteEntityCrossReference EntityID="OLDSUPP001" Type="supplier" Changed="true">
                </DeleteEntityCrossReference>
            </Product>
        </Products>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, "Expected 1 product"
    product = parser.products[0]
    
    assert "EntityCrossReference" in product, "EntityCrossReference missing"
    assert "DeleteEntityCrossReference" in product, "DeleteEntityCrossReference missing"
    
    entity_ref = product["EntityCrossReference"]
    assert entity_ref["EntityID"] == "SUPPLIER001", "Entity ID not parsed"
    assert entity_ref["Type"] == "supplier", "Entity Type not parsed"
    assert entity_ref["Changed"] is False, "Entity Changed not False"
    
    delete_ref = product["DeleteEntityCrossReference"]
    assert delete_ref["EntityID"] == "OLDSUPP001", "Delete Entity ID not parsed"
    assert delete_ref["Changed"] is True, "Delete Entity Changed not True"
    
    print("✓ Product with EntityCrossReferences parsed correctly")
    return True


def test_parse_delete_asset_reference():
    """Test parsing delete asset cross-reference."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="PROD004">
                <Name>Product with Delete Reference</Name>
                <DeleteAssetCrossReference AssetID="OLD_ASSET" Type="image" Changed="true">
                    <KeyValue KeyID="oldKey">oldValue</KeyValue>
                </DeleteAssetCrossReference>
            </Product>
        </Products>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, "Expected 1 product"
    product = parser.products[0]
    
    assert "DeleteAssetCrossReference" in product, "DeleteAssetCrossReference missing"
    
    delete_ref = product["DeleteAssetCrossReference"]
    assert delete_ref["AssetID"] == "OLD_ASSET", "Asset ID not parsed"
    assert delete_ref["Type"] == "image", "Type not parsed"
    assert delete_ref["Changed"] is True, "Changed not True"
    assert len(delete_ref["KeyValue"]) == 1, "KeyValue list missing"
    assert delete_ref["KeyValue"][0]["value"] == "oldValue", "KeyValue value not parsed"
    
    print("✓ DeleteAssetCrossReference parsed correctly")
    return True


def test_mixed_references():
    """Test parsing a complex product with multiple reference types."""
    xml_str = '''
    <STEP-ProductInformation>
        <Products>
            <Product ID="COMPLEX001">
                <Name>Complex Product</Name>
                <AssetCrossReference AssetID="IMAGE001" Type="image" Changed="false">
                </AssetCrossReference>
                <ProductCrossReference ProductID="RELATED001" Type="related" Changed="false">
                </ProductCrossReference>
                <ClassificationReference ClassificationID="CAT100" Type="category">
                </ClassificationReference>
                <EntityCrossReference EntityID="BRAND001" Type="brand">
                </EntityCrossReference>
            </Product>
        </Products>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.products) == 1, "Expected 1 product"
    product = parser.products[0]
    
    # Verify all reference types are present
    assert "AssetCrossReference" in product, "Missing AssetCrossReference"
    assert "ProductCrossReference" in product, "Missing ProductCrossReference"
    assert "ClassificationReference" in product, "Missing ClassificationReference"
    assert "EntityCrossReference" in product, "Missing EntityCrossReference"
    
    # Verify IDs
    assert product["AssetCrossReference"]["AssetID"] == "IMAGE001"
    assert product["ProductCrossReference"]["ProductID"] == "RELATED001"
    assert product["ClassificationReference"]["ClassificationID"] == "CAT100"
    assert product["EntityCrossReference"]["EntityID"] == "BRAND001"
    
    print("✓ Complex product with mixed references parsed correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 2 Integration Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_product_with_asset_reference()
        print()
        test_parse_product_with_product_reference()
        print()
        test_parse_product_with_classification_reference()
        print()
        test_parse_product_with_entity_reference()
        print()
        test_parse_delete_asset_reference()
        print()
        test_mixed_references()
        
        print()
        print("=" * 70)
        print("✓ All integration tests passed (6/6)!")
        print("=" * 70)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
