"""Extended STEP REST API client with operation groups.

Extends the base StiboStepRestClient to provide organized access to
operation groups for different STEP entities.
"""

import logging
from typing import Optional

from ..client import StiboStepRestClient
from .base import BaseOperation
from .operations.products import ProductOperations
from .operations.assets import AssetOperations
from .operations.classifications import ClassificationOperations
from .operations.entities import EntityOperations
from .operations.attributes import AttributeOperations
from .operations.metadata import MetadataOperations
from .operations.imports import ImportOperations
from .operations.exports import ExportOperations
from .operations.relations import RelationOperations
from .operations.bulk import (
    BulkOperations,
    WorkflowOperations,
    AdvancedSearchOperations,
    CacheOperations,
    StreamingOperations,
)


class StepRestClient(StiboStepRestClient):
    """Extended REST client with organized operation groups.
    
    Inherits authentication and base functionality from StiboStepRestClient,
    adding domain-specific operation groups for easier API access.
    
    Attributes:
        products: ProductOperations instance
        assets: AssetOperations instance
        classifications: ClassificationOperations instance
        entities: EntityOperations instance
        attributes: AttributeOperations instance
        metadata: MetadataOperations instance
        imports: ImportOperations instance
        exports: ExportOperations instance
        relations: RelationOperations instance
        bulk: BulkOperations instance
        workflows: WorkflowOperations instance
        search: AdvancedSearchOperations instance
        cache: CacheOperations instance
        streaming: StreamingOperations instance
        attributes: AttributeOperations instance
        metadata: MetadataOperations instance
        imports: ImportOperations instance
        exports: ExportOperations instance
        relations: RelationOperations instance
    """
    
    def __init__(self, location_base, authorisation,
                 openapi_file=None, logger=None,
                 proxies=None, ssl_version=None,
                 cache_openapi=False, nocert=False,
                 context: Optional[str] = None, workspace: Optional[str] = None):
        """Initialize StepRestClient with operation groups.
        
        Args:
            location_base: Base URL of STEP REST API
            authorisation: Authentication handler (e.g., BasicAuthorisation)
            openapi_file: Path to OpenAPI specification file
            logger: Logger instance
            proxies: Proxy configuration
            ssl_version: SSL version configuration
            cache_openapi: Whether to cache OpenAPI spec
            nocert: Whether to skip SSL certificate verification
            context: STEP context ID passed to all context-aware API calls
            workspace: STEP workspace ID (server defaults to "Main" if not supplied)
        """
        # Initialize parent class
        super().__init__(
            location_base=location_base,
            authorisation=authorisation,
            openapi_file=openapi_file,
            logger=logger,
            proxies=proxies,
            ssl_version=ssl_version,
            cache_openapi=cache_openapi,
            nocert=nocert
        )
        
        # Get logger for operation groups
        if logger is None:
            op_logger = logging.getLogger(f"{self.__class__.__module__}.operations")
        else:
            op_logger = logger
        
        # Initialize operation groups (context/workspace passed to entity-level operations)
        self.products = ProductOperations(self.client, logger=op_logger, context=context, workspace=workspace)
        self.assets = AssetOperations(self.client, logger=op_logger, context=context, workspace=workspace)
        self.classifications = ClassificationOperations(self.client, logger=op_logger, context=context, workspace=workspace)
        self.entities = EntityOperations(self.client, logger=op_logger, context=context, workspace=workspace)
        self.attributes = AttributeOperations(self.client, logger=op_logger, context=context, workspace=workspace)
        self.relations = RelationOperations(self.client, logger=op_logger, context=context, workspace=workspace)
        # Metadata, imports, exports, bulk and streaming operate on system/job level - no per-call context
        self.metadata = MetadataOperations(self.client, logger=op_logger)
        self.imports = ImportOperations(self.client, logger=op_logger)
        self.exports = ExportOperations(self.client, logger=op_logger)
        self.bulk = BulkOperations(self.client, logger=op_logger)
        self.workflows = WorkflowOperations(self.client, logger=op_logger)
        self.search = AdvancedSearchOperations(self.client, logger=op_logger)
        self.cache = CacheOperations(self.client, logger=op_logger)
        self.streaming = StreamingOperations(self.client, logger=op_logger)
    
    def get_operation_group(self, group_name: str) -> Optional[BaseOperation]:
        """Get an operation group by name.
        
        Useful for dynamic access to operation groups.
        
        Args:
            group_name: Name of operation group (e.g., 'products', 'assets')
            
        Returns:
            Operation group instance or None if not found
        """
        return getattr(self, group_name, None)
