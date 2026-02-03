#!/usr/bin/env python3
"""Unit and integration tests for Phase 9 Advanced Features parsing."""

import sys
sys.path.insert(0, '.')

from stepxmlclient.parser import Parser
import xml.etree.ElementTree as ET


def test_parse_single_business_rule():
    """Test parsing a single BusinessRule element."""
    xml_str = '''
    <STEP-ProductInformation>
        <BusinessRules>
            <BusinessRule ID="MyAction" Type="Action" Scope="Global" RunPrivileged="false">
                <Name>My Action</Name>
                <Description>Test action rule</Description>
            </BusinessRule>
        </BusinessRules>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.business_rules) == 1, f"Expected 1 business rule, got {len(parser.business_rules)}"
    rule = parser.business_rules[0]
    
    assert rule["ID"] == "MyAction", "BusinessRule ID not parsed"
    assert rule["Type"] == "Action", "BusinessRule Type not parsed"
    assert rule["Scope"] == "Global", "BusinessRule Scope not parsed"
    assert rule["RunPrivileged"] == False, "BusinessRule RunPrivileged not parsed"
    assert rule["Name"] == ["My Action"], "BusinessRule Name not parsed"
    assert rule["Description"] == "Test action rule", "BusinessRule Description not parsed"
    
    print("✓ Single BusinessRule parsed correctly")
    return True


def test_parse_multiple_business_rules():
    """Test parsing multiple BusinessRule elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <BusinessRules>
            <BusinessRule ID="Rule1" Type="Action">
                <Name>Action Rule</Name>
            </BusinessRule>
            <BusinessRule ID="Rule2" Type="Condition">
                <Name>Condition Rule</Name>
            </BusinessRule>
            <BusinessRule ID="Rule3" Type="Library">
                <Name>Library Rule</Name>
            </BusinessRule>
        </BusinessRules>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.business_rules) == 3, f"Expected 3 business rules, got {len(parser.business_rules)}"
    
    types = [rule["Type"] for rule in parser.business_rules]
    assert "Action" in types, "Action type not found"
    assert "Condition" in types, "Condition type not found"
    assert "Library" in types, "Library type not found"
    
    print("✓ Multiple BusinessRules parsed correctly")
    return True


def test_parse_single_event_queue():
    """Test parsing a single EventQueue element."""
    xml_str = '''
    <STEP-ProductInformation>
        <EventQueues>
            <EventQueue ID="MainQueue" QueueStatus="Read" DaysRetained="30" Selected="true">
                <Name>Main Event Queue</Name>
                <Configuration>encoded_config</Configuration>
            </EventQueue>
        </EventQueues>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.event_queues) == 1, f"Expected 1 event queue, got {len(parser.event_queues)}"
    queue = parser.event_queues[0]
    
    assert queue["ID"] == "MainQueue", "EventQueue ID not parsed"
    assert queue["QueueStatus"] == "Read", "EventQueue QueueStatus not parsed"
    assert queue["DaysRetained"] == "30", "EventQueue DaysRetained not parsed"
    assert queue["Selected"] == True, "EventQueue Selected not parsed"
    assert queue["Referenced"] == False, "EventQueue Referenced not correct"
    assert queue["Changed"] == False, "EventQueue Changed not correct"
    assert queue["Name"] == ["Main Event Queue"], "EventQueue Name not parsed"
    
    print("✓ Single EventQueue parsed correctly")
    return True


