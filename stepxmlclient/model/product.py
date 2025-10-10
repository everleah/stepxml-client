from typing import List
from . import BaseObject

class Product(BaseObject):
    _GROUP_NAME: str = 'products'
    _TAG_NAME: str = 'Product'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentId", "UserTypeID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = [
        "Values", "AssetCrossReference", "DeleteAssetCrossReference"]

class ProductReplacementRule(BaseObject):
    _GROUP_NAME: str = 'product_replacement_rules'
    _TAG_NAME: str = 'Product'
    _ATTRIBUTE_NAMES: List[str] = ["ID", "ParentId", "UserTypeID"]
    _TEXT_NAMES: List[str] = ["Name"]
    _CHILDREN_NAMES: List[str] = ["Values"]