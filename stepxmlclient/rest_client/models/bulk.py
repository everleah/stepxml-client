"""Bulk operations and workflow model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class BulkOperationRequest(BaseModel):
    """Request for bulk operations."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "operationType": "CREATE",
            "entities": [
                {"entityId": "PROD_001", "name": "Product 1"},
                {"entityId": "PROD_002", "name": "Product 2"}
            ],
            "continueOnError": True
        }
    })
    
    operationType: str = Field(..., description="Operation type: CREATE, UPDATE, DELETE")
    entities: List[Dict[str, Any]] = Field(..., description="List of entities to process")
    continueOnError: Optional[bool] = Field(True, description="Continue processing on error")
    timeout: Optional[int] = Field(None, description="Operation timeout in seconds")


class BulkOperationResponse(BaseModel):
    """Response from bulk operation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "bulkOperationId": "BULK_001",
            "operationType": "CREATE",
            "status": "COMPLETED",
            "totalCount": 2,
            "successCount": 2,
            "failureCount": 0,
            "startTime": "2025-01-01T00:00:00Z",
            "endTime": "2025-01-01T00:00:05Z"
        }
    })
    
    bulkOperationId: str = Field(..., description="Unique bulk operation ID")
    operationType: str = Field(..., description="Type of operation performed")
    status: str = Field(..., description="Operation status: PENDING, RUNNING, COMPLETED, FAILED")
    totalCount: int = Field(..., description="Total entities processed")
    successCount: int = Field(..., description="Successfully processed entities")
    failureCount: int = Field(..., description="Failed entities")
    startTime: Optional[str] = Field(None, description="Operation start time")
    endTime: Optional[str] = Field(None, description="Operation end time")
    duration: Optional[float] = Field(None, description="Duration in seconds")


class BulkOperationResult(BaseModel):
    """Individual result from bulk operation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entityId": "PROD_001",
            "status": "SUCCESS",
            "message": "Entity created successfully",
            "resultId": "RES_001"
        }
    })
    
    entityId: str = Field(..., description="Entity identifier")
    status: str = Field(..., description="Result status: SUCCESS, FAILURE, SKIPPED")
    message: Optional[str] = Field(None, description="Status message")
    resultId: Optional[str] = Field(None, description="Result identifier")
    error: Optional[Dict[str, Any]] = Field(None, description="Error details if failed")


class BulkOperationResultResponse(BaseModel):
    """Paginated list of bulk operation results."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "results": [
                {"entityId": "PROD_001", "status": "SUCCESS", "resultId": "RES_001"}
            ],
            "totalCount": 100,
            "limit": 20,
            "offset": 0
        }
    })
    
    results: List[BulkOperationResult] = Field(..., description="List of operation results")
    totalCount: int = Field(..., description="Total results")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")


class WorkflowDefinition(BaseModel):
    """Workflow definition."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "workflowId": "WF_001",
            "name": "Product Approval",
            "description": "Standard product approval workflow",
            "states": ["DRAFT", "REVIEW", "APPROVED"],
            "initialState": "DRAFT"
        }
    })
    
    workflowId: str = Field(..., description="Unique workflow ID")
    name: str = Field(..., description="Workflow name")
    description: Optional[str] = Field(None, description="Workflow description")
    states: List[str] = Field(..., description="Available workflow states")
    initialState: str = Field(..., description="Initial state for new entities")
    transitions: Optional[List[Dict[str, Any]]] = Field(None, description="State transitions")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Workflow metadata")


class WorkflowInstance(BaseModel):
    """Workflow instance for an entity."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "instanceId": "WFI_001",
            "workflowId": "WF_001",
            "entityId": "PROD_001",
            "currentState": "REVIEW",
            "startTime": "2025-01-01T00:00:00Z",
            "history": [
                {"state": "DRAFT", "timestamp": "2025-01-01T00:00:00Z"},
                {"state": "REVIEW", "timestamp": "2025-01-01T00:01:00Z"}
            ]
        }
    })
    
    instanceId: str = Field(..., description="Workflow instance ID")
    workflowId: str = Field(..., description="Associated workflow ID")
    entityId: str = Field(..., description="Entity ID")
    currentState: str = Field(..., description="Current workflow state")
    startTime: Optional[str] = Field(None, description="Instance start time")
    endTime: Optional[str] = Field(None, description="Instance end time")
    history: Optional[List[Dict[str, Any]]] = Field(None, description="State transition history")


class WorkflowTransitionRequest(BaseModel):
    """Request to transition workflow to new state."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "targetState": "APPROVED",
            "reason": "Approved by manager",
            "metadata": {"approvedBy": "user123"}
        }
    })
    
    targetState: str = Field(..., description="Target state to transition to")
    reason: Optional[str] = Field(None, description="Transition reason")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Transition metadata")


