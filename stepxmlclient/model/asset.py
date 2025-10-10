from typing import List
from . import BaseObject

class Asset(BaseObject):
    _GROUP_NAME: str = 'assets'
    _TAG_NAME: str = 'Asset'
    _ATTRIBUTE_NAMES: List[str] = ["ID"]
    _TEXT_NAMES: List[str] = ["Name", "KeyValue"]
    _CHILDREN_NAMES: List[str] = ["Values"]