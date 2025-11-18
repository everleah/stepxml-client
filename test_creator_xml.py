from stepxmlclient.creator import Creator
from stepxmlclient.model.asset import Asset
from stepxmlclient.model.product import Product

# Minimal test data
assets = [
    Asset({"ID": "A1", "Name": "Asset One", "KeyValue": "K1", "Values": {"AttrA": {"ID": "V1", "value": "Val1"}}}),
    Asset({"ID": "A2", "Name": "Asset Two", "KeyValue": "K2", "Values": {"AttrA": {"ID": "V2", "value": "Val2"}}})
]
products = [
    Product({"ID": "P1", "ParentId": "", "UserTypeID": "TypeA", "Name": "Product One", "Values": {"Attr1": {"ID": "PV1", "value": "PVal1"}}}),
    Product({"ID": "P2", "ParentId": "", "UserTypeID": "TypeA", "Name": "Product Two", "Values": {"Attr1": {"ID": "PV2", "value": "PVal2"}}})
]

def test_creator():
    creator = Creator("TestContext")
    for asset in assets:
        creator.add(asset)
    for product in products:
        creator.add(product)
    creator.build()
    xml_bytes = creator.to_bytes()
    print(xml_bytes.decode("utf-8"))

if __name__ == "__main__":
    test_creator()
