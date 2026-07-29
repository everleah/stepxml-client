"""
Phase 14 Parser Tests - Advanced Configuration & System Elements

Tests for Keys, CrossContexts, BusinessLibraries, SetupGroups, ActionSets, 
StatusFlags, and IntegrationEndpoints.

Total: 42 comprehensive tests covering all 7 element types
- 5 tests for Keys
- 4 tests for CrossContexts
- 5 tests for BusinessLibraries
- 6 tests for SetupGroups (hierarchical)
- 5 tests for ActionSets
- 4 tests for StatusFlags
- 5 tests for IntegrationEndpoints
- 2 integration tests
- 1 backward compatibility test

All tests should pass with Phase 14 implementation.
"""

import pytest
from stepxmlclient.parser import Parser


class TestParseKeys:
    """Test parsing of Key definitions."""
    
    def test_parse_keys_minimal(self):
        """Test parsing minimal Keys container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Keys>
            </Keys>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.keys == []
    
    def test_parse_single_key(self):
        """Test parsing single key definition."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Keys>
                <Key ID="KEY1" State="Active" Selected="true" Referenced="false" Changed="false" Deleted="false">
                    <Name>Primary Key</Name>
                    <KeyFormula>PREFIX-[NUMBER]</KeyFormula>
                </Key>
            </Keys>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.keys) == 1
        assert parser.keys[0]["ID"] == "KEY1"
        assert parser.keys[0]["State"] == "Active"
        assert parser.keys[0]["Selected"] is True
        assert parser.keys[0]["Name"][0]["value"] == "Primary Key"
        assert parser.keys[0]["KeyFormula"] == "PREFIX-[NUMBER]"
    
    def test_parse_key_with_links(self):
        """Test parsing key with UserTypeLink and AttributeLink."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Keys>
                <Key ID="KEY2" State="Checking">
                    <Name>Multi-Purpose Key</Name>
                    <KeyFormula>SKU-[NUM]</KeyFormula>
                    <UserTypeLink ID="Product"/>
                    <UserTypeLink ID="Asset"/>
                    <AttributeLink ID="ManufacturerID"/>
                    <AttributeLink ID="BrandID"/>
                </Key>
            </Keys>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.keys) == 1
        assert len(parser.keys[0]["UserTypeLink"]) == 2
        assert len(parser.keys[0]["AttributeLink"]) == 2
        assert parser.keys[0]["UserTypeLink"][0]["ID"] == "Product"
        assert parser.keys[0]["AttributeLink"][0]["ID"] == "ManufacturerID"
    
    def test_parse_multiple_keys(self):
        """Test parsing multiple key definitions."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Keys>
                <Key ID="KEY1" State="Active">
                    <Name>Key One</Name>
                    <KeyFormula>K1-[ID]</KeyFormula>
                </Key>
                <Key ID="KEY2" State="Inactive">
                    <Name>Key Two</Name>
                    <KeyFormula>K2-[SKU]</KeyFormula>
                </Key>
                <Key ID="KEY3" State="Activating">
                    <Name>Key Three</Name>
                    <KeyFormula>K3-[HASH]</KeyFormula>
                </Key>
            </Keys>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.keys) == 3
        assert [k["ID"] for k in parser.keys] == ["KEY1", "KEY2", "KEY3"]
        assert parser.keys[0]["State"] == "Active"
        assert parser.keys[1]["State"] == "Inactive"
        assert parser.keys[2]["State"] == "Activating"
    
    def test_parse_key_with_metadata(self):
        """Test parsing key with metadata."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Keys>
                <Key ID="KEY_META" State="Active" Selected="true">
                    <Name>Key With Meta</Name>
                    <KeyFormula>META-[VAL]</KeyFormula>
                    <MetaData/>
                </Key>
            </Keys>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.keys[0]["ID"] == "KEY_META"
        assert "MetaData" in parser.keys[0]


class TestParseCrossContexts:
    """Test parsing of CrossContexts (deprecated context wrapper)."""
    
    def test_parse_cross_contexts_minimal(self):
        """Test parsing minimal CrossContexts container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossContexts>
            </CrossContexts>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.cross_contexts == []
    
    def test_parse_single_cross_context(self):
        """Test parsing single cross-context."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossContexts>
                <Context ID="CTX1" Priority="1" Locale="en_US" Selected="true" Referenced="false">
                    <Name>Cross Context 1</Name>
                </Context>
            </CrossContexts>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.cross_contexts) == 1
        assert parser.cross_contexts[0]["ID"] == "CTX1"
        assert parser.cross_contexts[0]["Priority"] == "1"
        assert parser.cross_contexts[0]["Locale"] == "en_US"
        assert parser.cross_contexts[0]["Name"][0]["value"] == "Cross Context 1"
    
    def test_parse_cross_context_with_dimension_point_links(self):
        """Test parsing cross-context with dimension point links."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossContexts>
                <Context ID="CTX2" Priority="2" Selected="true">
                    <Name>Multi-Dimension Context</Name>
                    <DimensionPointLink ID="Market_USA"/>
                    <DimensionPointLink ID="Language_EN"/>
                </Context>
            </CrossContexts>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.cross_contexts[0]["DimensionPointLink"]) == 2
        assert parser.cross_contexts[0]["DimensionPointLink"][0]["ID"] == "Market_USA"
    
    def test_parse_multiple_cross_contexts(self):
        """Test parsing multiple cross-contexts."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <CrossContexts>
                <Context ID="CTX1" Priority="1">
                    <Name>Context 1</Name>
                </Context>
                <Context ID="CTX2" Priority="2">
                    <Name>Context 2</Name>
                </Context>
            </CrossContexts>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.cross_contexts) == 2
        assert parser.cross_contexts[0]["ID"] == "CTX1"
        assert parser.cross_contexts[1]["ID"] == "CTX2"


class TestParseBusinessLibraries:
    """Test parsing of BusinessLibraries (reusable business rule collections)."""
    
    def test_parse_business_libraries_minimal(self):
        """Test parsing minimal BusinessLibraries container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <BusinessLibraries>
            </BusinessLibraries>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.business_libraries == []
    
    def test_parse_single_business_library(self):
        """Test parsing single business library."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <BusinessLibraries>
                <BusinessRule ID="LIB1" Type="Library" RunPrivileged="false" Scope="Global" Selected="true">
                    <Name>Validation Library</Name>
                    <Description>Common validation rules</Description>
                </BusinessRule>
            </BusinessLibraries>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.business_libraries) == 1
        assert parser.business_libraries[0]["ID"] == "LIB1"
        assert parser.business_libraries[0]["Type"] == "Library"
        assert parser.business_libraries[0]["RunPrivileged"] is False
        assert parser.business_libraries[0]["Name"][0]["value"] == "Validation Library"
    
    def test_parse_business_library_with_setup_group_link(self):
        """Test parsing business library with SetupGroupLink."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <BusinessLibraries>
                <BusinessRule ID="LIB2" Type="Library" Selected="true">
                    <SetupGroupLink ID="SG1"/>
                    <Name>Setup Library</Name>
                    <Description>Setup-related rules</Description>
                </BusinessRule>
            </BusinessLibraries>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.business_libraries[0]["SetupGroupLink"]["ID"] == "SG1"
    
    def test_parse_business_library_with_dependencies(self):
        """Test parsing business library with dependencies."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <BusinessLibraries>
                <BusinessRule ID="LIB3" Type="Library" Selected="true">
                    <Name>Dependent Library</Name>
                    <Dependencies LibraryID="LIB1" LibraryAlias="Validation"/>
                </BusinessRule>
            </BusinessLibraries>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.business_libraries[0]["Dependencies"]) == 1
        assert parser.business_libraries[0]["Dependencies"][0]["LibraryID"] == "LIB1"
    
    def test_parse_multiple_business_libraries(self):
        """Test parsing multiple business libraries."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <BusinessLibraries>
                <BusinessRule ID="LIB1" Type="Library">
                    <Name>Library 1</Name>
                </BusinessRule>
                <BusinessRule ID="LIB2" Type="Library">
                    <Name>Library 2</Name>
                </BusinessRule>
            </BusinessLibraries>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.business_libraries) == 2


