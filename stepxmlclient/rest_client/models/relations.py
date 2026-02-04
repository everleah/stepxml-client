"""Relationship and relation model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class RelationshipTypeResponse(BaseModel):
    """Relationship type definition."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "relationshipTypeId": "IS_PART_OF",
            "name": "Is Part Of",
            "description": "Component relationship",
            "isDirectional": True,
            "bidirectionalName": "HAS_PART"
        }
    })
    
    relationshipTypeId: str = Field(..., description="Unique relationship type ID")
    name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Type description")
    isDirectional: Optional[bool] = Field(False, description="Whether relationship is directional")
    bidirectionalName: Optional[str] = Field(None, description="Reverse relationship name")


class RelationshipResponse(BaseModel):
    """Single relationship/link between entities."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "relationshipId": "REL_001",
            "relationshipType": "IS_PART_OF",
            "sourceId": "PROD_001",
            "targetId": "PROD_002",
            "sourceType": "Product",
            "targetType": "Product",
            "createdAt": "2025-01-01T00:00:00Z",
            "metadata": {"quantity": 5, "unit": "pieces"}
        }
    })
    
    relationshipId: str = Field(..., description="Unique relationship ID")
    relationshipType: str = Field(..., description="Type of relationship")
    sourceId: str = Field(..., description="Source entity ID")
    targetId: str = Field(..., description="Target entity ID")
    sourceType: str = Field(..., description="Source entity type (Product, Asset, etc.)")
    targetType: str = Field(..., description="Target entity type")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")
    modifiedAt: Optional[str] = Field(None, description="Last modification timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Relationship metadata")
    status: Optional[str] = Field(None, description="Relationship status (ACTIVE, INACTIVE)")


class RelationshipListResponse(BaseModel):
    """Response containing list of relationships."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "relationships": [
                {"relationshipId": "REL_001", "relationshipType": "IS_PART_OF", "sourceId": "PROD_001", "targetId": "PROD_002", "sourceType": "Product", "targetType": "Product"}
            ],
            "totalCount": 150,
            "limit": 20,
            "offset": 0
        }
    })
    
    relationships: List[RelationshipResponse] = Field(..., description="List of relationships")
    totalCount: int = Field(..., description="Total number of relationships")
    limit: int = Field(..., description="Result limit")
    offset: int = Field(..., description="Result offset")


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
