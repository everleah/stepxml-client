"""Phase 8: Bulk operations, workflows, and advanced search - Comprehensive test suite."""

import unittest
from unittest.mock import Mock, patch
from stepxmlclient.rest_client.operations.bulk import (
    BulkOperations,
    WorkflowOperations,
    AdvancedSearchOperations,
    CacheOperations,
    StreamingOperations,
)
from stepxmlclient.rest_client.models.bulk import (
    BulkOperationResponse,
    BulkOperationResultResponse,
    WorkflowDefinition,
    WorkflowInstance,
    WorkflowTransitionRequest,
    AdvancedSearchRequest,
    AdvancedSearchResponse,
    CacheConfigRequest,
    CacheStatistics,
    StreamingRequest,
    StreamingResponse,
)
from stepxmlclient.rest_client.exceptions import ValidationError, NotFoundError


class TestBulkOperationsInit(unittest.TestCase):
    """Test BulkOperations initialization."""
    
    def test_init_without_logger(self):
        """Test initialization without logger."""
        mock_client = Mock()
        ops = BulkOperations(mock_client)
        
        self.assertEqual(ops.client, mock_client)
        self.assertEqual(ops.operation_name, "BulkOperations")
        self.assertIsNotNone(ops.logger)
    
    def test_init_with_logger(self):
        """Test initialization with logger."""
        mock_client = Mock()
        mock_logger = Mock()
        ops = BulkOperations(mock_client, logger=mock_logger)
        
        self.assertEqual(ops.client, mock_client)
        self.assertEqual(ops.logger, mock_logger)


