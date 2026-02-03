"""
Phase 13: Advanced Configuration Elements Parsing Tests

Tests for:
- BulkUpdateConfigurations (bulk operation configurations)
- DerivedEventTypes (event type definitions)
- GlobalSettings (system-wide configuration)
- ImportConfigurations (data import configurations)
- PortalConfigurations (web UI/portal settings)
"""

import pytest
from stepxmlclient.parser import Parser


class TestParseBulkUpdateConfigurations:
    """Test parsing of bulk update configurations."""
    
    def test_parse_bulk_update_configurations_minimal(self):
        """Test parsing empty BulkUpdateConfigurations."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.bulk_update_configurations, list)
        assert len(parser.bulk_update_configurations) == 0
    
    def test_parse_single_bulk_update_configuration(self):
        """Test parsing single bulk update configuration."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations>
                <BulkUpdateConfiguration ID="BULK001"/>
            </BulkUpdateConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.bulk_update_configurations) == 1
        assert parser.bulk_update_configurations[0]["ID"] == "BULK001"
    
    def test_parse_bulk_update_configuration_with_name(self):
        """Test parsing bulk update configuration with Name."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations>
                <BulkUpdateConfiguration ID="BULK001">
                    <Name>Bulk Update Config</Name>
                </BulkUpdateConfiguration>
            </BulkUpdateConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.bulk_update_configurations[0]
        assert "Name" in config
        assert config["Name"][0]["value"] == "Bulk Update Config"
    
    def test_parse_bulk_update_configuration_with_classification_reference(self):
        """Test parsing bulk update configuration with classification reference."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations>
                <BulkUpdateConfiguration ID="BULK001">
                    <Name>Bulk Config</Name>
                    <ClassificationReference ClassificationID="CLASS001"/>
                </BulkUpdateConfiguration>
            </BulkUpdateConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.bulk_update_configurations[0]
        assert "ClassificationReference" in config
        assert config["ClassificationReference"][0]["ClassificationID"] == "CLASS001"
    
    def test_parse_multiple_bulk_update_configurations(self):
        """Test parsing multiple bulk update configurations."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations>
                <BulkUpdateConfiguration ID="BULK001">
                    <Name>Config 1</Name>
                </BulkUpdateConfiguration>
                <BulkUpdateConfiguration ID="BULK002">
                    <Name>Config 2</Name>
                </BulkUpdateConfiguration>
            </BulkUpdateConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.bulk_update_configurations) == 2


class TestParseDerivedEventTypes:
    """Test parsing of derived event types."""
    
    def test_parse_derived_event_types_minimal(self):
        """Test parsing empty DerivedEventTypes."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <DerivedEventTypes/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.derived_event_types, list)
        assert len(parser.derived_event_types) == 0
    
    def test_parse_single_derived_event_type(self):
        """Test parsing single derived event type."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <DerivedEventTypes>
                <DerivedEventType>ProductUpdated</DerivedEventType>
            </DerivedEventTypes>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.derived_event_types) == 1
        assert parser.derived_event_types[0]["value"] == "ProductUpdated"
    
    def test_parse_multiple_derived_event_types(self):
        """Test parsing multiple derived event types."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <DerivedEventTypes>
                <DerivedEventType>ProductUpdated</DerivedEventType>
                <DerivedEventType>ProductDeleted</DerivedEventType>
                <DerivedEventType>ProductCreated</DerivedEventType>
            </DerivedEventTypes>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.derived_event_types) == 3
        values = [et["value"] for et in parser.derived_event_types]
        assert "ProductUpdated" in values
        assert "ProductDeleted" in values
        assert "ProductCreated" in values


class TestParseGlobalSettings:
    """Test parsing of global settings."""
    
    def test_parse_global_settings_minimal(self):
        """Test parsing empty GlobalSettings."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <GlobalSettings/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.global_settings, dict)
        assert len(parser.global_settings) == 0
    
    def test_parse_global_settings_with_calculated_attributes(self):
        """Test parsing global settings with CalculatedAttributeSettings."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <GlobalSettings>
                <CalculatedAttributeSettings/>
            </GlobalSettings>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "CalculatedAttributeSettings" in parser.global_settings
    
    def test_parse_global_settings_with_asset_settings(self):
        """Test parsing global settings with AssetSettings."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <GlobalSettings>
                <AssetSettings/>
            </GlobalSettings>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "AssetSettings" in parser.global_settings
    
    def test_parse_global_settings_with_both_settings(self):
        """Test parsing global settings with both child elements."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <GlobalSettings>
                <CalculatedAttributeSettings/>
                <AssetSettings/>
            </GlobalSettings>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert "CalculatedAttributeSettings" in parser.global_settings
        assert "AssetSettings" in parser.global_settings


