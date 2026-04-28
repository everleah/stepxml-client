"""Product-related REST API models.

Provides Pydantic models aligned with STEP REST API v2 product schemas.
"""

from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class ProductResponse(BaseModel):
    """Single product response data.

    Mirrors the REST API Product schema:
    - objectType/parent describe product placement and type
    - values/references are dynamic maps keyed by ID
    - attributeLinks/dataContainers are typed arrays/maps from API
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "PROD123",
                "name": "Example Product",
                "objectType": "SalesItem",
                "parent": "I-Level3-122",
                "values": {
                    "UPC": {
                        "value": {
                            "value": "445555555575"
                        }
                    }
                },
                "references": {
                    "Accessory": {
                        "references": [
                            {
                                "target": "I-SalesItem-1111"
                            }
                        ]
                    }
                },
                "attributeLinks": [],
                "dataContainers": {}
            }
        }
    )

    id: str = Field(..., description="Product ID")
    name: Optional[str] = Field(None, description="Product name/description")
    objectType: Optional[str] = Field(None, description="Object type ID")
    parent: Optional[str] = Field(None, description="Parent product ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Product values keyed by attribute ID")
    references: Optional[Dict[str, Any]] = Field(None, description="References keyed by reference type ID")
    attributeLinks: Optional[List[Dict[str, Any]]] = Field(None, description="Attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Data containers keyed by type ID")


class ProductListResponse(BaseModel):
    """Paginated product list response.
    
    Attributes:
        items: List of ProductResponse objects
        total: Total number of products
        limit: Items per page
        offset: Current offset
        has_more: Whether more results are available
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],
                "total": 150,
                "limit": 20,
                "offset": 0,
                "has_more": True
            }
        }
    )
    
    items: List[ProductResponse] = Field(default_factory=list, description="Products in this page")
    total: Optional[int] = Field(None, ge=0, description="Total number of products")
    limit: int = Field(20, ge=1, le=1000, description="Items per page")
    offset: int = Field(0, ge=0, description="Current offset")
    has_more: bool = Field(False, description="Whether more results are available")


class ProductSearchRequest(BaseModel):
    """Search request for products.
    
    Attributes:
        query: Free-text search query
        object_type: Filter by object type
        modified_since: Only products modified after this date (ISO 8601)
        limit: Max results to return
        offset: Result offset for pagination
        include_values: Whether to include product values
        include_attributes: Whether to include attributes
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "*",
                "object_type": "SalesItem",
                "limit": 20,
                "offset": 0,
                "include_values": True,
                "include_attributes": True
            }
        }
    )

    query: str = Field("*", description="Free-text search query (default: all)")
    object_type: Optional[str] = Field(None, description="Filter by object type")
    modified_since: Optional[str] = Field(None, description="ISO 8601 timestamp filter")
    limit: int = Field(20, ge=1, le=1000, description="Max results")
    offset: int = Field(0, ge=0, description="Result offset")
    include_values: bool = Field(True, description="Include product values")
    include_attributes: bool = Field(True, description="Include product attributes")


class ProductCreateRequest(BaseModel):
    """Request to create a new product.
    
    Attributes:
        objectType: Object type ID (required)
        parent: Parent product ID (required)
        name: Product name/description
        values: Product values map keyed by attribute ID
        references: Product references map keyed by reference/link type ID
        attributeLinks: Product attribute links
        dataContainers: Product data containers keyed by data container type ID
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "objectType": "SalesItem",
                "parent": "I-Level3-122",
                "name": "New Product",
                "values": {
                    "UPC": {
                        "value": {
                            "value": "445555555575"
                        }
                    }
                },
                "references": {},
                "attributeLinks": [],
                "dataContainers": {}
            }
        }
    )

    objectType: str = Field(..., description="Object type ID")
    parent: str = Field(..., description="Parent product ID")
    name: Optional[str] = Field(None, description="Product name/description")
    values: Optional[Dict[str, Any]] = Field(None, description="Product values")
    references: Optional[Dict[str, Any]] = Field(None, description="Product references")
    attributeLinks: Optional[List[Dict[str, Any]]] = Field(None, description="Product attribute links")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Product data containers")


class ProductUpdateRequest(BaseModel):
    """Request to update an existing product.
    
    Attributes:
        name: Updated product name/description
        parent: Optional new parent product ID
        values: Updated product values
        references: Updated references
        attributeLinks: Updated attribute links
        dataContainers: Updated data containers
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Product Name",
                "parent": "ElectricGuitars",
                "values": {
                    "Body": {
                        "value": {
                            "value": "Alder"
                        }
                    }
                },
                "references": {}
            }
        }
    )

    name: Optional[str] = Field(None, description="Updated product name")
    parent: Optional[str] = Field(None, description="Updated parent product ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Values to update")
    references: Optional[Dict[str, Any]] = Field(None, description="References to update")
    attributeLinks: Optional[List[Dict[str, Any]]] = Field(None, description="Attribute links to update")
    dataContainers: Optional[Dict[str, Any]] = Field(None, description="Data containers to update")
