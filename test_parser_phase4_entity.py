#!/usr/bin/env python3
"""Unit and integration tests for Phase 4 Entity parser."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_single_entity():
    """Test parsing a single entity with basic attributes."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="SUPP001" UserTypeID="Supplier" Changed="true">
                <Name>Supplier One</Name>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, f"Expected 1 entity, got {len(parser.entities)}"
    entity = parser.entities[0]
    
    assert entity["ID"] == "SUPP001", "Entity ID not parsed"
    assert entity["UserTypeID"] == "Supplier", "UserTypeID not parsed"
    assert entity["Changed"] is True, "Changed not converted to bool"
    assert entity["Name"] == "Supplier One", "Name not parsed"
    assert entity["Selected"] is True, "Selected default should be True"
    assert entity["Referenced"] is False, "Referenced default should be False"
    
    print("✓ Single entity parsed correctly")
    return True


def test_parse_entity_with_key_values():
    """Test parsing entity with KeyValue and ParentKeyValue elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="MANU001" ParentID="PARENT_MANU">
                <Name>Manufacturer</Name>
                <KeyValue KeyID="code">MANU-001-CODE</KeyValue>
                <KeyValue KeyID="vat">DE123456789</KeyValue>
                <ParentKeyValue KeyID="parentKey">parentValue</ParentKeyValue>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert entity["ID"] == "MANU001", "ID not parsed"
    assert entity["ParentID"] == "PARENT_MANU", "ParentID not parsed"
    assert len(entity["KeyValue"]) == 2, "KeyValue count incorrect"
    assert entity["KeyValue"][0]["KeyID"] == "code", "First KeyValue ID not correct"
    assert entity["KeyValue"][1]["value"] == "DE123456789", "Second KeyValue value not correct"
    assert len(entity["ParentKeyValue"]) == 1, "ParentKeyValue count incorrect"
    
    print("✓ Entity with KeyValues parsed correctly")
    return True


def test_parse_nested_entities():
    """Test parsing hierarchical entities (nested)."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="ORG001">
                <Name>Organization</Name>
                <Entity ID="DIV001">
                    <Name>Division 1</Name>
                </Entity>
                <Entity ID="DIV002">
                    <Name>Division 2</Name>
                </Entity>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 root entity"
    root = parser.entities[0]
    
    assert root["ID"] == "ORG001", "Root ID not parsed"
    assert "Entity" in root, "Nested entities missing"
    nested = root["Entity"]
    assert isinstance(nested, list), "Nested entities should be a list"
    assert len(nested) == 2, "Expected 2 nested entities"
    
    assert nested[0]["ID"] == "DIV001", "First nested entity ID not correct"
    assert nested[1]["ID"] == "DIV002", "Second nested entity ID not correct"
    
    print("✓ Nested entities parsed correctly")
    return True


def test_parse_entity_with_product_references():
    """Test entity with product cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="BRAND001">
                <Name>Brand Entity</Name>
                <ProductCrossReference ProductID="PROD001" Type="branded" Changed="false">
                </ProductCrossReference>
                <ProductCrossReference ProductID="PROD002" Type="branded">
                </ProductCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "ProductCrossReference" in entity, "ProductCrossReference missing"
    prod_cross = entity["ProductCrossReference"]
    assert isinstance(prod_cross, list), "Multiple ProductCrossReferences should be list"
    assert len(prod_cross) == 2, f"Expected 2 ProductCrossReferences, got {len(prod_cross)}"
    assert prod_cross[0]["ProductID"] == "PROD001", "First ProductCrossReference not correct"
    assert prod_cross[1]["ProductID"] == "PROD002", "Second ProductCrossReference not correct"
    
    print("✓ Entity with product references parsed correctly")
    return True


def test_parse_entity_with_classification_references():
    """Test entity with classification cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="CAT_ENT">
                <Name>Category Entity</Name>
                <ClassificationCrossReference ClassificationID="CAT001" Type="mapped">
                </ClassificationCrossReference>
                <DeleteClassificationCrossReference ClassificationID="OLD_CAT" Type="obsolete" Changed="true">
                </DeleteClassificationCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "ClassificationCrossReference" in entity, "ClassificationCrossReference missing"
    class_ref = entity["ClassificationCrossReference"]
    assert class_ref["ClassificationID"] == "CAT001", "Classification reference not correct"
    
    assert "DeleteClassificationCrossReference" in entity, "DeleteClassificationCrossReference missing"
    delete_ref = entity["DeleteClassificationCrossReference"]
    assert delete_ref["ClassificationID"] == "OLD_CAT", "Delete classification ID not correct"
    
    print("✓ Entity with classification references parsed correctly")
    return True


