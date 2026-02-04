"""Extended STEP REST API client with operation groups.

Extends the base StiboStepRestClient to provide organized access to
operation groups for different STEP entities.
"""

import logging
from typing import Optional

from ..client import StiboStepRestClient
from .base import BaseOperation


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
    """
    
    def __init__(self, location_base, authorisation,
                 openapi_file=None, logger=None,
                 proxies=None, ssl_version=None,
                 cache_openapi=False, nocert=False):
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
        
        # Initialize operation groups (will be implemented in subsequent phases)
        # These are placeholders showing the intended structure
        self.products = None  # ProductOperations(self.client, logger=op_logger)
        self.assets = None    # AssetOperations(self.client, logger=op_logger)
        self.classifications = None  # ClassificationOperations(self.client, logger=op_logger)
        self.entities = None  # EntityOperations(self.client, logger=op_logger)
        self.attributes = None  # AttributeOperations(self.client, logger=op_logger)
        self.metadata = None  # MetadataOperations(self.client, logger=op_logger)
        self.imports = None   # ImportOperations(self.client, logger=op_logger)
        self.exports = None   # ExportOperations(self.client, logger=op_logger)
    
    def get_operation_group(self, group_name: str) -> Optional[BaseOperation]:
        """Get an operation group by name.
        
        Useful for dynamic access to operation groups.
        
        Args:
            group_name: Name of operation group (e.g., 'products', 'assets')
            
        Returns:
            Operation group instance or None if not found
        """
        return getattr(self, group_name, None)