class TestBulkOperations(unittest.TestCase):
    """Test bulk operation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = BulkOperations(self.mock_client)
    
    def test_bulk_create_entities_success(self):
        """Test bulk creating entities."""
        entities = [
            {"entityId": "PROD_001", "name": "Product 1"},
            {"entityId": "PROD_002", "name": "Product 2"}
        ]
        
        mock_response = {
            "bulkOperationId": "BULK_001",
            "operationType": "CREATE",
            "status": "COMPLETED",
            "totalCount": 2,
            "successCount": 2,
            "failureCount": 0
        }
        
        self.mock_client.bulkCreateEntities.return_value = mock_response
        
        result = self.ops.bulk_create_entities(entities)
        
        self.assertIsInstance(result, BulkOperationResponse)
        self.assertEqual(result.bulkOperationId, "BULK_001")
        self.assertEqual(result.successCount, 2)
    
    def test_bulk_create_entities_empty_list(self):
        """Test bulk create with empty list."""
        with self.assertRaises(ValidationError):
            self.ops.bulk_create_entities([])
    
    def test_bulk_update_entities_success(self):
        """Test bulk updating entities."""
        entities = [
            {"entityId": "PROD_001", "status": "INACTIVE"},
            {"entityId": "PROD_002", "status": "INACTIVE"}
        ]
        
        mock_response = {
            "bulkOperationId": "BULK_002",
            "operationType": "UPDATE",
            "status": "COMPLETED",
            "totalCount": 2,
            "successCount": 2,
            "failureCount": 0
        }
        
        self.mock_client.bulkUpdateEntities.return_value = mock_response
        
        result = self.ops.bulk_update_entities(entities)
        
        self.assertIsInstance(result, BulkOperationResponse)
        self.assertEqual(result.operationType, "UPDATE")
    
    def test_bulk_delete_entities_success(self):
        """Test bulk deleting entities."""
        entity_ids = ["PROD_001", "PROD_002", "PROD_003"]
        
        mock_response = {
            "bulkOperationId": "BULK_003",
            "operationType": "DELETE",
            "status": "COMPLETED",
            "totalCount": 3,
            "successCount": 3,
            "failureCount": 0
        }
        
        self.mock_client.bulkDeleteEntities.return_value = mock_response
        
        result = self.ops.bulk_delete_entities(entity_ids)
        
        self.assertIsInstance(result, BulkOperationResponse)
        self.assertEqual(result.totalCount, 3)
    
    def test_bulk_delete_entities_empty_list(self):
        """Test bulk delete with empty list."""
        with self.assertRaises(ValidationError):
            self.ops.bulk_delete_entities([])
    
    def test_get_bulk_operation_status_success(self):
        """Test getting bulk operation status."""
        operation_id = "BULK_001"
        mock_response = {
            "bulkOperationId": operation_id,
            "operationType": "CREATE",
            "status": "COMPLETED",
            "totalCount": 100,
            "successCount": 99,
            "failureCount": 1
        }
        
        self.mock_client.getBulkOperationStatus.return_value = mock_response
        
        result = self.ops.get_bulk_operation_status(operation_id)
        
        self.assertIsInstance(result, BulkOperationResponse)
        self.assertEqual(result.bulkOperationId, operation_id)
    
    def test_get_bulk_operation_status_not_found(self):
        """Test getting non-existent operation status."""
        self.mock_client.getBulkOperationStatus.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.get_bulk_operation_status("nonexistent")
    
    def test_get_bulk_operation_results_success(self):
        """Test getting bulk operation results."""
        operation_id = "BULK_001"
        mock_response = {
            "results": [
                {"entityId": "PROD_001", "status": "SUCCESS"}
            ],
            "totalCount": 100,
            "limit": 20,
            "offset": 0
        }
        
        self.mock_client.getBulkOperationResults.return_value = mock_response
        
        result = self.ops.get_bulk_operation_results(operation_id)
        
        self.assertIsInstance(result, BulkOperationResultResponse)
        self.assertEqual(len(result.results), 1)


class TestWorkflowOperations(unittest.TestCase):
    """Test workflow operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = WorkflowOperations(self.mock_client)
    
    def test_get_workflow_definitions_success(self):
        """Test getting workflow definitions."""
        mock_response = {
            "workflows": [
                {
                    "workflowId": "WF_001",
                    "name": "Product Approval",
                    "states": ["DRAFT", "REVIEW", "APPROVED"],
                    "initialState": "DRAFT"
                }
            ]
        }
        
        self.mock_client.getWorkflowDefinitions.return_value = mock_response
        
        result = self.ops.get_workflow_definitions()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], WorkflowDefinition)
    
    def test_get_workflow_definition_success(self):
        """Test getting specific workflow definition."""
        workflow_id = "WF_001"
        mock_response = {
            "workflowId": workflow_id,
            "name": "Product Approval",
            "states": ["DRAFT", "REVIEW", "APPROVED"],
            "initialState": "DRAFT"
        }
        
        self.mock_client.getWorkflowDefinition.return_value = mock_response
        
        result = self.ops.get_workflow_definition(workflow_id)
        
        self.assertIsInstance(result, WorkflowDefinition)
        self.assertEqual(result.workflowId, workflow_id)
    
    def test_get_entity_workflow_instance_success(self):
        """Test getting entity workflow instance."""
        entity_id = "PROD_001"
        mock_response = {
            "instanceId": "WFI_001",
            "workflowId": "WF_001",
            "entityId": entity_id,
            "currentState": "REVIEW"
        }
        
        self.mock_client.getEntityWorkflowInstance.return_value = mock_response
        
        result = self.ops.get_entity_workflow_instance(entity_id)
        
        self.assertIsInstance(result, WorkflowInstance)
        self.assertEqual(result.currentState, "REVIEW")
    
    def test_transition_workflow_success(self):
        """Test transitioning workflow state."""
        entity_id = "PROD_001"
        transition_data = WorkflowTransitionRequest(
            targetState="APPROVED",
            reason="Approved by manager",
            metadata={"approvedBy": "manager_123"}
        )
        
        mock_response = {
            "instanceId": "WFI_001",
            "workflowId": "WF_001",
            "entityId": entity_id,
            "currentState": "APPROVED"
        }
        
        self.mock_client.transitionWorkflow.return_value = mock_response
        
        result = self.ops.transition_workflow(entity_id, transition_data)
        
        self.assertIsInstance(result, WorkflowInstance)
        self.assertEqual(result.currentState, "APPROVED")
    
    def test_transition_workflow_not_found(self):
        """Test transitioning non-existent entity."""
        self.mock_client.transitionWorkflow.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.transition_workflow(
                "nonexistent",
                WorkflowTransitionRequest(targetState="APPROVED", reason=None, metadata=None)
            )