def test_parse_entity_with_entity_references():
    """Test entity-to-entity cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="PARENT_ENT">
                <Name>Parent Entity</Name>
                <EntityCrossReference EntityID="CHILD_ENT1" Type="child" Changed="false">
                </EntityCrossReference>
                <EntityCrossReference EntityID="CHILD_ENT2" Type="child">
                </EntityCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "EntityCrossReference" in entity, "EntityCrossReference missing"
    entity_cross = entity["EntityCrossReference"]
    assert isinstance(entity_cross, list), "Multiple EntityCrossReferences should be list"
    assert len(entity_cross) == 2, f"Expected 2 EntityCrossReferences"
    assert entity_cross[0]["EntityID"] == "CHILD_ENT1", "First entity reference not correct"
    assert entity_cross[1]["EntityID"] == "CHILD_ENT2", "Second entity reference not correct"
    
    print("✓ Entity-to-entity references parsed correctly")
    return True


def test_parse_entity_with_asset_references():
    """Test entity with asset cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="DOC_ENT">
                <Name>Document Entity</Name>
                <AssetCrossReference AssetID="DOC001" Type="document" QualifierID="en_US">
                    <KeyValue KeyID="version">1.0</KeyValue>
                </AssetCrossReference>
                <SuppressedAssetCrossReference AssetID="DOC002" Type="document" Changed="true">
                </SuppressedAssetCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "AssetCrossReference" in entity, "AssetCrossReference missing"
    asset_ref = entity["AssetCrossReference"]
    assert asset_ref["AssetID"] == "DOC001", "Asset ID not parsed"
    assert asset_ref["Type"] == "document", "Asset Type not parsed"
    assert asset_ref["QualifierID"] == "en_US", "Asset QualifierID not parsed"
    assert len(asset_ref.get("KeyValue", [])) == 1, "Asset KeyValue not parsed"
    
    assert "SuppressedAssetCrossReference" in entity, "SuppressedAssetCrossReference missing"
    suppressed = entity["SuppressedAssetCrossReference"]
    assert suppressed["AssetID"] == "DOC002", "Suppressed asset ID not correct"
    
    print("✓ Entity with asset references parsed correctly")
    return True


def test_parse_entity_with_context_references():
    """Test entity with context cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="CTX_ENT">
                <Name>Context Entity</Name>
                <ContextCrossReference ContextID="CTX001" Type="mapped" QualifierID="en_US">
                </ContextCrossReference>
                <SuppressedContextCrossReference ContextID="CTX002" Type="suppressed">
                </SuppressedContextCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "ContextCrossReference" in entity, "ContextCrossReference missing"
    ctx_ref = entity["ContextCrossReference"]
    assert ctx_ref["ContextID"] == "CTX001", "Context ID not parsed"
    assert ctx_ref["Type"] == "mapped", "Context Type not parsed"
    assert ctx_ref["QualifierID"] == "en_US", "Context QualifierID not parsed"
    
    assert "SuppressedContextCrossReference" in entity, "SuppressedContextCrossReference missing"
    supp_ctx = entity["SuppressedContextCrossReference"]
    assert supp_ctx["ContextID"] == "CTX002", "Suppressed context ID not correct"
    
    print("✓ Entity with context references parsed correctly")
    return True


def test_parse_entity_with_workspace_references():
    """Test entity with workspace cross-references."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="WS_ENT">
                <Name>Workspace Entity</Name>
                <WorkspaceCrossReference WorkspaceID="WS001" Type="linked" QualifierID="en">
                </WorkspaceCrossReference>
                <SuppressedWorkspaceCrossReference WorkspaceID="WS002" Type="suppressed">
                </SuppressedWorkspaceCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "WorkspaceCrossReference" in entity, "WorkspaceCrossReference missing"
    ws_ref = entity["WorkspaceCrossReference"]
    assert ws_ref["WorkspaceID"] == "WS001", "Workspace ID not parsed"
    assert ws_ref["Type"] == "linked", "Workspace Type not parsed"
    
    assert "SuppressedWorkspaceCrossReference" in entity, "SuppressedWorkspaceCrossReference missing"
    supp_ws = entity["SuppressedWorkspaceCrossReference"]
    assert supp_ws["WorkspaceID"] == "WS002", "Suppressed workspace ID not correct"
    
    print("✓ Entity with workspace references parsed correctly")
    return True