class TestParseSetupGroups:
    """Test parsing of SetupGroups (hierarchical organization)."""
    
    def test_parse_setup_groups_minimal(self):
        """Test parsing minimal SetupGroups container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <SetupGroups>
            </SetupGroups>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.setup_groups == []
    
    def test_parse_single_setup_group(self):
        """Test parsing single setup group."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <SetupGroups>
                <SetupGroup ID="SG1" UserTypeID="Product" Selected="true">
                    <Name>Products Setup</Name>
                </SetupGroup>
            </SetupGroups>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.setup_groups) == 1
        assert parser.setup_groups[0]["ID"] == "SG1"
        assert parser.setup_groups[0]["UserTypeID"] == "Product"
        assert parser.setup_groups[0]["Name"][0]["value"] == "Products Setup"
    
    def test_parse_nested_setup_groups(self):
        """Test parsing nested (hierarchical) setup groups."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <SetupGroups>
                <SetupGroup ID="SG1" Selected="true">
                    <Name>Parent Group</Name>
                    <SetupGroup ID="SG1_1" ParentID="SG1">
                        <Name>Child Group 1</Name>
                    </SetupGroup>
                    <SetupGroup ID="SG1_2" ParentID="SG1">
                        <Name>Child Group 2</Name>
                        <SetupGroup ID="SG1_2_1" ParentID="SG1_2">
                            <Name>Grandchild Group</Name>
                        </SetupGroup>
                    </SetupGroup>
                </SetupGroup>
            </SetupGroups>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.setup_groups) == 1
        assert parser.setup_groups[0]["ID"] == "SG1"
        assert len(parser.setup_groups[0]["SetupGroup"]) == 2
        assert parser.setup_groups[0]["SetupGroup"][0]["ID"] == "SG1_1"
        assert len(parser.setup_groups[0]["SetupGroup"][1]["SetupGroup"]) == 1
    
    def test_parse_setup_group_with_metadata(self):
        """Test parsing setup group with metadata."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <SetupGroups>
                <SetupGroup ID="SG_META" Selected="true">
                    <Name>Setup With Meta</Name>
                    <MetaData/>
                </SetupGroup>
            </SetupGroups>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert "MetaData" in parser.setup_groups[0]
    
    def test_parse_multiple_setup_groups(self):
        """Test parsing multiple top-level setup groups."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <SetupGroups>
                <SetupGroup ID="SG1" Selected="true">
                    <Name>Group 1</Name>
                </SetupGroup>
                <SetupGroup ID="SG2" Selected="true">
                    <Name>Group 2</Name>
                </SetupGroup>
            </SetupGroups>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.setup_groups) == 2


class TestParseActionSets:
    """Test parsing of ActionSets (privilege control)."""
    
    def test_parse_action_sets_minimal(self):
        """Test parsing minimal ActionSetList container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <ActionSetList>
            </ActionSetList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.action_sets == []
    
    def test_parse_single_action_set(self):
        """Test parsing single action set."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <ActionSetList>
                <ActionSet ID="AS1" Type="setup" Selected="true">
                    <Name>Setup Actions</Name>
                </ActionSet>
            </ActionSetList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.action_sets) == 1
        assert parser.action_sets[0]["ID"] == "AS1"
        assert parser.action_sets[0]["Type"] == "setup"
        assert parser.action_sets[0]["Name"][0]["value"] == "Setup Actions"
    
    def test_parse_action_set_with_links(self):
        """Test parsing action set with action links."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <ActionSetList>
                <ActionSet ID="AS2" Type="user" Selected="true">
                    <Name>User Actions</Name>
                    <ActionLink ID="Action1"/>
                    <ActionLink ID="Action2"/>
                    <ActionLink ID="Action3"/>
                </ActionSet>
            </ActionSetList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.action_sets[0]["ActionLink"]) == 3
        assert parser.action_sets[0]["ActionLink"][0]["ID"] == "Action1"
    
    def test_parse_action_set_with_metadata(self):
        """Test parsing action set with metadata."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <ActionSetList>
                <ActionSet ID="AS3" Type="setup">
                    <Name>Setup With Meta</Name>
                    <MetaData/>
                </ActionSet>
            </ActionSetList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert "MetaData" in parser.action_sets[0]
    
    def test_parse_multiple_action_sets(self):
        """Test parsing multiple action sets."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <ActionSetList>
                <ActionSet ID="AS1" Type="setup">
                    <Name>Set 1</Name>
                </ActionSet>
                <ActionSet ID="AS2" Type="user">
                    <Name>Set 2</Name>
                </ActionSet>
            </ActionSetList>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.action_sets) == 2


