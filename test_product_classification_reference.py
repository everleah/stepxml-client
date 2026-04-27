from stepxmlclient.creator import Creator
from stepxmlclient.model import Product


def test_product_add_classification_reference_serializes_reference_tag():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P100", "UserTypeID": "UT_PRODUCT"})
    product.add_classification_reference(classification_id="CAT100", type_="category")

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<ClassificationReference ClassificationID=\"CAT100\"" in xml


def test_product_add_classification_cross_reference_serializes_cross_reference_tag():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P101", "UserTypeID": "UT_PRODUCT"})
    product.add_classification_cross_reference(classification_id="CAT101", type_="mapped")

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<ClassificationCrossReference ClassificationID=\"CAT101\"" in xml
