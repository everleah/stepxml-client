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


def test_product_serializes_suppressed_and_delete_suppressed_classification_tags():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P102", "UserTypeID": "UT_PRODUCT"})
    product._data["SuppressedClassificationReference"] = [
        {"ClassificationID": "CAT_SUPP", "Type": "category"}
    ]
    product._data["DeleteSuppressedClassificationReference"] = [
        {"ClassificationID": "CAT_DEL_SUPP", "Type": "category"}
    ]
    product._data["SuppressedClassificationCrossReference"] = [
        {"ClassificationID": "CAT_X_SUPP", "Type": "mapped"}
    ]
    product._data["DeleteSuppressedClassificationCrossReference"] = [
        {"ClassificationID": "CAT_X_DEL_SUPP", "Type": "mapped"}
    ]

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<SuppressedClassificationReference ClassificationID=\"CAT_SUPP\"" in xml
    assert "<DeleteSuppressedClassificationReference ClassificationID=\"CAT_DEL_SUPP\"" in xml
    assert "<SuppressedClassificationCrossReference ClassificationID=\"CAT_X_SUPP\"" in xml
    assert "<DeleteSuppressedClassificationCrossReference ClassificationID=\"CAT_X_DEL_SUPP\"" in xml


def test_product_serializes_workflow_attribute_and_data_container_links():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P103", "UserTypeID": "UT_PRODUCT"})
    product._data["STEPWorkflowStateBind"] = {"WorkflowID": "WF_APPROVAL", "StateID": "STATE_DRAFT"}
    product._data["AttributeLink"] = [{"AttributeID": "ATTR_COLOR"}]
    product._data["DeleteAttributeLink"] = [{"AttributeID": "ATTR_OLD"}]
    product._data["DataContainerTypeLink"] = [{"DataContainerTypeID": "DCT_MARKETING"}]
    product._data["DeleteDataContainerTypeLink"] = [{"DataContainerTypeID": "DCT_OLD"}]

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<STEPWorkflowStateBind WorkflowID=\"WF_APPROVAL\" StateID=\"STATE_DRAFT\"" in xml
    assert "<AttributeLink AttributeID=\"ATTR_COLOR\"" in xml
    assert "<DeleteAttributeLink AttributeID=\"ATTR_OLD\"" in xml
    assert "<DataContainerTypeLink DataContainerTypeID=\"DCT_MARKETING\"" in xml
    assert "<DeleteDataContainerTypeLink DataContainerTypeID=\"DCT_OLD\"" in xml
