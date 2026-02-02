#!/usr/bin/env python3
"""Unit and integration tests for Phase 3 Classification parser."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_single_classification():
    """Test parsing a single classification with basic attributes."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="CAT001" UserTypeID="CategoryType" Changed="true">
                <Name>Electronics Category</Name>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, f"Expected 1 classification, got {len(parser.classifications)}"
    classification = parser.classifications[0]
    
    assert classification["ID"] == "CAT001", "Classification ID not parsed"
    assert classification["UserTypeID"] == "CategoryType", "UserTypeID not parsed"
    assert classification["Changed"] is True, "Changed not converted to bool"
    assert classification["Name"] == "Electronics Category", "Name not parsed"
    assert classification["Selected"] is True, "Selected default should be True"
    assert classification["Referenced"] is False, "Referenced default should be False"
    
    print("✓ Single classification parsed correctly")
    return True


def test_parse_classification_with_key_values():
    """Test parsing classification with KeyValue and ParentKeyValue elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="CAT002" ParentID="PARENT_CAT">
                <Name>Subcategory</Name>
                <KeyValue KeyID="sku">CAT-002-SKU</KeyValue>
                <KeyValue KeyID="ean">4012345678901</KeyValue>
                <ParentKeyValue KeyID="parentKey">parentValue</ParentKeyValue>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    assert classification["ID"] == "CAT002", "ID not parsed"
    assert classification["ParentID"] == "PARENT_CAT", "ParentID not parsed"
    assert len(classification["KeyValue"]) == 2, "KeyValue count incorrect"
    assert classification["KeyValue"][0]["KeyID"] == "sku", "First KeyValue ID not correct"
    assert classification["KeyValue"][1]["value"] == "4012345678901", "Second KeyValue value not correct"
    assert len(classification["ParentKeyValue"]) == 1, "ParentKeyValue count incorrect"
    assert classification["ParentKeyValue"][0]["value"] == "parentValue", "ParentKeyValue not parsed"
    
    print("✓ Classification with KeyValues parsed correctly")
    return True


def test_parse_nested_classifications():
    """Test parsing hierarchical classifications (nested)."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="ROOT_CAT">
                <Name>Root Category</Name>
                <Classification ID="SUB_CAT1">
                    <Name>Subcategory 1</Name>
                </Classification>
                <Classification ID="SUB_CAT2">
                    <Name>Subcategory 2</Name>
                </Classification>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 root classification"
    root = parser.classifications[0]
    
    assert root["ID"] == "ROOT_CAT", "Root ID not parsed"
    assert "Classification" in root, "Nested classifications missing"
    nested = root["Classification"]
    assert isinstance(nested, list), "Nested classifications should be a list"
    assert len(nested) == 2, "Expected 2 nested classifications"
    
    assert nested[0]["ID"] == "SUB_CAT1", "First nested classification ID not correct"
    assert nested[0]["Name"] == "Subcategory 1", "First nested classification name not correct"
    assert nested[1]["ID"] == "SUB_CAT2", "Second nested classification ID not correct"
    assert nested[1]["Name"] == "Subcategory 2", "Second nested classification name not correct"
    
    print("✓ Nested classifications parsed correctly")
    return True