def test_parse_event_queue_discard_status():
    """Test parsing EventQueue with Discard status."""
    xml_str = '''
    <STEP-ProductInformation>
        <EventQueues>
            <EventQueue ID="DiscardQueue" QueueStatus="Discard">
                <Name>Discard Queue</Name>
                <Configuration>encoded</Configuration>
            </EventQueue>
        </EventQueues>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.event_queues) == 1, "Expected 1 event queue"
    queue = parser.event_queues[0]
    
    assert queue["QueueStatus"] == "Discard", "EventQueue Discard status not parsed"
    
    print("✓ EventQueue with Discard status parsed correctly")
    return True


def test_parse_single_workflow():
    """Test parsing a single STEPWorkflow element."""
    xml_str = '''
    <STEP-ProductInformation>
        <STEPWorkflows>
            <STEPWorkflow ID="ProductApproval" Selected="true">
                <Name>Product Approval Workflow</Name>
                <ValidUserTypeLink UserTypeID="Product"/>
                <ValidUserTypeLink UserTypeID="Asset"/>
            </STEPWorkflow>
        </STEPWorkflows>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.workflows) == 1, f"Expected 1 workflow, got {len(parser.workflows)}"
    workflow = parser.workflows[0]
    
    assert workflow["ID"] == "ProductApproval", "Workflow ID not parsed"
    assert workflow["Selected"] == True, "Workflow Selected not parsed"
    assert workflow["Name"] == ["Product Approval Workflow"], "Workflow Name not parsed"
    assert workflow["ValidUserTypeLink"] == ["Product", "Asset"], "Workflow ValidUserTypeLink not parsed"
    
    print("✓ Single STEPWorkflow parsed correctly")
    return True


