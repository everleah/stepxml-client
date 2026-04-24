"""Test inbound integration endpoint operations.

Tests the high-level InboundOperations wrapper for uploading STEP-XML
to configured inbound endpoints and managing their status.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import logging

from stepxmlclient.rest_client.operations.inbound import InboundOperations
from stepxmlclient.rest_client.exceptions import NotFoundError, ValidationError, RestApiError


class TestInboundOperations(unittest.TestCase):
    """Test InboundOperations class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.logger = logging.getLogger("test_inbound")
        self.context = "TestContext"
        self.workspace = "TestWorkspace"
        
        self.inbound = InboundOperations(
            self.mock_client,
            logger=self.logger,
            context=self.context,
            workspace=self.workspace
        )

    def test_upload_and_invoke_with_bytes(self):
        """Test upload_and_invoke with bytes data."""
        xml_data = b"<StepXML>test</StepXML>"
        endpoint_id = "test_endpoint"
        
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.return_value = {
            "processId": "12345"
        }
        
        result = self.inbound.upload_and_invoke(endpoint_id, xml_data)
        
        self.assertEqual(result["processId"], "12345")
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.assert_called_once()
        
        # Check that context and workspace were passed
        call_kwargs = self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.call_args[1]
        self.assertEqual(call_kwargs["context"], self.context)
        self.assertEqual(call_kwargs["workspace"], self.workspace)

    def test_upload_and_invoke_with_string(self):
        """Test upload_and_invoke with string data."""
        xml_data = "<StepXML>test</StepXML>"
        endpoint_id = "test_endpoint"
        
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.return_value = {
            "success": True
        }
        
        result = self.inbound.upload_and_invoke(endpoint_id, xml_data)
        
        self.assertTrue(result["success"])
        
        # Verify string was converted to bytes
        call_kwargs = self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.call_args[1]
        self.assertEqual(call_kwargs["body"], b"<StepXML>test</StepXML>")

    def test_upload_and_invoke_missing_endpoint_id(self):
        """Test upload_and_invoke raises error for missing endpoint_id."""
        xml_data = b"<StepXML>test</StepXML>"
        
        with self.assertRaises(ValidationError):
            self.inbound.upload_and_invoke(None, xml_data)

    def test_upload_and_invoke_missing_xml_data(self):
        """Test upload_and_invoke raises error for missing xml_data."""
        endpoint_id = "test_endpoint"
        
        with self.assertRaises(ValidationError):
            self.inbound.upload_and_invoke(endpoint_id, None)

    def test_upload_and_invoke_with_file_name(self):
        """Test upload_and_invoke with optional file name."""
        xml_data = b"<StepXML>test</StepXML>"
        endpoint_id = "test_endpoint"
        file_name = "data.xml"
        
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.return_value = {}
        
        self.inbound.upload_and_invoke(endpoint_id, xml_data, file_name=file_name)
        
        call_kwargs = self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.call_args[1]
        self.assertEqual(call_kwargs["fileName"], file_name)

    def test_upload_and_invoke_endpoint_not_found(self):
        """Test upload_and_invoke raises NotFoundError for missing endpoint."""
        xml_data = b"<StepXML>test</StepXML>"
        endpoint_id = "missing_endpoint"
        
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.side_effect = \
            Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.inbound.upload_and_invoke(endpoint_id, xml_data)

    def test_upload_and_invoke_endpoint_not_enabled(self):
        """Test upload_and_invoke raises ValidationError when endpoint disabled."""
        xml_data = b"<StepXML>test</StepXML>"
        endpoint_id = "disabled_endpoint"
        
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.side_effect = \
            Exception("400 Bad Request: endpoint not enabled")
        
        with self.assertRaises(ValidationError) as ctx:
            self.inbound.upload_and_invoke(endpoint_id, xml_data)
        
        self.assertIn("not enabled", str(ctx.exception))

    def test_upload_and_invoke_no_rest_receiver(self):
        """Test upload_and_invoke raises error when REST receiver not configured."""
        xml_data = b"<StepXML>test</StepXML>"
        endpoint_id = "no_rest_receiver"
        
        self.mock_client.postInboundIntegrationEndpointUploadAndInvoke.side_effect = \
            Exception("400 Bad Request: REST receiver not configured")
        
        with self.assertRaises(ValidationError) as ctx:
            self.inbound.upload_and_invoke(endpoint_id, xml_data)
        
        self.assertIn("REST", str(ctx.exception))

    def test_list_endpoints(self):
        """Test list_endpoints."""
        endpoints = [
            {"ID": "endpoint1", "Name": "Import1"},
            {"ID": "endpoint2", "Name": "Import2"}
        ]
        self.mock_client.getInboundIntegrationEndpoints.return_value = endpoints
        
        result = self.inbound.list_endpoints()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["ID"], "endpoint1")

    def test_get_status(self):
        """Test get_status."""
        endpoint_id = "test_endpoint"
        status_response = {"status": "enabled", "messageCount": 42}
        
        self.mock_client.getInboundIntegrationEndpointStatus.return_value = status_response
        
        result = self.inbound.get_status(endpoint_id)
        
        self.assertEqual(result["status"], "enabled")
        self.assertEqual(result["messageCount"], 42)

    def test_get_status_missing_endpoint_id(self):
        """Test get_status raises error for missing endpoint_id."""
        with self.assertRaises(ValidationError):
            self.inbound.get_status(None)

    def test_enable_endpoint(self):
        """Test enable_endpoint."""
        endpoint_id = "test_endpoint"
        
        self.mock_client.postInboundIntegrationEndpointEnable.return_value = {
            "success": True
        }
        
        result = self.inbound.enable_endpoint(endpoint_id)
        
        self.assertTrue(result["success"])
        self.mock_client.postInboundIntegrationEndpointEnable.assert_called_once()

    def test_disable_endpoint(self):
        """Test disable_endpoint."""
        endpoint_id = "test_endpoint"
        
        self.mock_client.postInboundIntegrationEndpointDisable.return_value = {
            "success": True
        }
        
        result = self.inbound.disable_endpoint(endpoint_id)
        
        self.assertTrue(result["success"])
        self.mock_client.postInboundIntegrationEndpointDisable.assert_called_once()

    def test_get_execution_report(self):
        """Test get_execution_report."""
        endpoint_id = "test_endpoint"
        report = [
            {"timestamp": "2026-04-24", "action": "import", "status": "success"},
            {"timestamp": "2026-04-23", "action": "import", "status": "failed"}
        ]
        
        self.mock_client.getInboundIntegrationEndpointExecutionReport.return_value = report
        
        result = self.inbound.get_execution_report(endpoint_id)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["action"], "import")

    def test_get_statistics(self):
        """Test get_statistics."""
        endpoint_id = "test_endpoint"
        stats = {
            "messageCount": 100,
            "errorCount": 5,
            "successCount": 95
        }
        
        self.mock_client.getInboundIntegrationEndpointStatistics.return_value = stats
        
        result = self.inbound.get_statistics(endpoint_id)
        
        self.assertEqual(result["messageCount"], 100)
        self.assertEqual(result["errorCount"], 5)

    def test_get_worker_processes(self):
        """Test get_worker_processes."""
        endpoint_id = "test_endpoint"
        processes = ["proc1", "proc2", "proc3"]
        
        self.mock_client.getInboundIntegrationEndpointWorkerProcesses.return_value = processes
        
        result = self.inbound.get_worker_processes(endpoint_id)
        
        self.assertEqual(len(result), 3)

    def test_context_and_workspace_passed_to_all_operations(self):
        """Verify context and workspace are passed to all operations."""
        endpoint_id = "test_endpoint"
        
        # Mock all operations
        self.mock_client.getInboundIntegrationEndpointStatus.return_value = {}
        self.mock_client.postInboundIntegrationEndpointEnable.return_value = {}
        self.mock_client.postInboundIntegrationEndpointDisable.return_value = {}
        self.mock_client.getInboundIntegrationEndpointExecutionReport.return_value = []
        self.mock_client.getInboundIntegrationEndpointStatistics.return_value = {}
        self.mock_client.getInboundIntegrationEndpointWorkerProcesses.return_value = []
        self.mock_client.getInboundIntegrationEndpoints.return_value = []
        
        # Call operations
        self.inbound.get_status(endpoint_id)
        self.inbound.enable_endpoint(endpoint_id)
        self.inbound.disable_endpoint(endpoint_id)
        self.inbound.get_execution_report(endpoint_id)
        self.inbound.get_statistics(endpoint_id)
        self.inbound.get_worker_processes(endpoint_id)
        self.inbound.list_endpoints()
        
        # Check all calls included context and workspace
        for call in self.mock_client.method_calls:
            if "Inbound" in str(call):
                call_kwargs = call[2]  # Get kwargs from call tuple
                if call_kwargs:  # Only check if there are kwargs
                    self.assertIn("context", call_kwargs)
                    self.assertEqual(call_kwargs["context"], self.context)
                    self.assertIn("workspace", call_kwargs)
                    self.assertEqual(call_kwargs["workspace"], self.workspace)


if __name__ == "__main__":
    unittest.main()
