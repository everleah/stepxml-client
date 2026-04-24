"""Bulk operations, workflows, and advanced search for STEP REST API v2."""

import logging
from typing import Optional, List, Dict, Any

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import ValidationError, NotFoundError, RestApiError
from ..models.bulk import (
    BulkOperationRequest,
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


class BulkOperations(BaseOperation):
    """Operations for bulk processing of entities."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize bulk operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="BulkOperations", logger=logger)
    
    @handle_rest_errors
    def bulk_create_entities(self, entities: List[Dict[str, Any]],
                            continue_on_error: bool = True) -> BulkOperationResponse:
        """Bulk create entities in one operation.
        
        Args:
            entities: List of entity dictionaries to create
            continue_on_error: Continue processing on error (default: True)
            
        Returns:
            BulkOperationResponse with operation status
            
        Raises:
            ValidationError: If entities invalid
            RestApiError: For API errors
        """
        if not entities:
            raise ValidationError("entities list cannot be empty")
        
        request_data = {
            "operationType": "CREATE",
            "entities": entities,
            "continueOnError": continue_on_error
        }
        
        self._log_operation("bulkCreateEntities", {
            "entityCount": len(entities),
            "continueOnError": continue_on_error
        })
        
        try:
            response = self.client.bulkCreateEntities(body=request_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Bulk create failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return BulkOperationResponse(**response)
        return response
    
    @handle_rest_errors
    def bulk_update_entities(self, entities: List[Dict[str, Any]],
                            continue_on_error: bool = True) -> BulkOperationResponse:
        """Bulk update entities in one operation.
        
        Args:
            entities: List of entity dictionaries to update
            continue_on_error: Continue processing on error (default: True)
            
        Returns:
            BulkOperationResponse with operation status
            
        Raises:
            ValidationError: If entities invalid
            RestApiError: For API errors
        """
        if not entities:
            raise ValidationError("entities list cannot be empty")
        
        request_data = {
            "operationType": "UPDATE",
            "entities": entities,
            "continueOnError": continue_on_error
        }
        
        self._log_operation("bulkUpdateEntities", {
            "entityCount": len(entities),
            "continueOnError": continue_on_error
        })
        
        try:
            response = self.client.bulkUpdateEntities(body=request_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Bulk update failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return BulkOperationResponse(**response)
        return response
    
    @handle_rest_errors
    def bulk_delete_entities(self, entity_ids: List[str],
                            continue_on_error: bool = True) -> BulkOperationResponse:
        """Bulk delete entities in one operation.
        
        Args:
            entity_ids: List of entity IDs to delete
            continue_on_error: Continue processing on error (default: True)
            
        Returns:
            BulkOperationResponse with operation status
            
        Raises:
            ValidationError: If entity_ids invalid
            RestApiError: For API errors
        """
        if not entity_ids:
            raise ValidationError("entity_ids list cannot be empty")
        
        request_data = {
            "operationType": "DELETE",
            "entities": [{"entityId": eid} for eid in entity_ids],
            "continueOnError": continue_on_error
        }
        
        self._log_operation("bulkDeleteEntities", {
            "entityCount": len(entity_ids),
            "continueOnError": continue_on_error
        })
        
        try:
            response = self.client.bulkDeleteEntities(body=request_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Bulk delete failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return BulkOperationResponse(**response)
        return response
    
    @handle_rest_errors
    def get_bulk_operation_status(self, operation_id: str) -> BulkOperationResponse:
        """Get status of a bulk operation.
        
        Args:
            operation_id: The bulk operation ID
            
        Returns:
            BulkOperationResponse with current status
            
        Raises:
            ValidationError: If operation_id missing
            NotFoundError: If operation not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"operation_id": operation_id},
            ["operation_id"]
        )
        
        self._log_operation("getBulkOperationStatus", {"operationId": operation_id})
        
        try:
            response = self.client.getBulkOperationStatus(operationId=operation_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(operation_id, "BulkOperation")
            raise
        
        if isinstance(response, dict):
            return BulkOperationResponse(**response)
        return response
    
    @handle_rest_errors
    def get_bulk_operation_results(self, operation_id: str,
                                   limit: int = 20,
                                   offset: int = 0) -> BulkOperationResultResponse:
        """Get detailed results from a bulk operation.
        
        Args:
            operation_id: The bulk operation ID
            limit: Result limit (1-500, default: 20)
            offset: Result offset (default: 0)
            
        Returns:
            BulkOperationResultResponse with operation results
            
        Raises:
            ValidationError: If operation_id missing
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"operation_id": operation_id},
            ["operation_id"]
        )
        
        pagination_params = self._build_pagination_params(limit, offset)
        
        self._log_operation("getBulkOperationResults", {
            "operationId": operation_id,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        self._log_operation("getBulkOperationResults", {
            "operationId": operation_id,
            "limit": pagination_params["limit"],
            "offset": pagination_params["offset"]
        })
        
        response = self.client.getBulkOperationResults(
            operationId=operation_id,
            **self._clean_params({
                "limit": pagination_params["limit"],
                "offset": pagination_params["offset"]
            })
        )
        
        if isinstance(response, dict):
            return BulkOperationResultResponse(**response)
        return response


class WorkflowOperations(BaseOperation):
    """Operations for workflow management."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize workflow operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="WorkflowOperations", logger=logger)
    
    @handle_rest_errors
    def get_workflow_definitions(self) -> List[WorkflowDefinition]:
        """Get all available workflow definitions.
        
        Returns:
            List of WorkflowDefinition objects
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getWorkflowDefinitions", {})
        
        response = self.client.getWorkflowDefinitions()
        
        if isinstance(response, dict) and "workflows" in response:
            return [WorkflowDefinition(**wf) for wf in response["workflows"]]
        elif isinstance(response, list):
            return [WorkflowDefinition(**wf) if isinstance(wf, dict) else wf for wf in response]
        return []
    
    @handle_rest_errors
    def get_workflow_definition(self, workflow_id: str) -> WorkflowDefinition:
        """Get a specific workflow definition.
        
        Args:
            workflow_id: The workflow ID
            
        Returns:
            WorkflowDefinition object
            
        Raises:
            ValidationError: If workflow_id missing
            NotFoundError: If workflow not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"workflow_id": workflow_id},
            ["workflow_id"]
        )
        
        self._log_operation("getWorkflowDefinition", {"workflowId": workflow_id})
        
        try:
            response = self.client.getWorkflowDefinition(workflowId=workflow_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(workflow_id, "Workflow")
            raise
        
        if isinstance(response, dict):
            return WorkflowDefinition(**response)
        return response
    
    @handle_rest_errors
    def get_entity_workflow_instance(self, entity_id: str) -> WorkflowInstance:
        """Get workflow instance for an entity.
        
        Args:
            entity_id: The entity ID
            
        Returns:
            WorkflowInstance object
            
        Raises:
            ValidationError: If entity_id missing
            NotFoundError: If entity or workflow instance not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        self._log_operation("getEntityWorkflowInstance", {"entityId": entity_id})
        
        try:
            response = self.client.getEntityWorkflowInstance(entityId=entity_id)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity/WorkflowInstance")
            raise
        
        if isinstance(response, dict):
            return WorkflowInstance(**response)
        return response
    
    @handle_rest_errors
    def transition_workflow(self, entity_id: str,
                          data: WorkflowTransitionRequest) -> WorkflowInstance:
        """Transition entity to new workflow state.
        
        Args:
            entity_id: The entity ID
            data: WorkflowTransitionRequest with target state
            
        Returns:
            Updated WorkflowInstance
            
        Raises:
            ValidationError: If data invalid
            NotFoundError: If entity not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"entity_id": entity_id},
            ["entity_id"]
        )
        
        if hasattr(data, 'model_dump'):
            transition_data = data.model_dump(exclude_none=True)
        else:
            transition_data = dict(data) if not isinstance(data, dict) else data
        
        self._log_operation("transitionWorkflow", {
            "entityId": entity_id,
            "targetState": transition_data.get("targetState")
        })
        
        try:
            response = self.client.transitionWorkflow(
                entityId=entity_id,
                body=transition_data
            )
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(entity_id, "Entity")
            raise
        
        if isinstance(response, dict):
            return WorkflowInstance(**response)
        return response