class TestAdvancedSearchOperations(unittest.TestCase):
    """Test advanced search operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = AdvancedSearchOperations(self.mock_client)
    
    def test_advanced_search_success(self):
        """Test advanced search with aggregations."""
        search_request = AdvancedSearchRequest(
            entityType="Product",
            facets=["status", "category"],
            limit=20,
            offset=None,
            sort=None,
            query=None,
            filters=None
        )
        
        mock_response = {
            "entities": [
                {"entityId": "PROD_001", "name": "Product 1"}
            ],
            "aggregations": [
                {
                    "field": "status",
                    "buckets": [
                        {"value": "ACTIVE", "count": 150}
                    ]
                }
            ],
            "totalCount": 200,
            "limit": 20,
            "offset": 0
        }
        
        self.mock_client.advancedSearch.return_value = mock_response
        
        result = self.ops.advanced_search(search_request)
        
        self.assertIsInstance(result, AdvancedSearchResponse)
        self.assertEqual(len(result.entities), 1)
        self.assertIsNotNone(result.aggregations)
    
    def test_advanced_search_invalid_request(self):
        """Test advanced search with invalid request."""
        self.mock_client.advancedSearch.side_effect = Exception("400 Bad Request")
        
        search_request = AdvancedSearchRequest(
            entityType="Product",
            facets=None,
            limit=20,
            offset=None,
            sort=None,
            query=None,
            filters=None
        )
        
        with self.assertRaises(ValidationError):
            self.ops.advanced_search(search_request)
    
    def test_get_search_suggestions_success(self):
        """Test getting search suggestions."""
        mock_response = {
            "suggestions": ["Product 1", "Product 2", "Product 3"]
        }
        
        self.mock_client.getSearchSuggestions.return_value = mock_response
        
        result = self.ops.get_search_suggestions("Product", "Prod")
        
        self.assertIsInstance(result, dict)
        self.assertIn("suggestions", result)
    
    def test_get_search_suggestions_missing_params(self):
        """Test search suggestions with missing parameters."""
        with self.assertRaises(ValidationError):
            self.ops.get_search_suggestions("", "")


class TestCacheOperations(unittest.TestCase):
    """Test cache operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = CacheOperations(self.mock_client)
    
    def test_configure_cache_success(self):
        """Test configuring cache."""
        config = CacheConfigRequest(
            enableCache=True,
            ttlSeconds=300,
            cacheKey=None,
            invalidatePrevious=None
        )
        
        self.mock_client.configureCache.return_value = None
        
        result = self.ops.configure_cache(config)
        
        self.assertTrue(result)
        self.mock_client.configureCache.assert_called_once()
    
    def test_configure_cache_invalid(self):
        """Test configuring cache with invalid config."""
        self.mock_client.configureCache.side_effect = Exception("400 Bad Request")
        
        config = CacheConfigRequest(
            enableCache=True,
            ttlSeconds=300,
            cacheKey=None,
            invalidatePrevious=None
        )
        
        with self.assertRaises(ValidationError):
            self.ops.configure_cache(config)
    
    def test_get_cache_statistics_success(self):
        """Test getting cache statistics."""
        mock_response = {
            "hits": 450,
            "misses": 50,
            "hitRate": 0.9,
            "size": 1024000,
            "itemCount": 25
        }
        
        self.mock_client.getCacheStatistics.return_value = mock_response
        
        result = self.ops.get_cache_statistics()
        
        self.assertIsInstance(result, CacheStatistics)
        self.assertEqual(result.hitRate, 0.9)
    
    def test_clear_cache_success(self):
        """Test clearing cache."""
        self.mock_client.clearCache.return_value = None
        
        result = self.ops.clear_cache()
        
        self.assertTrue(result)
        self.mock_client.clearCache.assert_called_once()
    
    def test_clear_cache_with_key(self):
        """Test clearing specific cache key."""
        self.mock_client.clearCache.return_value = None
        
        result = self.ops.clear_cache(cache_key="product_search")
        
        self.assertTrue(result)


