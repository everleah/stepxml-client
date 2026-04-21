"""Relationship and relation model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class RelationshipTypeResponse(BaseModel):
    """Reference type definition (maps to STEP ``ReferenceType`` schema).

    All fields are optional because the STEP REST API spec declares
    ``required: []`` on this schema.
    """

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "id": "IS_PART_OF",
            "name": "Is Part Of",
            "productClassificationLinkType": False,
            "multivalued": True
        }
    })

    # Primary spec field — the STEP API returns 'id', not 'relationshipTypeId'.
    id: Optional[str] = Field(None, description="Reference type ID (spec field)")
    # Backward-compatible alias so callers that used the old field name still work.
    relationshipTypeId: Optional[str] = Field(None, description="Alias for id (legacy field name)")
    name: Optional[str] = Field(None, description="Display name")
    productClassificationLinkType: Optional[bool] = Field(None, description="Whether this is a classification link type")
    multivalued: Optional[bool] = Field(None, description="Whether multiple targets are allowed")
    validSourceObjectTypes: Optional[List[str]] = Field(None, description="Valid source object types")
    validTargetObjectTypes: Optional[List[str]] = Field(None, description="Valid target object types")
    # Legacy optional fields kept for backward compatibility
    description: Optional[str] = Field(None, description="Type description")
    isDirectional: Optional[bool] = Field(None, description="Whether relationship is directional")
    bidirectionalName: Optional[str] = Field(None, description="Reverse relationship name")


class RelationshipResponse(BaseModel):
    """Single reference/link between entities (maps to STEP ``ReferenceEntry`` schema).

    All fields are optional because the STEP REST API spec declares
    ``required: []`` on ``ReferenceEntry``.  The spec fields are
    ``contextLocal``, ``inherited``, ``target``, ``targetType``, ``values``,
    and ``entity``.
    """

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "target": "PROD_002",
            "targetType": "Product",
            "contextLocal": True,
            "inherited": False
        }
    })

    # Spec-defined fields (ReferenceEntry)
    contextLocal: Optional[bool] = Field(None, description="Whether the reference is context-local")
    inherited: Optional[bool] = Field(None, description="Whether the reference is inherited")
    target: Optional[str] = Field(None, description="Target entity ID")
    targetType: Optional[str] = Field(None, description="Target entity type")
    values: Optional[Dict[str, Any]] = Field(None, description="Reference attribute values")
    entity: Optional[Dict[str, Any]] = Field(None, description="Embedded target entity")
    # Legacy fields kept for backward compatibility
    relationshipId: Optional[str] = Field(None, description="Relationship ID (legacy)")
    relationshipType: Optional[str] = Field(None, description="Relationship type (legacy)")
    sourceId: Optional[str] = Field(None, description="Source entity ID (legacy)")
    targetId: Optional[str] = Field(None, description="Target entity ID (legacy alias for target)")
    sourceType: Optional[str] = Field(None, description="Source entity type (legacy)")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")
    modifiedAt: Optional[str] = Field(None, description="Last modification timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Reference metadata")
    status: Optional[str] = Field(None, description="Reference status")


class RelationshipListResponse(BaseModel):
    """Response containing list of references.

    The STEP REST API spec returns a ``Reference`` schema for list-reference
    endpoints, which has an empty properties definition (``required: []``).
    All fields here are therefore optional.
    """

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "relationships": [],
            "totalCount": 0,
            "limit": 20,
            "offset": 0
        }
    })

    relationships: Optional[List[RelationshipResponse]] = Field(None, description="List of references")
    totalCount: Optional[int] = Field(None, description="Total number of references")
    limit: Optional[int] = Field(None, description="Result limit")
    offset: Optional[int] = Field(None, description="Result offset")


class CrossReferenceResponse(BaseModel):
    """Cross-reference between entities."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "crossReferenceId": "XREF_001",
            "sourceEntityId": "PROD_001",
            "targetEntityId": "PROD_002",
            "referenceType": "RELATED_PRODUCT",
            "description": "Alternative color variant",
            "sequence": 1
        }
    })
    
    crossReferenceId: str = Field(..., description="Unique cross-reference ID")
    sourceEntityId: str = Field(..., description="Source entity ID")
    targetEntityId: str = Field(..., description="Target entity ID")
    referenceType: str = Field(..., description="Type of cross-reference")
    description: Optional[str] = Field(None, description="Reference description")
    sequence: Optional[int] = Field(None, description="Display sequence")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")