class AdvancedSearchRequest(BaseModel):
    """Advanced search request with complex queries."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entityType": "Product",
            "query": {
                "operator": "AND",
                "conditions": [
                    {"field": "status", "operator": "=", "value": "ACTIVE"},
                    {"field": "createdDate", "operator": ">", "value": "2025-01-01"}
                ]
            },
            "facets": ["status", "category"],
            "limit": 20,
            "offset": 0
        }
    })
    
    entityType: str = Field(..., description="Entity type to search")
    query: Optional[Dict[str, Any]] = Field(None, description="Complex query structure")
    facets: Optional[List[str]] = Field(None, description="Facet fields to aggregate")
    filters: Optional[List[Dict[str, Any]]] = Field(None, description="Additional filters")
    limit: Optional[int] = Field(20, description="Result limit (1-500)")
    offset: Optional[int] = Field(0, description="Result offset")
    sort: Optional[List[Dict[str, str]]] = Field(None, description="Sort specifications")


class SearchAggregation(BaseModel):
    """Aggregation result from search."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "field": "status",
            "buckets": [
                {"value": "ACTIVE", "count": 150},
                {"value": "INACTIVE", "count": 50}
            ]
        }
    })
    
    field: str = Field(..., description="Aggregation field")
    buckets: List[Dict[str, Any]] = Field(..., description="Aggregation buckets")


class AdvancedSearchResponse(BaseModel):
    """Response from advanced search."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entities": [
                {"entityId": "PROD_001", "name": "Product 1"}
            ],
            "aggregations": [
                {"field": "status", "buckets": [{"value": "ACTIVE", "count": 150}]}
            ],
            "totalCount": 200,
            "limit": 20,
            "offset": 0
        }
    })
    
    entities: List[Dict[str, Any]] = Field(..., description="Search results")
    aggregations: Optional[List[SearchAggregation]] = Field(None, description="Aggregation results")
    totalCount: int = Field(..., description="Total results available")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")
    facets: Optional[Dict[str, List[str]]] = Field(None, description="Available facet values")


class CacheConfigRequest(BaseModel):
    """Request to configure result caching."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "enableCache": True,
            "ttlSeconds": 300,
            "cacheKey": "product_search_all"
        }
    })
    
    enableCache: bool = Field(..., description="Enable/disable caching")
    ttlSeconds: Optional[int] = Field(300, description="Cache TTL in seconds")
    cacheKey: Optional[str] = Field(None, description="Cache identifier")
    invalidatePrevious: Optional[bool] = Field(False, description="Invalidate previous cache")


class CacheStatistics(BaseModel):
    """Cache statistics."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "hits": 450,
            "misses": 50,
            "hitRate": 0.9,
            "size": 1024000,
            "itemCount": 25
        }
    })
    
    hits: int = Field(..., description="Cache hit count")
    misses: int = Field(..., description="Cache miss count")
    hitRate: float = Field(..., description="Cache hit rate (0.0-1.0)")
    size: int = Field(..., description="Cache size in bytes")
    itemCount: int = Field(..., description="Number of cached items")
    lastClearTime: Optional[str] = Field(None, description="Last cache clear time")


class StreamingRequest(BaseModel):
    """Request for streaming large result sets."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entityType": "Product",
            "chunkSize": 1000,
            "format": "JSON",
            "includeMetadata": True
        }
    })
    
    entityType: str = Field(..., description="Entity type to stream")
    chunkSize: int = Field(1000, description="Entities per chunk")
    format: str = Field("JSON", description="Output format (JSON, CSV, XML)")
    includeMetadata: Optional[bool] = Field(False, description="Include entity metadata")
    filters: Optional[List[Dict[str, Any]]] = Field(None, description="Filters to apply")


class StreamingResponse(BaseModel):
    """Response chunk from streaming operation."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "streamId": "STREAM_001",
            "chunkNumber": 1,
            "totalChunks": 5,
            "entities": [{"entityId": "PROD_001"}],
            "hasMore": True
        }
    })
    
    streamId: str = Field(..., description="Stream identifier")
    chunkNumber: int = Field(..., description="Current chunk number")
    totalChunks: Optional[int] = Field(None, description="Total chunks (if known)")
    entities: List[Dict[str, Any]] = Field(..., description="Entity chunk")
    hasMore: bool = Field(..., description="More chunks available")
    nextToken: Optional[str] = Field(None, description="Token for next chunk")
