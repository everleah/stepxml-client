"""Product-related REST API models.

Provides Pydantic models for product data, search requests, and CRUD operations.
"""

from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class ProductAttribute(BaseModel):
    """Single product attribute with value.
    
    Attributes:
        name: Attribute name/ID
        value: Attribute value
        context: Context of the attribute (if context-dependent)
        language: Language code (if multilingual)
    """
    
    name: str = Field(..., description="Attribute name/ID")
    value: Any = Field(..., description="Attribute value")
    context: Optional[str] = Field(None, description="Context if applicable")
    language: Optional[str] = Field(None, description="Language code if multilingual")


class ProductValue(BaseModel):
    """Product value (variant/SKU).
    
    Attributes:
        id: Value/SKU ID
        attributes: Attributes specific to this value
        key_values: Key-value pairs for identification
    """
    
    id: str = Field(..., description="Value/SKU ID")
    attributes: Optional[List[ProductAttribute]] = Field(None, description="Value-specific attributes")
    key_values: Optional[Dict[str, Any]] = Field(None, description="Key-value pairs")


class CrossReference(BaseModel):
    """Cross-reference to another entity.
    
    Attributes:
        type: Type of reference (Product, Asset, Classification, Entity)
        target_id: ID of referenced entity
        attributes: Attributes of the cross-reference
    """
    
    type: str = Field(..., description="Reference type")
    target_id: str = Field(..., description="ID of referenced entity")
    attributes: Optional[Dict[str, Any]] = Field(None, description="Reference attributes")


class ProductResponse(BaseModel):
    """Single product response data.
    
    Attributes:
        id: Product ID
        user_type_id: User type/classification
        name: Product name/description
        attributes: Product attributes
        values: Product values/variants
        cross_references: Cross-references to other entities
        created_date: Creation timestamp
        modified_date: Last modification timestamp
        version: Product version number
        metadata: Additional metadata
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "PROD123",
                "user_type_id": "Product",
                "name": "Example Product",
                "attributes": [],
                "values": [],
                "cross_references": [],
                "created_date": "2024-01-01T00:00:00Z",
                "modified_date": "2024-02-04T10:00:00Z",
                "version": 1,
                "metadata": {}
            }
        }
    )
    
    id: str = Field(..., description="Product ID")
    user_type_id: Optional[str] = Field(None, description="User type/classification")
    name: Optional[str] = Field(None, description="Product name/description")
    attributes: Optional[List[ProductAttribute]] = Field(default_factory=list, description="Product attributes")
    values: Optional[List[ProductValue]] = Field(default_factory=list, description="Product values/variants")
    cross_references: Optional[List[CrossReference]] = Field(default_factory=list, description="Cross-references")
    created_date: Optional[str] = Field(None, description="Creation timestamp")
    modified_date: Optional[str] = Field(None, description="Last modification timestamp")
    version: Optional[int] = Field(None, description="Product version")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


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
        user_type_id: Filter by user type
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
                "limit": 20,
                "offset": 0,
                "include_values": True,
                "include_attributes": True
            }
        }
    )
    
    query: str = Field("*", description="Free-text search query (default: all)")
    user_type_id: Optional[str] = Field(None, description="Filter by user type")
    modified_since: Optional[str] = Field(None, description="ISO 8601 timestamp filter")
    limit: int = Field(20, ge=1, le=1000, description="Max results")
    offset: int = Field(0, ge=0, description="Result offset")
    include_values: bool = Field(True, description="Include product values")
    include_attributes: bool = Field(True, description="Include product attributes")


class ProductCreateRequest(BaseModel):
    """Request to create a new product.
    
    Attributes:
        id: Product ID (required)
        user_type_id: User type/classification
        name: Product name/description
        attributes: Initial attributes
        values: Initial values/variants
        cross_references: Initial cross-references
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "NEWPROD123",
                "user_type_id": "Product",
                "name": "New Product",
                "attributes": [],
                "values": [],
                "cross_references": []
            }
        }
    )
    
    id: str = Field(..., description="Product ID")
    user_type_id: Optional[str] = Field(None, description="User type/classification")
    name: Optional[str] = Field(None, description="Product name/description")
    attributes: Optional[List[ProductAttribute]] = Field(None, description="Initial attributes")
    values: Optional[List[ProductValue]] = Field(None, description="Initial values/variants")
    cross_references: Optional[List[CrossReference]] = Field(None, description="Initial cross-references")


class ProductUpdateRequest(BaseModel):
    """Request to update an existing product.
    
    Attributes:
        name: Updated product name/description
        attributes: Updated attributes (merged with existing)
        values: Updated values/variants (merged with existing)
        cross_references: Updated cross-references (merged with existing)
        user_type_id: Updated user type
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Product Name",
                "attributes": [],
                "user_type_id": "Product"
            }
        }
    )
    
    name: Optional[str] = Field(None, description="Updated product name")
    user_type_id: Optional[str] = Field(None, description="Updated user type")
    attributes: Optional[List[ProductAttribute]] = Field(None, description="Attributes to update")
    values: Optional[List[ProductValue]] = Field(None, description="Values to update")
    cross_references: Optional[List[CrossReference]] = Field(None, description="Cross-references to update")