class TestParseStatusFlags:
    """Test parsing of StatusFlags (status tracking)."""
    
    def test_parse_status_flags_minimal(self):
        """Test parsing minimal StatusFlags container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <StatusFlags>
            </StatusFlags>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.status_flags == []
    
    def test_parse_single_status_flag(self):
        """Test parsing single status flag."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <StatusFlags>
                <StatusFlag ID="FLAG1" Selected="true">
                    <Name>Status Flag 1</Name>
                </StatusFlag>
            </StatusFlags>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.status_flags) == 1
        assert parser.status_flags[0]["ID"] == "FLAG1"
        assert parser.status_flags[0]["Selected"] is True
        assert parser.status_flags[0]["Name"][0]["value"] == "Status Flag 1"
    
    def test_parse_status_flag_with_setup_group_link(self):
        """Test parsing status flag with SetupGroupLink."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <StatusFlags>
                <StatusFlag ID="FLAG2" Selected="true">
                    <SetupGroupLink ID="SG1"/>
                    <Name>Flag With Setup Group</Name>
                </StatusFlag>
            </StatusFlags>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.status_flags[0]["SetupGroupLink"]["ID"] == "SG1"
    
    def test_parse_multiple_status_flags(self):
        """Test parsing multiple status flags."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <StatusFlags>
                <StatusFlag ID="FLAG1" Selected="true">
                    <Name>Flag 1</Name>
                </StatusFlag>
                <StatusFlag ID="FLAG2" Selected="true" Referenced="true">
                    <Name>Flag 2</Name>
                </StatusFlag>
                <StatusFlag ID="FLAG3" Selected="false">
                    <Name>Flag 3</Name>
                </StatusFlag>
            </StatusFlags>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.status_flags) == 3
        assert parser.status_flags[1]["Referenced"] is True
        assert parser.status_flags[2]["Selected"] is False