def test_parse_classification_with_product_references():
    """Test classification with product references and cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="BRAND_CAT">
                <Name>Brand Category</Name>
                <ProductReference ProductID="PROD001" Type="primary" Changed="false">
                </ProductReference>
                <ProductCrossReference ProductID="PROD002" Type="related">
                </ProductCrossReference>
                <ProductCrossReference ProductID="PROD003" Type="related">
                </ProductCrossReference>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    assert "ProductReference" in classification, "ProductReference missing"
    assert classification["ProductReference"]["ProductID"] == "PROD001", "ProductReference not parsed correctly"
    
    assert "ProductCrossReference" in classification, "ProductCrossReference missing"
    prod_cross = classification["ProductCrossReference"]
    assert isinstance(prod_cross, list), "Multiple ProductCrossReferences should be list"
    assert len(prod_cross) == 2, f"Expected 2 ProductCrossReferences, got {len(prod_cross)}"
    assert prod_cross[0]["ProductID"] == "PROD002", "First ProductCrossReference not correct"
    assert prod_cross[1]["ProductID"] == "PROD003", "Second ProductCrossReference not correct"
    
    print("✓ Classification with product references parsed correctly")
    return True


def test_parse_classification_with_classification_references():
    """Test classification-to-classification cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="MAIN_CAT">
                <Name>Main Category</Name>
                <ClassificationCrossReference ClassificationID="RELATED_CAT1" Type="related">
                </ClassificationCrossReference>
                <ClassificationCrossReference ClassificationID="RELATED_CAT2" Type="variant">
                </ClassificationCrossReference>
                <DeleteClassificationCrossReference ClassificationID="OLD_CAT" Type="obsolete" Changed="true">
                </DeleteClassificationCrossReference>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    assert "ClassificationCrossReference" in classification, "ClassificationCrossReference missing"
    class_cross = classification["ClassificationCrossReference"]
    assert isinstance(class_cross, list), "Multiple ClassificationCrossReferences should be list"
    assert len(class_cross) == 2, f"Expected 2 active ClassificationCrossReferences"
    assert class_cross[0]["ClassificationID"] == "RELATED_CAT1", "First reference not correct"
    assert class_cross[1]["ClassificationID"] == "RELATED_CAT2", "Second reference not correct"
    
    assert "DeleteClassificationCrossReference" in classification, "DeleteClassificationCrossReference missing"
    delete_ref = classification["DeleteClassificationCrossReference"]
    assert delete_ref["ClassificationID"] == "OLD_CAT", "Delete reference ID not correct"
    assert delete_ref["Changed"] is True, "Delete reference Changed not correct"
    
    print("✓ Classification-to-classification references parsed correctly")
    return True


def test_parse_classification_with_entity_references():
    """Test classification with entity cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="SUPPLIER_CAT">
                <Name>Supplier Category</Name>
                <EntityCrossReference EntityID="SUPPLIER_001" Type="supplier" Changed="false">
                </EntityCrossReference>
                <DeleteEntityCrossReference EntityID="OLD_SUPPLIER" Type="supplier" Changed="true">
                </DeleteEntityCrossReference>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    assert "EntityCrossReference" in classification, "EntityCrossReference missing"
    entity_ref = classification["EntityCrossReference"]
    assert entity_ref["EntityID"] == "SUPPLIER_001", "Entity ID not parsed"
    assert entity_ref["Type"] == "supplier", "Entity Type not parsed"
    assert entity_ref["Changed"] is False, "Entity Changed not correct"
    
    assert "DeleteEntityCrossReference" in classification, "DeleteEntityCrossReference missing"
    delete_ref = classification["DeleteEntityCrossReference"]
    assert delete_ref["EntityID"] == "OLD_SUPPLIER", "Delete entity ID not correct"
    
    print("✓ Classification with entity references parsed correctly")
    return True


def test_parse_classification_with_asset_references():
    """Test classification with asset cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="IMAGE_CAT">
                <Name>Image Category</Name>
                <AssetCrossReference AssetID="ASSET001" Type="image" QualifierID="en_US">
                    <KeyValue KeyID="variant">thumbnail</KeyValue>
                </AssetCrossReference>
                <SuppressedAssetCrossReference AssetID="ASSET002" Type="video" Changed="true">
                </SuppressedAssetCrossReference>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    assert "AssetCrossReference" in classification, "AssetCrossReference missing"
    asset_ref = classification["AssetCrossReference"]
    assert asset_ref["AssetID"] == "ASSET001", "Asset ID not parsed"
    assert asset_ref["Type"] == "image", "Asset Type not parsed"
    assert asset_ref["QualifierID"] == "en_US", "Asset QualifierID not parsed"
    assert len(asset_ref.get("KeyValue", [])) == 1, "Asset KeyValue not parsed"
    
    assert "SuppressedAssetCrossReference" in classification, "SuppressedAssetCrossReference missing"
    suppressed = classification["SuppressedAssetCrossReference"]
    assert suppressed["AssetID"] == "ASSET002", "Suppressed asset ID not correct"
    assert suppressed["Type"] == "video", "Suppressed asset type not correct"
    assert suppressed["Changed"] is True, "Suppressed asset Changed not correct"
    
    print("✓ Classification with asset references parsed correctly")
    return True


