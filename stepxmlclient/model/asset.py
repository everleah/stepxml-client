from . import BaseObject

class Asset(BaseObject):
    _GROUP_NAME = 'assets'
    _TAG_NAME = 'Asset'
    _ATTRIBUTE_NAMES = ("ID",)
    _TEXT_NAMES = ("Name",)
    _CHILDREN_NAMES = ("Values",)