"""REST API operations for STEP REST API v2.

Operation groups for different STEP entity types.
"""

from .products import ProductOperations
from .assets import AssetOperations
from .classifications import ClassificationOperations
from .entities import EntityOperations
from .attributes import AttributeOperations
from .metadata import MetadataOperations
from .imports import ImportOperations
from .exports import ExportOperations
from .relations import RelationOperations

__all__ = [
    'ProductOperations',
    'AssetOperations',
    'ClassificationOperations',
    'EntityOperations',
    'AttributeOperations',
    'MetadataOperations',
    'ImportOperations',
    'ExportOperations',
    'RelationOperations',
]