def test_parse_classification_with_metadata():
    """Test classification with metadata."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="META_CAT">
                <Name>Category with Metadata</Name>
                <MetaData>
                    <Value AttributeID="description">A test category</Value>
                    <MultiValue AttributeID="keywords">
                        <Value>keyword1</Value>
                        <Value>keyword2</Value>
                    </MultiValue>
                </MetaData>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    assert "MetaData" in classification, "MetaData missing"
    metadata = classification["MetaData"]
    assert "description" in metadata, "Description attribute not in metadata"
    assert metadata["description"]["value"] == "A test category", "Description value not correct"
    assert "keywords" in metadata, "Keywords attribute not in metadata"
    keywords = metadata["keywords"]
    assert isinstance(keywords, list), "Keywords should be list (MultiValue)"
    assert len(keywords) == 2, "Expected 2 keywords"
    
    print("✓ Classification with metadata parsed correctly")
    return True


def test_parse_complex_classification():
    """Test complex classification with all reference types."""
    xml_str = '''
    <STEP-ProductInformation>
        <Classifications>
            <Classification ID="COMPLEX_CAT" ParentID="PARENT" UserTypeID="ComplexType" QualifierID="en_US" Changed="false">
                <Name>Complex Category</Name>
                <KeyValue KeyID="code">COMPLEX-001</KeyValue>
                <ProductReference ProductID="PROD001" Type="primary">
                </ProductReference>
                <ProductCrossReference ProductID="PROD002" Type="related">
                </ProductCrossReference>
                <ClassificationCrossReference ClassificationID="CAT001" Type="related">
                </ClassificationCrossReference>
                <EntityCrossReference EntityID="ENTITY001" Type="brand">
                </EntityCrossReference>
                <AssetCrossReference AssetID="ASSET001" Type="image">
                </AssetCrossReference>
            </Classification>
        </Classifications>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.classifications) == 1, "Expected 1 classification"
    classification = parser.classifications[0]
    
    # Verify all attributes
    assert classification["ID"] == "COMPLEX_CAT", "ID not correct"
    assert classification["ParentID"] == "PARENT", "ParentID not correct"
    assert classification["UserTypeID"] == "ComplexType", "UserTypeID not correct"
    assert classification["QualifierID"] == "en_US", "QualifierID not correct"
    assert classification["Changed"] is False, "Changed not correct"
    
    # Verify KeyValue
    assert len(classification["KeyValue"]) == 1, "KeyValue missing"
    
    # Verify all reference types present
    assert "ProductReference" in classification, "ProductReference missing"
    assert "ProductCrossReference" in classification, "ProductCrossReference missing"
    assert "ClassificationCrossReference" in classification, "ClassificationCrossReference missing"
    assert "EntityCrossReference" in classification, "EntityCrossReference missing"
    assert "AssetCrossReference" in classification, "AssetCrossReference missing"
    
    # Verify each reference parsed correctly
    assert classification["ProductReference"]["ProductID"] == "PROD001"
    assert classification["ProductCrossReference"]["ProductID"] == "PROD002"
    assert classification["ClassificationCrossReference"]["ClassificationID"] == "CAT001"
    assert classification["EntityCrossReference"]["EntityID"] == "ENTITY001"
    assert classification["AssetCrossReference"]["AssetID"] == "ASSET001"
    
    print("✓ Complex classification with all references parsed correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 3 Classification Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_single_classification()
        print()
        test_parse_classification_with_key_values()
        print()
        test_parse_nested_classifications()
        print()
        test_parse_classification_with_product_references()
        print()
        test_parse_classification_with_classification_references()
        print()
        test_parse_classification_with_entity_references()
        print()
        test_parse_classification_with_asset_references()
        print()
        test_parse_classification_with_metadata()
        print()
        test_parse_complex_classification()
        
        print()
        print("=" * 70)
        print("✓ All Phase 3 classification tests passed (9/9)!")
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