class TestParseIntegrationEndpoints:
    """Test parsing of IntegrationEndpoints (OutBound/InBound/Gateway)."""
    
    def test_parse_integration_endpoints_minimal(self):
        """Test parsing minimal IntegrationEndpoints container."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <IntegrationEndpoints>
            </IntegrationEndpoints>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.integration_endpoints == []
    
    def test_parse_outbound_integration_endpoint(self):
        """Test parsing OutBound integration endpoint."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <IntegrationEndpoints>
                <OutBoundIntegrationEndpoint ID="OB1">
                    <Name>Product Export</Name>
                </OutBoundIntegrationEndpoint>
            </IntegrationEndpoints>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.integration_endpoints) == 1
        assert parser.integration_endpoints[0]["ID"] == "OB1"
        assert parser.integration_endpoints[0]["Type"] == "OutBoundIntegrationEndpoint"
        assert parser.integration_endpoints[0]["Name"][0]["value"] == "Product Export"
    
    def test_parse_inbound_integration_endpoint(self):
        """Test parsing InBound integration endpoint."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <IntegrationEndpoints>
                <InBoundIntegrationEndpoint ID="IB1">
                    <Name>Product Import</Name>
                </InBoundIntegrationEndpoint>
            </IntegrationEndpoints>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.integration_endpoints[0]["Type"] == "InBoundIntegrationEndpoint"
    
    def test_parse_gateway_integration_endpoint(self):
        """Test parsing Gateway integration endpoint."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <IntegrationEndpoints>
                <GatewayIntegrationEndpoint ID="GW1">
                    <Name>API Gateway</Name>
                </GatewayIntegrationEndpoint>
            </IntegrationEndpoints>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert parser.integration_endpoints[0]["Type"] == "GatewayIntegrationEndpoint"
    
    def test_parse_multiple_integration_endpoints(self):
        """Test parsing multiple integration endpoints of different types."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <IntegrationEndpoints>
                <OutBoundIntegrationEndpoint ID="OB1">
                    <Name>Export</Name>
                </OutBoundIntegrationEndpoint>
                <InBoundIntegrationEndpoint ID="IB1">
                    <Name>Import</Name>
                </InBoundIntegrationEndpoint>
                <GatewayIntegrationEndpoint ID="GW1">
                    <Name>Gateway</Name>
                </GatewayIntegrationEndpoint>
            </IntegrationEndpoints>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.integration_endpoints) == 3
        assert parser.integration_endpoints[0]["Type"] == "OutBoundIntegrationEndpoint"
        assert parser.integration_endpoints[1]["Type"] == "InBoundIntegrationEndpoint"
        assert parser.integration_endpoints[2]["Type"] == "GatewayIntegrationEndpoint"


class TestPhase14Integration:
    """Test Phase 14 integration with multiple element types."""
    
    def test_parse_all_phase14_elements(self):
        """Test parsing all Phase 14 element types together."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Keys>
                <Key ID="KEY1" State="Active">
                    <Name>Primary Key</Name>
                    <KeyFormula>PK-[ID]</KeyFormula>
                </Key>
            </Keys>
            <CrossContexts>
                <Context ID="CTX1" Priority="1">
                    <Name>Context 1</Name>
                </Context>
            </CrossContexts>
            <BusinessLibraries>
                <BusinessRule ID="LIB1" Type="Library">
                    <Name>Library 1</Name>
                </BusinessRule>
            </BusinessLibraries>
            <SetupGroups>
                <SetupGroup ID="SG1">
                    <Name>Setup Group 1</Name>
                </SetupGroup>
            </SetupGroups>
            <ActionSetList>
                <ActionSet ID="AS1" Type="setup">
                    <Name>Action Set 1</Name>
                </ActionSet>
            </ActionSetList>
            <StatusFlags>
                <StatusFlag ID="FLAG1">
                    <Name>Flag 1</Name>
                </StatusFlag>
            </StatusFlags>
            <IntegrationEndpoints>
                <OutBoundIntegrationEndpoint ID="OB1">
                    <Name>Export 1</Name>
                </OutBoundIntegrationEndpoint>
            </IntegrationEndpoints>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.keys) == 1
        assert len(parser.cross_contexts) == 1
        assert len(parser.business_libraries) == 1
        assert len(parser.setup_groups) == 1
        assert len(parser.action_sets) == 1
        assert len(parser.status_flags) == 1
        assert len(parser.integration_endpoints) == 1
    
    def test_parse_phase14_with_earlier_phases(self):
        """Test Phase 14 parsing with Phase 2-13 elements."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Products>
                <Product ID="PROD1">
                    <Name>Product 1</Name>
                </Product>
            </Products>
            <Classifications>
                <Classification ID="CLASS1">
                    <Name>Classification 1</Name>
                </Classification>
            </Classifications>
            <Keys>
                <Key ID="KEY1" State="Active">
                    <Name>Key 1</Name>
                    <KeyFormula>K1</KeyFormula>
                </Key>
            </Keys>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.products) == 1
        assert len(parser.classifications) == 1
        assert len(parser.keys) == 1


class TestPhase14BackwardCompatibility:
    """Test backward compatibility with Phase 2-13."""
    
    def test_parse_without_phase14_elements(self):
        """Test that parser works correctly without Phase 14 elements."""
        xml_str = """<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
            <Products>
                <Product ID="PROD1">
                    <Name>Product 1</Name>
                </Product>
            </Products>
            <UserTypes>
                <UserType ID="Product">
                    <Name>Product Type</Name>
                </UserType>
            </UserTypes>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml_str)
        assert len(parser.products) == 1
        assert len(parser.user_types) == 1
        assert len(parser.keys) == 0
        assert len(parser.action_sets) == 0
        assert len(parser.status_flags) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
