"""Attribute model classes for STEP REST API v2."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class AttributeValue(BaseModel):
    """Individual attribute value."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "value": "Blue",
            "context": "Context1",
            "language": "en"
        }
    })
    
    value: Any = Field(..., description="The attribute value")
    context: str | None = Field(None, description="Context for this value")
    language: str | None = Field(None, description="Language code")


class ListOfValueItem(BaseModel):
    """Individual item in a List of Values."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "LOV_ITEM_001",
            "name": "Option 1",
            "description": "First option",
            "sequence": 1
        }
    })
    
    id: str = Field(..., description="LOV item ID")
    name: str = Field(..., description="LOV item name")
    description: str | None = Field(None, description="LOV item description")
    sequence: Optional[int] = Field(None, description="Display sequence")


class ListOfValueResponse(BaseModel):
    """Response containing List of Values (maps to STEP ``ListOfValues`` schema).

    ``values`` contains metadata keyed by attribute ID, not LOV entries.
    Entries are retrieved separately through get_list_of_values_entries().
    Legacy entry lists in ``values`` and ``items`` remain accepted.
    """

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "id": "LOV_001",
            "name": "Color LOV",
            "extendable": False,
            "usesValueIds": True,
            "values": {"Description": {"value": {"value": "Color choices"}}}
        }
    })

    id: str | None = Field(None, description="LOV ID")
    name: str | None = Field(None, description="LOV name")
    extendable: Optional[bool] = Field(None, description="Whether users can extend the LOV")
    usesValueIds: Optional[bool] = Field(None, description="Whether values have explicit IDs")
    validator: Optional[Dict[str, Any]] = Field(None, description="Value validator")
    dataTypeGroups: Optional[List[str]] = Field(None, description="Data type group IDs")
    values: Optional[Dict[str, Any] | List[ListOfValueItem]] = Field(
        None, description="Metadata keyed by attribute ID (legacy entry lists accepted)")
    # Backward-compatible alias — some callers may have used 'items'
    items: Optional[List[ListOfValueItem]] = Field(None, description="Alias for values (legacy field name)")
    total: Optional[int] = Field(None, description="Total number of items")


class AttributeMetadata(BaseModel):
    """Metadata about an attribute."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "type": "Text",
            "required": True,
            "multiValued": False,
            "createdAt": "2025-01-01T00:00:00Z",
            "modifiedAt": "2025-01-02T00:00:00Z"
        }
    })
    
    type: str = Field(..., description="Attribute data type (Text, Number, Boolean, etc.)")
    required: Optional[bool] = Field(None, description="Whether attribute is required")
    multiValued: Optional[bool] = Field(None, description="Whether attribute supports multiple values")
    createdAt: str | None = Field(None, description="Creation timestamp")
    modifiedAt: str | None = Field(None, description="Last modification timestamp")


class AttributeResponse(BaseModel):
    """Attribute definition with STEP fields and optional legacy aliases."""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "ATTR_001",
            "name": "Color",
            "validator": {"name": "text"},
            "multivalued": False,
            "listOfValues": "LOV_001"
        }
    })
    
    id: str = Field(..., description="Attribute ID")
    name: str | None = Field(None, description="Attribute name")
    validator: Optional[Dict[str, Any]] = Field(None, description="Attribute validator")
    multivalued: Optional[bool] = Field(None, description="Supports multiple values")
    calculated: Optional[bool] = Field(None, description="Whether the attribute is calculated")
    specification: Optional[bool] = Field(None, description="Whether the attribute is a specification")
    dataTypeGroups: Optional[List[str]] = Field(None, description="Data type group IDs")
    listOfValues: str | None = Field(None, description="Associated list of values ID")
    units: Optional[List[str]] = Field(None, description="Valid unit IDs")
    defaultUnit: str | None = Field(None, description="Default unit ID")
    values: Optional[Dict[str, Any]] = Field(None, description="Metadata keyed by attribute ID")
    validForObjectTypes: Optional[List[str]] = Field(None, description="Valid object type IDs")
    description: str | None = Field(None, description="Attribute description")
    type: str | None = Field(None, description="Legacy attribute data type")
    lovId: str | None = Field(None, description="Associated List of Values ID")
    required: Optional[bool] = Field(None, description="Is required")
    multiValued: Optional[bool] = Field(None, description="Supports multiple values")
    metadata: Optional[AttributeMetadata] = Field(None, description="Attribute metadata")
