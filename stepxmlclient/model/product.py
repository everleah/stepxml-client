from . import BaseObject

class Product(BaseObject):
    _GROUP_NAME = 'products'
    _TAG_NAME = 'Product'
    _ATTRIBUTE_NAMES = ("ID", "ParentId", "UserTypeID")
    _TEXT_NAMES = ("Name",)
    _CHILDREN_NAMES = (
        "Values", "AssetCrossReference", "DeleteAssetCrossReference")
    
    
class ProductReplacementRule(BaseObject):
    _GROUP_NAME = 'product_replacement_rules'
    _TAG_NAME = 'Product'
    
    

    