def test_parse_entity_with_metadata():
    """Test entity with metadata."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="META_ENT">
                <Name>Entity with Metadata</Name>
                <MetaData>
                    <Value AttributeID="description">A test entity</Value>
                    <MultiValue AttributeID="tags">
                        <Value>tag1</Value>
                        <Value>tag2</Value>
                    </MultiValue>
                </MetaData>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    assert "MetaData" in entity, "MetaData missing"
    metadata = entity["MetaData"]
    assert "description" in metadata, "Description attribute not in metadata"
    assert metadata["description"]["value"] == "A test entity", "Description value not correct"
    assert "tags" in metadata, "Tags attribute not in metadata"
    
    print("✓ Entity with metadata parsed correctly")
    return True


def test_parse_complex_entity():
    """Test complex entity with all reference types."""
    xml_str = '''
    <STEP-ProductInformation>
        <Entities>
            <Entity ID="COMPLEX_ENT" ParentID="PARENT" UserTypeID="ComplexType" QualifierID="en_US" Changed="false">
                <Name>Complex Entity</Name>
                <KeyValue KeyID="code">COMPLEX-001</KeyValue>
                <ProductCrossReference ProductID="PROD001" Type="linked">
                </ProductCrossReference>
                <ClassificationCrossReference ClassificationID="CAT001" Type="mapped">
                </ClassificationCrossReference>
                <EntityCrossReference EntityID="ENT001" Type="related">
                </EntityCrossReference>
                <AssetCrossReference AssetID="ASSET001" Type="document">
                </AssetCrossReference>
                <ContextCrossReference ContextID="CTX001" Type="context">
                </ContextCrossReference>
                <WorkspaceCrossReference WorkspaceID="WS001" Type="workspace">
                </WorkspaceCrossReference>
            </Entity>
        </Entities>
        <Products/>
        <Assets/>
        <DeleteAssets/>
        <DeleteProducts/>
        <Classifications/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.entities) == 1, "Expected 1 entity"
    entity = parser.entities[0]
    
    # Verify all attributes
    assert entity["ID"] == "COMPLEX_ENT", "ID not correct"
    assert entity["ParentID"] == "PARENT", "ParentID not correct"
    assert entity["UserTypeID"] == "ComplexType", "UserTypeID not correct"
    assert entity["QualifierID"] == "en_US", "QualifierID not correct"
    assert entity["Changed"] is False, "Changed not correct"
    
    # Verify all reference types present
    assert "ProductCrossReference" in entity, "ProductCrossReference missing"
    assert "ClassificationCrossReference" in entity, "ClassificationCrossReference missing"
    assert "EntityCrossReference" in entity, "EntityCrossReference missing"
    assert "AssetCrossReference" in entity, "AssetCrossReference missing"
    assert "ContextCrossReference" in entity, "ContextCrossReference missing"
    assert "WorkspaceCrossReference" in entity, "WorkspaceCrossReference missing"
    
    # Verify each reference
    assert entity["ProductCrossReference"]["ProductID"] == "PROD001"
    assert entity["ClassificationCrossReference"]["ClassificationID"] == "CAT001"
    assert entity["EntityCrossReference"]["EntityID"] == "ENT001"
    assert entity["AssetCrossReference"]["AssetID"] == "ASSET001"
    assert entity["ContextCrossReference"]["ContextID"] == "CTX001"
    assert entity["WorkspaceCrossReference"]["WorkspaceID"] == "WS001"
    
    print("✓ Complex entity with all references parsed correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 4 Entity Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_single_entity()
        print()
        test_parse_entity_with_key_values()
        print()
        test_parse_nested_entities()
        print()
        test_parse_entity_with_product_references()
        print()
        test_parse_entity_with_classification_references()
        print()
        test_parse_entity_with_entity_references()
        print()
        test_parse_entity_with_asset_references()
        print()
        test_parse_entity_with_context_references()
        print()
        test_parse_entity_with_workspace_references()
        print()
        test_parse_entity_with_metadata()
        print()
        test_parse_complex_entity()
        
        print()
        print("=" * 70)
        print("✓ All Phase 4 entity tests passed (11/11)!")
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