class AdvancedSearchOperations(BaseOperation):
    """Operations for advanced search and aggregations."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize advanced search operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="AdvancedSearchOperations", logger=logger)
    
    @handle_rest_errors
    def advanced_search(self, search_request: AdvancedSearchRequest) -> AdvancedSearchResponse:
        """Execute advanced search with complex queries and aggregations.
        
        Args:
            search_request: AdvancedSearchRequest with query details
            
        Returns:
            AdvancedSearchResponse with results and aggregations
            
        Raises:
            ValidationError: If request invalid
            RestApiError: For API errors
        """
        if hasattr(search_request, 'model_dump'):
            request_data = search_request.model_dump(exclude_none=True)
        else:
            request_data = dict(search_request) if not isinstance(search_request, dict) else search_request
        
        self._log_operation("advancedSearch", {
            "entityType": request_data.get("entityType"),
            "hasAggregations": "aggregations" in request_data,
            "hasFacets": bool(request_data.get("facets"))
        })
        
        try:
            response = self.client.advancedSearch(body=request_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Advanced search failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return AdvancedSearchResponse(**response)
        return response
    
    @handle_rest_errors
    def get_search_suggestions(self, entity_type: str,
                              prefix: str,
                              field: Optional[str] = None) -> Dict[str, Any]:
        """Get search suggestions for auto-complete.
        
        Args:
            entity_type: Entity type to search
            prefix: Prefix to match
            field: Optional field to search in
            
        Returns:
            Dictionary with suggestions
            
        Raises:
            ValidationError: If parameters invalid
            RestApiError: For API errors
        """
        if not entity_type or not prefix:
            raise ValidationError("entity_type and prefix are required")
        
        self._log_operation("getSearchSuggestions", {
            "entityType": entity_type,
            "prefixLength": len(prefix),
            "field": field
        })
        
        params = self._clean_params({
            "entityType": entity_type,
            "prefix": prefix,
            "field": field
        })
        
        response = self.client.getSearchSuggestions(**params)
        
        return response if isinstance(response, dict) else {"suggestions": response}


class CacheOperations(BaseOperation):
    """Operations for managing result caching."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize cache operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="CacheOperations", logger=logger)
    
    @handle_rest_errors
    def configure_cache(self, config: CacheConfigRequest) -> bool:
        """Configure caching for query results.
        
        Args:
            config: CacheConfigRequest with cache settings
            
        Returns:
            True if configuration successful
            
        Raises:
            ValidationError: If config invalid
            RestApiError: For API errors
        """
        if hasattr(config, 'model_dump'):
            config_data = config.model_dump(exclude_none=True)
        else:
            config_data = dict(config) if not isinstance(config, dict) else config
        
        self._log_operation("configureCache", {
            "enableCache": config_data.get("enableCache"),
            "ttlSeconds": config_data.get("ttlSeconds")
        })
        
        try:
            self.client.configureCache(body=config_data)
            return True
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Cache configuration failed: {str(e)}")
            raise
    
    @handle_rest_errors
    def get_cache_statistics(self) -> CacheStatistics:
        """Get cache statistics and performance metrics.
        
        Returns:
            CacheStatistics with cache metrics
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("getCacheStatistics", {})
        
        response = self.client.getCacheStatistics()
        
        if isinstance(response, dict):
            return CacheStatistics(**response)
        return response
    
    @handle_rest_errors
    def clear_cache(self, cache_key: Optional[str] = None) -> bool:
        """Clear cache or specific cache entries.
        
        Args:
            cache_key: Optional specific cache key to clear (clears all if None)
            
        Returns:
            True if cache cleared successfully
            
        Raises:
            RestApiError: For API errors
        """
        self._log_operation("clearCache", {"cacheKey": cache_key})
        
        params = self._clean_params({"cacheKey": cache_key}) if cache_key else {}
        
        try:
            self.client.clearCache(**params)
            return True
        except Exception:
            raise


class StreamingOperations(BaseOperation):
    """Operations for streaming large result sets."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """Initialize streaming operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
        """
        super().__init__(client, operation_name="StreamingOperations", logger=logger)
    
    @handle_rest_errors
    def start_streaming(self, stream_request: StreamingRequest) -> StreamingResponse:
        """Start streaming large result set.
        
        Args:
            stream_request: StreamingRequest with stream configuration
            
        Returns:
            StreamingResponse with first chunk
            
        Raises:
            ValidationError: If request invalid
            RestApiError: For API errors
        """
        if hasattr(stream_request, 'model_dump'):
            request_data = stream_request.model_dump(exclude_none=True)
        else:
            request_data = dict(stream_request) if not isinstance(stream_request, dict) else stream_request
        
        self._log_operation("startStreaming", {
            "entityType": request_data.get("entityType"),
            "chunkSize": request_data.get("chunkSize"),
            "format": request_data.get("format")
        })
        
        try:
            response = self.client.startStreaming(body=request_data)
        except Exception as e:
            if "400" in str(e):
                raise ValidationError(f"Stream start failed: {str(e)}")
            raise
        
        if isinstance(response, dict):
            return StreamingResponse(**response)
        return response
    
    @handle_rest_errors
    def get_next_stream_chunk(self, stream_id: str,
                             next_token: Optional[str] = None) -> StreamingResponse:
        """Get next chunk from stream.
        
        Args:
            stream_id: The stream ID
            next_token: Optional token for next chunk
            
        Returns:
            StreamingResponse with next chunk
            
        Raises:
            ValidationError: If stream_id missing
            NotFoundError: If stream not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"stream_id": stream_id},
            ["stream_id"]
        )
        
        self._log_operation("getNextStreamChunk", {
            "streamId": stream_id,
            "hasToken": next_token is not None
        })
        
        try:
            params = self._clean_params({
                "streamId": stream_id,
                "nextToken": next_token
            })
            response = self.client.getNextStreamChunk(**params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(stream_id, "Stream")
            raise
        
        if isinstance(response, dict):
            return StreamingResponse(**response)
        return response
    
    @handle_rest_errors
    def close_stream(self, stream_id: str) -> bool:
        """Close/cancel a stream.
        
        Args:
            stream_id: The stream ID to close
            
        Returns:
            True if stream closed successfully
            
        Raises:
            ValidationError: If stream_id missing
            NotFoundError: If stream not found
            RestApiError: For API errors
        """
        self._validate_required_params(
            {"stream_id": stream_id},
            ["stream_id"]
        )
        
        self._log_operation("closeStream", {"streamId": stream_id})
        
        try:
            self.client.closeStream(streamId=stream_id)
            return True
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(stream_id, "Stream")
            raise
