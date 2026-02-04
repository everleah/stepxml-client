"""Organization and dimensional models for STEP XML Client.

Defines organizational and dimensional configuration classes including Contexts,
Qualifiers, Dimensions, Tags, and Units used to organize and structure STEP MDM data.
"""

from typing import List, Optional, Any, Dict, TYPE_CHECKING
from . import BaseObject

if TYPE_CHECKING:
    pass


class Context(BaseObject):
    """Context - multi-language/multi-dimensional context for data.
    
    Defines a context in which data can exist with language and dimensional variations.
    Contexts enable organizing data by language, region, or dimensional axes.
    
    Supports:
    - Multiple languages via Name elements
    - Dimension point associations for multi-dimensional data
    - Locale specification (language/region codes)
    - Priority management for cross-context resolution
    - Boolean state tracking (Selected, Referenced, Changed, Deleted)
    
    Attributes:
        ID: Unique context identifier
        Priority: Priority for context resolution
        Locale: Language/locale code (e.g., 'en_US')
        Name: Context name (localized)
        DimensionPointLink: Links to dimension points
        MetaData: Associated metadata
        Selected: Whether context is selected
        Referenced: Whether context is referenced
        Changed: Whether context was changed
        Deleted: Whether context is marked for deletion
    """
    _GROUP_NAME: str = 'contexts'
    _TAG_NAME: str = 'Context'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "Priority", "Locale", "Selected", "Referenced", "Changed", "Deleted"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["DimensionPointLink", "MetaData"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize link lists if not provided
        if "DimensionPointLink" not in self._data:
            self._data["DimensionPointLink"] = []
    
    def add_dimension_point_link(self, dimension_id: str, dimension_point_id: str) -> None:
        """Add a dimension point link to this context.
        
        Args:
            dimension_id: ID of the dimension
            dimension_point_id: ID of the dimension point
        """
        link_dict = {
            "DimensionID": dimension_id,
            "DimensionPointID": dimension_point_id
        }
        
        if not isinstance(self._data["DimensionPointLink"], list):
            self._data["DimensionPointLink"] = []
        self._data["DimensionPointLink"].append(link_dict)


class Qualifier(BaseObject):
    """Qualifier - represents a dimension qualifier or multi-dimensional data point.
    
    Qualifiers enable multi-dimensional attribute management in STEP.
    They combine dimension points to define a specific multi-dimensional position.
    
    Supports:
    - Multiple dimension point associations
    - Multi-language names
    - Metadata tracking
    """
    _GROUP_NAME: str = 'qualifiers'
    _TAG_NAME: str = 'Qualifier'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["DimensionPointLink", "MetaData"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize link lists if not provided
        if "DimensionPointLink" not in self._data:
            self._data["DimensionPointLink"] = []
    
    def add_dimension_point_link(self, dimension_id: str, dimension_point_id: str) -> None:
        """Add a dimension point link to this qualifier.
        
        Args:
            dimension_id: ID of the dimension
            dimension_point_id: ID of the dimension point
        """
        link_dict = {
            "DimensionID": dimension_id,
            "DimensionPointID": dimension_point_id
        }
        
        if not isinstance(self._data["DimensionPointLink"], list):
            self._data["DimensionPointLink"] = []
        self._data["DimensionPointLink"].append(link_dict)


class Dimension(BaseObject):
    """Dimension - defines an axis for multi-dimensional data organization.
    
    Dimensions define categorization axes (e.g., Market, Color, Size) along which
    products and attributes can be organized. Each dimension contains dimension points.
    
    Supports:
    - Dimension points (values/positions along this axis)
    - Multi-language names
    - Duplicate point control
    - Metadata tracking
    """
    _GROUP_NAME: str = 'dimensions'
    _TAG_NAME: str = 'Dimension'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "AllowDuplicates"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["DimensionPoint", "MetaData"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        # Initialize dimension points list if not provided
        if "DimensionPoint" not in self._data:
            self._data["DimensionPoint"] = []
    
    def add_dimension_point(self, dimension_point: Optional['DimensionPoint'] = None,
                           **kwargs) -> None:
        """Add a dimension point to this dimension.
        
        Can be called two ways:
        1. With object: add_dimension_point(dimension_point=point_obj)
        2. With parameters: add_dimension_point(ID="DP001", Name="Point Name")
        """
        if dimension_point is not None:
            point = dimension_point
        else:
            point = DimensionPoint(kwargs)
        
        if not isinstance(self._data["DimensionPoint"], list):
            self._data["DimensionPoint"] = []
        self._data["DimensionPoint"].append(point)


class DimensionPoint(BaseObject):
    """DimensionPoint - represents a point/value within a dimension.
    
    Dimension points define the valid positions or values along a dimension axis.
    For example, a "Color" dimension might have points: Red, Blue, Green.
    
    Supports:
    - Multi-language names
    - Metadata tracking
    """
    _GROUP_NAME: Optional[str] = None  # Used as child element only
    _TAG_NAME: str = 'DimensionPoint'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["MetaData"]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
