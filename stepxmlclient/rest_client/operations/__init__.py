"""REST API operations for STEP REST API v2.

Operation groups for different STEP entity types.
"""

from .assets import AssetOperations
from .attributes import AttributeOperations
from .background_processes import BackgroundProcessOperations
from .batch import BatchOperations
from .classifications import ClassificationOperations
from .collection_groups import CollectionGroupOperations
from .collections import CollectionOperations
from .contexts import ContextOperations
from .data_type_groups import DataTypeGroupOperations
from .entities import EntityOperations
from .event_processors import EventProcessorOperations
from .exports import ExportOperations
from .gateway import GatewayOperations
from .inbound import InboundOperations
from .outbound import OutboundOperations
from .products import ProductOperations
from .relations import RelationOperations
from .reports import ReportOperations
from .system_information import SystemInformationOperations
from .user_groups import UserGroupOperations
from .users import UserOperations
from .workflow_tasks import WorkflowTaskOperations
from .workflows import WorkflowOperations

__all__ = [
    'AssetOperations',
    'AttributeOperations',
    'BackgroundProcessOperations',
    'BatchOperations',
    'ClassificationOperations',
    'CollectionGroupOperations',
    'CollectionOperations',
    'ContextOperations',
    'DataTypeGroupOperations',
    'EntityOperations',
    'EventProcessorOperations',
    'ExportOperations',
    'GatewayOperations',
    'InboundOperations',
    'OutboundOperations',
    'ProductOperations',
    'RelationOperations',
    'ReportOperations',
    'SystemInformationOperations',
    'UserGroupOperations',
    'UserOperations',
    'WorkflowOperations',
    'WorkflowTaskOperations',
]
