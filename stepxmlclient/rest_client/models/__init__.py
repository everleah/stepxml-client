"""REST API models for STEP REST API v2.

Provides Pydantic models for request/response handling and validation.
"""

from .common import (
    PageInfo,
    PagedResponse,
    ErrorDetail,
    ErrorResponse,
    ApiResponse,
    SearchFilter,
    SearchRequest,
    SuccessResponse,
    ListResponse,
)
from .product import (
    ProductResponse,
    ProductListResponse,
    ProductSearchRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
)
from .asset import (
    AssetResponse,
    AssetListResponse,
    AssetSearchRequest,
    AssetCreateRequest,
    AssetUpdateRequest,
    AssetUploadRequest,
    AssetDownloadResponse,
    AssetMetadata,
)
from .classification import (
    ClassificationResponse,
    ClassificationListResponse,
    ClassificationCreateRequest,
    ClassificationUpdateRequest,
)
from .entity import (
    EntityResponse,
    EntityListResponse,
    EntityCreateRequest,
    EntityUpdateRequest,
    EntityRelationshipResponse,
)
from .attribute import (
    AttributeResponse,
    AttributeMetadata,
    AttributeValue,
    ListOfValueResponse,
    ListOfValueItem,
)
from .import_export import (
    BackgroundProcessResponse,
    ExportJobCreateRequest,
)
from .relations import (
    RelationshipTypeResponse,
    RelationshipResponse,
    RelationshipListResponse,
    RelationshipCreateRequest,
    RelationshipUpdateRequest,
    CrossReferenceResponse,
    CrossReferenceListResponse,
    CrossReferenceCreateRequest,
    LinkResponse,
    LinkListResponse,
    LinkCreateRequest,
    RelationshipGraphResponse,
)
from .context import (
    ContextResponse,
)
from .system_information import (
    SystemInformationResponse,
)
from .user import (
    UserResponse,
    UserGroupResponse,
)
from .collection import (
    CollectionResponse,
    CollectionGroupResponse,
)
from .background_process import (
    BackgroundProcessResponse,
)
from .event_processor import (
    EventProcessorResponse,
)
from .integration_endpoint import (
    IntegrationEndpointResponse,
)
from .workflow import (
    WorkflowResponse,
    WorkflowTaskResponse,
)
from .batch import (
    BatchRequest,
    BatchResponse,
    OperationRequest,
    OperationResponse,
)
from .data_type_group import (
    DataTypeGroupResponse,
)

__all__ = [
    'PageInfo',
    'PagedResponse',
    'ErrorDetail',
    'ErrorResponse',
    'ApiResponse',
    'SearchFilter',
    'SearchRequest',
    'SuccessResponse',
    'ListResponse',
    'ProductResponse',
    'ProductListResponse',
    'ProductSearchRequest',
    'ProductCreateRequest',
    'ProductUpdateRequest',
    'AssetResponse',
    'AssetListResponse',
    'AssetSearchRequest',
    'AssetCreateRequest',
    'AssetUpdateRequest',
    'AssetUploadRequest',
    'AssetDownloadResponse',
    'AssetMetadata',
    'ClassificationResponse',
    'ClassificationListResponse',
    'ClassificationCreateRequest',
    'ClassificationUpdateRequest',
    'EntityResponse',
    'EntityListResponse',
    'EntityCreateRequest',
    'EntityUpdateRequest',
    'EntityRelationshipResponse',
    'AttributeResponse',
    'AttributeMetadata',
    'AttributeValue',
    'ListOfValueResponse',
    'ListOfValueItem',
    'BackgroundProcessResponse',
    'ExportJobCreateRequest',
    'RelationshipTypeResponse',
    'RelationshipResponse',
    'RelationshipListResponse',
    'RelationshipCreateRequest',
    'RelationshipUpdateRequest',
    'CrossReferenceResponse',
    'CrossReferenceListResponse',
    'CrossReferenceCreateRequest',
    'LinkResponse',
    'LinkListResponse',
    'LinkCreateRequest',
    'RelationshipGraphResponse',
    'WorkflowResponse',
    'WorkflowTaskResponse',
    'ContextResponse',
    'SystemInformationResponse',
    'UserResponse',
    'UserGroupResponse',
    'CollectionResponse',
    'CollectionGroupResponse',
    'EventProcessorResponse',
    'IntegrationEndpointResponse',
    'BatchRequest',
    'BatchResponse',
    'OperationRequest',
    'OperationResponse',
    'DataTypeGroupResponse',
]