class CrossReferenceListResponse(BaseModel):
    """Response containing list of cross-references."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "crossReferences": [
                {"crossReferenceId": "XREF_001", "sourceEntityId": "PROD_001", "targetEntityId": "PROD_002", "referenceType": "RELATED_PRODUCT"}
            ],
            "totalCount": 50,
            "limit": 20,
            "offset": 0
        }
    })
    
    crossReferences: List[CrossReferenceResponse] = Field(..., description="List of cross-references")
    totalCount: int = Field(..., description="Total number of cross-references")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")


class RelationshipCreateRequest(BaseModel):
    """Request to create a new relationship."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "relationshipType": "IS_PART_OF",
            "sourceId": "PROD_001",
            "targetId": "PROD_002",
            "metadata": {"quantity": 5}
        }
    })
    
    relationshipType: str = Field(..., description="Type of relationship to create")
    sourceId: str = Field(..., description="Source entity ID")
    targetId: str = Field(..., description="Target entity ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Relationship metadata")
    status: Optional[str] = Field("ACTIVE", description="Initial status")


class RelationshipUpdateRequest(BaseModel):
    """Request to update an existing relationship."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "metadata": {"quantity": 10},
            "status": "ACTIVE"
        }
    })
    
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata")
    status: Optional[str] = Field(None, description="Updated status")


class CrossReferenceCreateRequest(BaseModel):
    """Request to create a cross-reference."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "sourceEntityId": "PROD_001",
            "targetEntityId": "PROD_002",
            "referenceType": "RELATED_PRODUCT",
            "description": "Alternative color variant",
            "sequence": 1
        }
    })
    
    sourceEntityId: str = Field(..., description="Source entity ID")
    targetEntityId: str = Field(..., description="Target entity ID")
    referenceType: str = Field(..., description="Type of cross-reference")
    description: Optional[str] = Field(None, description="Reference description")
    sequence: Optional[int] = Field(None, description="Display sequence")


class RelationshipGraphResponse(BaseModel):
    """Graph representation of entity relationships."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "rootEntityId": "PROD_001",
            "rootEntityType": "Product",
            "nodes": [
                {"entityId": "PROD_001", "entityType": "Product", "label": "Main Product"}
            ],
            "edges": [
                {"source": "PROD_001", "target": "PROD_002", "relationshipType": "IS_PART_OF"}
            ],
            "depth": 2
        }
    })
    
    rootEntityId: str = Field(..., description="Root entity ID")
    rootEntityType: str = Field(..., description="Root entity type")
    nodes: List[Dict[str, Any]] = Field(..., description="Graph nodes")
    edges: List[Dict[str, Any]] = Field(..., description="Graph edges")
    depth: Optional[int] = Field(None, description="Graph depth/levels")
    totalNodes: Optional[int] = Field(None, description="Total nodes in graph")
    totalEdges: Optional[int] = Field(None, description="Total edges in graph")


class LinkResponse(BaseModel):
    """Product/Asset link or attachment."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "linkId": "LINK_001",
            "sourceId": "PROD_001",
            "targetId": "ASSET_001",
            "linkType": "PRODUCT_IMAGE",
            "sequence": 1,
            "metadata": {"isPrimary": True}
        }
    })
    
    linkId: str = Field(..., description="Unique link ID")
    sourceId: str = Field(..., description="Source entity ID")
    targetId: str = Field(..., description="Target entity ID")
    linkType: str = Field(..., description="Type of link (PRODUCT_IMAGE, PRODUCT_DOCUMENT, etc.)")
    sequence: Optional[int] = Field(None, description="Display sequence")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Link metadata")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")


class LinkListResponse(BaseModel):
    """Response containing list of links."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "links": [
                {"linkId": "LINK_001", "sourceId": "PROD_001", "targetId": "ASSET_001", "linkType": "PRODUCT_IMAGE"}
            ],
            "totalCount": 25,
            "limit": 20,
            "offset": 0
        }
    })
    
    links: List[LinkResponse] = Field(..., description="List of links")
    totalCount: int = Field(..., description="Total number of links")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")


class LinkCreateRequest(BaseModel):
    """Request to create a link."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "sourceId": "PROD_001",
            "targetId": "ASSET_001",
            "linkType": "PRODUCT_IMAGE",
            "sequence": 1
        }
    })
    
    sourceId: str = Field(..., description="Source entity ID")
    targetId: str = Field(..., description="Target entity ID")
    linkType: str = Field(..., description="Type of link")
    sequence: Optional[int] = Field(None, description="Display sequence")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Link metadata")