class TestParseImportConfigurations:
    """Test parsing of import configurations."""
    
    def test_parse_import_configurations_minimal(self):
        """Test parsing empty ImportConfigurations."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ImportConfigurations/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.import_configurations, list)
        assert len(parser.import_configurations) == 0
    
    def test_parse_single_import_configuration(self):
        """Test parsing single import configuration."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ImportConfigurations>
                <ImportConfiguration ID="IMP001"/>
            </ImportConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.import_configurations) == 1
        assert parser.import_configurations[0]["ID"] == "IMP001"
    
    def test_parse_import_configuration_with_name(self):
        """Test parsing import configuration with Name."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ImportConfigurations>
                <ImportConfiguration ID="IMP001">
                    <Name>CSV Import</Name>
                </ImportConfiguration>
            </ImportConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.import_configurations[0]
        assert "Name" in config
        assert config["Name"][0]["value"] == "CSV Import"
    
    def test_parse_import_configuration_with_classification_reference(self):
        """Test parsing import configuration with classification reference."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ImportConfigurations>
                <ImportConfiguration ID="IMP001">
                    <Name>Import Config</Name>
                    <ClassificationReference ClassificationID="CLASS001"/>
                </ImportConfiguration>
            </ImportConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.import_configurations[0]
        assert "ClassificationReference" in config
    
    def test_parse_multiple_import_configurations(self):
        """Test parsing multiple import configurations."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ImportConfigurations>
                <ImportConfiguration ID="IMP001">
                    <Name>CSV Import</Name>
                </ImportConfiguration>
                <ImportConfiguration ID="IMP002">
                    <Name>XML Import</Name>
                </ImportConfiguration>
            </ImportConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.import_configurations) == 2


class TestParsePortalConfigurations:
    """Test parsing of portal/web UI configurations."""
    
    def test_parse_portal_configurations_minimal(self):
        """Test parsing empty PortalConfigurations."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations/>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert isinstance(parser.portal_configurations, list)
        assert len(parser.portal_configurations) == 0
    
    def test_parse_single_portal_configuration(self):
        """Test parsing single portal configuration."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001"/>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.portal_configurations) == 1
        config = parser.portal_configurations[0]
        assert config["ID"] == "PORTAL001"
        assert config["Selected"] == True  # default
        assert config["Referenced"] == False  # default
        assert config["Changed"] == False  # default
    
    def test_parse_portal_configuration_with_attributes(self):
        """Test parsing portal configuration with all attributes."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001" Selected="true" Referenced="true" Changed="true"/>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.portal_configurations[0]
        assert config["Selected"] == True
        assert config["Referenced"] == True
        assert config["Changed"] == True
    
    def test_parse_portal_configuration_with_name(self):
        """Test parsing portal configuration with Name."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <Name>Portal Name</Name>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.portal_configurations[0]
        assert "Name" in config
        assert config["Name"][0]["value"] == "Portal Name"
    
    def test_parse_portal_configuration_with_setup_group_link(self):
        """Test parsing portal configuration with SetupGroupLink."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <SetupGroupLink ID="SETUP001"/>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.portal_configurations[0]
        assert "SetupGroupLink" in config
        assert config["SetupGroupLink"]["ID"] == "SETUP001"
    
    def test_parse_multiple_portal_configurations(self):
        """Test parsing multiple portal configurations."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <Name>Portal 1</Name>
                </PortalConfiguration>
                <PortalConfiguration ID="PORTAL002">
                    <Name>Portal 2</Name>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.portal_configurations) == 2


class TestPhase13Integration:
    """Integration tests for all Phase 13 elements."""
    
    def test_parse_all_phase13_elements(self):
        """Test parsing document with all Phase 13 elements."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations>
                <BulkUpdateConfiguration ID="BULK001">
                    <Name>Bulk Config</Name>
                </BulkUpdateConfiguration>
            </BulkUpdateConfigurations>
            <DerivedEventTypes>
                <DerivedEventType>ProductUpdated</DerivedEventType>
            </DerivedEventTypes>
            <GlobalSettings>
                <CalculatedAttributeSettings/>
            </GlobalSettings>
            <ImportConfigurations>
                <ImportConfiguration ID="IMP001">
                    <Name>Import Config</Name>
                </ImportConfiguration>
            </ImportConfigurations>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <Name>Portal Config</Name>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.bulk_update_configurations) == 1
        assert len(parser.derived_event_types) == 1
        assert len(parser.global_settings) > 0
        assert len(parser.import_configurations) == 1
        assert len(parser.portal_configurations) == 1
    
    def test_parse_phase13_with_earlier_phases(self):
        """Test parsing Phase 13 together with earlier phase elements."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <Products>
                <Product ID="PROD001">
                    <Name>Product 1</Name>
                </Product>
            </Products>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <Name>Portal Config</Name>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        # Verify earlier phases still work
        assert len(parser.products) == 1
        # Verify Phase 13 works
        assert len(parser.portal_configurations) == 1


class TestPhase13EdgeCases:
    """Edge case tests for Phase 13 elements."""
    
    def test_bulk_update_configuration_without_id(self):
        """Test bulk update configuration without ID attribute."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <BulkUpdateConfigurations>
                <BulkUpdateConfiguration>
                    <Name>No ID Config</Name>
                </BulkUpdateConfiguration>
            </BulkUpdateConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.bulk_update_configurations[0]
        assert config["ID"] is None
        assert "Name" in config
    
    def test_import_configuration_with_multiple_classification_references(self):
        """Test import configuration with multiple classification references."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ImportConfigurations>
                <ImportConfiguration ID="IMP001">
                    <ClassificationReference ClassificationID="CLASS001"/>
                    <ClassificationReference ClassificationID="CLASS002"/>
                    <ClassificationReference ClassificationID="CLASS003"/>
                </ImportConfiguration>
            </ImportConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.import_configurations[0]
        assert len(config["ClassificationReference"]) == 3
    
    def test_portal_configuration_with_metadata(self):
        """Test portal configuration with metadata."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <Name>Portal with Metadata</Name>
                    <MetaData>
                        <Attribute Name="Version" Value="1.0"/>
                    </MetaData>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        config = parser.portal_configurations[0]
        assert "MetaData" in config
    
    def test_derived_event_types_with_empty_elements(self):
        """Test derived event types with empty elements mixed with values."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <DerivedEventTypes>
                <DerivedEventType>ProductUpdated</DerivedEventType>
                <DerivedEventType></DerivedEventType>
                <DerivedEventType>ProductCreated</DerivedEventType>
            </DerivedEventTypes>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        # Should only capture non-empty values
        assert len(parser.derived_event_types) >= 2


class TestPhase13BackwardCompatibility:
    """Verify Phase 13 doesn't break earlier phases."""
    
    def test_parse_phases_2_11_without_phase13(self):
        """Test that earlier phases still work without Phase 13 elements."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <Products>
                <Product ID="PROD001">
                    <Name>Test Product</Name>
                </Product>
            </Products>
            <Classifications>
                <Classification ID="CLASS001">
                    <Name>Test Classification</Name>
                </Classification>
            </Classifications>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        assert len(parser.products) == 1
        assert len(parser.classifications) == 1
        # Phase 13 should be empty
        assert len(parser.bulk_update_configurations) == 0
        assert len(parser.derived_event_types) == 0
        assert len(parser.global_settings) == 0
        assert len(parser.import_configurations) == 0
        assert len(parser.portal_configurations) == 0
    
    def test_parse_phases_12_and_13_together(self):
        """Test Phase 12 and Phase 13 together."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <STEP-ProductInformation>
            <ReplacementRules>
                <Products/>
            </ReplacementRules>
            <CollectionList>
                <Collection ID="COLL001">
                    <Name>Collection</Name>
                </Collection>
            </CollectionList>
            <PortalConfigurations>
                <PortalConfiguration ID="PORTAL001">
                    <Name>Portal</Name>
                </PortalConfiguration>
            </PortalConfigurations>
        </STEP-ProductInformation>"""
        parser = Parser()
        parser.parse_str(xml)
        # Phase 12
        assert len(parser.replacement_rules) > 0
        assert len(parser.collections) == 1
        # Phase 13
        assert len(parser.portal_configurations) == 1