class TestStreamingOperations(unittest.TestCase):
    """Test streaming operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = StreamingOperations(self.mock_client)
    
    def test_start_streaming_success(self):
        """Test starting stream."""
        stream_request = StreamingRequest(
            entityType="Product",
            chunkSize=1000,
            format="JSON",
            filters=None,
            includeMetadata=None
        )
        
        mock_response = {
            "streamId": "STREAM_001",
            "chunkNumber": 1,
            "totalChunks": 5,
            "entities": [{"entityId": "PROD_001"}],
            "hasMore": True
        }
        
        self.mock_client.startStreaming.return_value = mock_response
        
        result = self.ops.start_streaming(stream_request)
        
        self.assertIsInstance(result, StreamingResponse)
        self.assertEqual(result.streamId, "STREAM_001")
        self.assertTrue(result.hasMore)
    
    def test_start_streaming_invalid(self):
        """Test starting stream with invalid request."""
        self.mock_client.startStreaming.side_effect = Exception("400 Bad Request")
        
        stream_request = StreamingRequest(
            entityType="Product",
            chunkSize=1000,
            format="JSON",
            filters=None,
            includeMetadata=None
        )
        
        with self.assertRaises(ValidationError):
            self.ops.start_streaming(stream_request)
    
    def test_get_next_stream_chunk_success(self):
        """Test getting next stream chunk."""
        stream_id = "STREAM_001"
        mock_response = {
            "streamId": stream_id,
            "chunkNumber": 2,
            "totalChunks": 5,
            "entities": [{"entityId": "PROD_002"}],
            "hasMore": True,
            "nextToken": "TOKEN_002"
        }
        
        self.mock_client.getNextStreamChunk.return_value = mock_response
        
        result = self.ops.get_next_stream_chunk(stream_id)
        
        self.assertIsInstance(result, StreamingResponse)
        self.assertEqual(result.chunkNumber, 2)
    
    def test_get_next_stream_chunk_not_found(self):
        """Test getting chunk from non-existent stream."""
        self.mock_client.getNextStreamChunk.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.get_next_stream_chunk("nonexistent")
    
    def test_close_stream_success(self):
        """Test closing stream."""
        stream_id = "STREAM_001"
        self.mock_client.closeStream.return_value = None
        
        result = self.ops.close_stream(stream_id)
        
        self.assertTrue(result)
        self.mock_client.closeStream.assert_called_once_with(streamId=stream_id)
    
    def test_close_stream_not_found(self):
        """Test closing non-existent stream."""
        self.mock_client.closeStream.side_effect = Exception("404 Not Found")
        
        with self.assertRaises(NotFoundError):
            self.ops.close_stream("nonexistent")


class TestErrorHandling(unittest.TestCase):
    """Test error handling in bulk operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.bulk_ops = BulkOperations(self.mock_client)
        self.wf_ops = WorkflowOperations(self.mock_client)
    
    def test_bulk_operations_missing_id_validation(self):
        """Test validation for missing operation ID."""
        with self.assertRaises(ValidationError):
            self.bulk_ops.get_bulk_operation_status(None)
    
    def test_workflow_missing_id_validation(self):
        """Test validation for missing workflow ID."""
        with self.assertRaises(ValidationError):
            self.wf_ops.get_workflow_definition(None)


class TestPaginationHandling(unittest.TestCase):
    """Test pagination parameter handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.ops = BulkOperations(self.mock_client)
    
    def test_bulk_operation_results_default_pagination(self):
        """Test results with default pagination."""
        self.mock_client.getBulkOperationResults.return_value = {
            "results": [],
            "totalCount": 0,
            "limit": 20,
            "offset": 0
        }
        
        self.ops.get_bulk_operation_results("BULK_001")
        
        call_args = self.mock_client.getBulkOperationResults.call_args[1]
        self.assertEqual(call_args["limit"], 20)
        self.assertEqual(call_args["offset"], 0)
    
    def test_bulk_operation_results_custom_pagination(self):
        """Test results with custom pagination."""
        self.mock_client.getBulkOperationResults.return_value = {
            "results": [],
            "totalCount": 0,
            "limit": 100,
            "offset": 50
        }
        
        self.ops.get_bulk_operation_results("BULK_001", limit=100, offset=50)
        
        call_args = self.mock_client.getBulkOperationResults.call_args[1]
        self.assertEqual(call_args["limit"], 100)
        self.assertEqual(call_args["offset"], 50)


if __name__ == '__main__':
    unittest.main()