def test_parse_multiple_workflows():
    """Test parsing multiple STEPWorkflow elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <STEPWorkflows>
            <STEPWorkflow ID="Flow1" Selected="true">
                <Name>Workflow 1</Name>
            </STEPWorkflow>
            <STEPWorkflow ID="Flow2" Selected="false">
                <Name>Workflow 2</Name>
            </STEPWorkflow>
        </STEPWorkflows>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.workflows) == 2, f"Expected 2 workflows, got {len(parser.workflows)}"
    
    ids = [w["ID"] for w in parser.workflows]
    assert "Flow1" in ids, "Flow1 not found"
    assert "Flow2" in ids, "Flow2 not found"
    
    print("✓ Multiple STEPWorkflows parsed correctly")
    return True


def test_parse_single_export_configuration():
    """Test parsing a single ExportConfiguration element."""
    xml_str = '''
    <STEP-ProductInformation>
        <ExportConfigurations>
            <ExportConfiguration ID="XMLExport">
                <Name>XML Export Config</Name>
                <ClassificationReference ClassificationID="Products"/>
                <ClassificationReference ClassificationID="Assets"/>
            </ExportConfiguration>
        </ExportConfigurations>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.export_configurations) == 1, f"Expected 1 export config, got {len(parser.export_configurations)}"
    config = parser.export_configurations[0]
    
    assert config["ID"] == "XMLExport", "ExportConfiguration ID not parsed"
    assert config["Name"] == ["XML Export Config"], "ExportConfiguration Name not parsed"
    assert config["ClassificationReference"] == ["Products", "Assets"], "ClassificationReference not parsed"
    
    print("✓ Single ExportConfiguration parsed correctly")
    return True


def test_parse_multiple_export_configurations():
    """Test parsing multiple ExportConfiguration elements."""
    xml_str = '''
    <STEP-ProductInformation>
        <ExportConfigurations>
            <ExportConfiguration ID="Export1">
                <Name>Export 1</Name>
            </ExportConfiguration>
            <ExportConfiguration ID="Export2">
                <Name>Export 2</Name>
            </ExportConfiguration>
        </ExportConfigurations>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.export_configurations) == 2, f"Expected 2 export configs, got {len(parser.export_configurations)}"
    
    ids = [c["ID"] for c in parser.export_configurations]
    assert "Export1" in ids, "Export1 not found"
    assert "Export2" in ids, "Export2 not found"
    
    print("✓ Multiple ExportConfigurations parsed correctly")
    return True


def test_parse_all_phase9_elements():
    """Test parsing all Phase 9 elements together."""
    xml_str = '''
    <STEP-ProductInformation>
        <BusinessRules>
            <BusinessRule ID="ApprovalAction" Type="Action">
                <Name>Approval Action</Name>
            </BusinessRule>
        </BusinessRules>
        <EventQueues>
            <EventQueue ID="ApprovalQueue" QueueStatus="Read">
                <Name>Approval Queue</Name>
                <Configuration>encoded</Configuration>
            </EventQueue>
        </EventQueues>
        <STEPWorkflows>
            <STEPWorkflow ID="ApprovalFlow" Selected="true">
                <Name>Approval Workflow</Name>
            </STEPWorkflow>
        </STEPWorkflows>
        <ExportConfigurations>
            <ExportConfiguration ID="ApprovalExport">
                <Name>Approval Export</Name>
            </ExportConfiguration>
        </ExportConfigurations>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.business_rules) == 1, "BusinessRule not parsed"
    assert len(parser.event_queues) == 1, "EventQueue not parsed"
    assert len(parser.workflows) == 1, "STEPWorkflow not parsed"
    assert len(parser.export_configurations) == 1, "ExportConfiguration not parsed"
    
    print("✓ All Phase 9 elements parsed correctly together")
    return True


def test_parse_with_namespaces():
    """Test parsing Phase 9 elements with XML namespaces."""
    xml_str = '''
    <STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
        <BusinessRules>
            <BusinessRule ID="Rule1" Type="Action">
                <Name>Rule 1</Name>
            </BusinessRule>
        </BusinessRules>
        <EventQueues>
            <EventQueue ID="Queue1" QueueStatus="Read">
                <Name>Queue 1</Name>
                <Configuration>encoded</Configuration>
            </EventQueue>
        </EventQueues>
        <STEPWorkflows>
            <STEPWorkflow ID="Flow1" Selected="true">
                <Name>Flow 1</Name>
            </STEPWorkflow>
        </STEPWorkflows>
        <ExportConfigurations>
            <ExportConfiguration ID="Export1">
                <Name>Export 1</Name>
            </ExportConfiguration>
        </ExportConfigurations>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.business_rules) == 1, "BusinessRule not parsed with namespace"
    assert len(parser.event_queues) == 1, "EventQueue not parsed with namespace"
    assert len(parser.workflows) == 1, "STEPWorkflow not parsed with namespace"
    assert len(parser.export_configurations) == 1, "ExportConfiguration not parsed with namespace"
    
    print("✓ All Phase 9 elements parsed correctly with namespaces")
    return True


def test_empty_phase9_containers():
    """Test parsing empty Phase 9 containers."""
    xml_str = '''
    <STEP-ProductInformation>
        <BusinessRules/>
        <EventQueues/>
        <STEPWorkflows/>
        <ExportConfigurations/>
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.business_rules) == 0, "Expected 0 business rules"
    assert len(parser.event_queues) == 0, "Expected 0 event queues"
    assert len(parser.workflows) == 0, "Expected 0 workflows"
    assert len(parser.export_configurations) == 0, "Expected 0 export configs"
    
    print("✓ Empty Phase 9 containers handled correctly")
    return True


def test_missing_phase9_elements():
    """Test parsing STEP XML with missing Phase 9 elements."""
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
        <EdgeTypes/>
    </STEP-ProductInformation>
    '''
    
    parser = Parser()
    parser.parse(ET.fromstring(xml_str))
    
    assert len(parser.business_rules) == 0, "Expected 0 business rules when missing"
    assert len(parser.event_queues) == 0, "Expected 0 event queues when missing"
    assert len(parser.workflows) == 0, "Expected 0 workflows when missing"
    assert len(parser.export_configurations) == 0, "Expected 0 export configs when missing"
    
    print("✓ Missing Phase 9 elements handled correctly")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Parser Phase 9 Advanced Features Tests")
    print("=" * 70)
    
    try:
        print()
        test_parse_single_business_rule()
        print()
        test_parse_multiple_business_rules()
        print()
        test_parse_single_event_queue()
        print()
        test_parse_event_queue_discard_status()
        print()
        test_parse_single_workflow()
        print()
        test_parse_multiple_workflows()
        print()
        test_parse_single_export_configuration()
        print()
        test_parse_multiple_export_configurations()
        print()
        test_parse_all_phase9_elements()
        print()
        test_parse_with_namespaces()
        print()
        test_empty_phase9_containers()
        print()
        test_missing_phase9_elements()
        
        print()
        print("=" * 70)
        print("✓ All Phase 9 advanced features tests passed (12/12)!")
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
