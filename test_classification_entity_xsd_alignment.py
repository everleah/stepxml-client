from stepxmlclient.creator import Creator
from stepxmlclient.model import Classification, Entity


def test_classification_supports_new_xsd_children_and_omits_suppressed_product_reference():
    creator = Creator("Context2", "Main")
    classification = Classification({"ID": "C100", "UserTypeID": "UT_CLASS"})
    classification._data["SequenceProduct"] = [{"ProductID": "PSEQ100"}]
    classification._data["DeleteAttributeLink"] = [{"AttributeID": "ATTR_OLD"}]
    classification._data["DeleteDataContainerTypeLink"] = [{"DataContainerTypeID": "DCT_OLD"}]
    classification._data["Tables"] = [{}]
    classification._data["CurrentTasks"] = [{}]
    classification._data["SuppressedProductReference"] = [{"ProductID": "P_SUPP"}]

    creator.add(classification)
    creator.build()

    xml = creator.to_string()
    assert "<SequenceProduct ProductID=\"PSEQ100\"" in xml
    assert "<DeleteAttributeLink AttributeID=\"ATTR_OLD\"" in xml
    assert "<DeleteDataContainerTypeLink DataContainerTypeID=\"DCT_OLD\"" in xml
    assert "<Tables" in xml
    assert "<CurrentTasks" in xml
    assert "<SuppressedProductReference" not in xml


def test_entity_supports_terms_and_current_tasks():
    creator = Creator("Context2", "Main")
    entity = Entity({"ID": "E100", "UserTypeID": "UT_ENTITY"})
    entity._data["CurrentTasks"] = [{}]
    entity._data["Terms"] = [{}]

    creator.add(entity)
    creator.build()

    xml = creator.to_string()
    assert "<CurrentTasks" in xml
    assert "<Terms" in xml


def test_entity_omits_non_entitytype_children():
    creator = Creator("Context2", "Main")
    entity = Entity({"ID": "E101", "UserTypeID": "UT_ENTITY"})
    entity._data["MetaData"] = [{}]
    entity._data["AttributeLink"] = [{"AttributeID": "ATTR1"}]
    entity._data["DataContainerTypeLink"] = [{"DataContainerTypeID": "DCT1"}]

    creator.add(entity)
    creator.build()

    xml = creator.to_string()
    assert "<MetaData" not in xml
    assert "<AttributeLink" not in xml
    assert "<DataContainerTypeLink" not in xml
