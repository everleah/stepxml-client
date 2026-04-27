from stepxmlclient.creator import Creator
from stepxmlclient.model import Asset


def test_asset_uses_classification_reference_tag():
    """Asset must serialize classification links as ClassificationReference per STEP.xsd."""
    creator = Creator("Context2", "Main")
    asset = Asset({"ID": "PIXXIO_1455587754test", "UserTypeID": "PIXXIO_ASSET"})
    asset._data["Values"] = {
        "AT_PIXXIO_Katalogartikelnummer": {"value": "45663344"},
        "AT_CH_AssetDeleted": {"value": "No"},
    }
    asset.add_classification_reference(classification_id="PIXXIO_ASSETS")

    creator.add(asset)
    creator.build()

    xml = creator.to_string()
    assert "<ClassificationReference ClassificationID=\"PIXXIO_ASSETS\"" in xml
    assert "<ClassificationCrossReference" not in xml


def test_asset_does_not_serialize_asset_or_product_cross_references():
    """AssetType in STEP.xsd does not allow AssetCrossReference/ProductCrossReference children."""
    creator = Creator("Context2", "Main")
    asset = Asset({"ID": "A100", "UserTypeID": "PIXXIO_ASSET"})
    asset._data["AssetCrossReference"] = [{"AssetID": "A200", "Type": "Alt"}]
    asset._data["ProductCrossReference"] = [{"ProductID": "P200", "Type": "Linked"}]
    asset.add_entity_reference(entity_id="E100", type_="Owner")

    creator.add(asset)
    creator.build()

    xml = creator.to_string()
    assert "<AssetCrossReference" not in xml
    assert "<ProductCrossReference" not in xml
    assert "<EntityCrossReference EntityID=\"E100\"" in xml


def test_asset_keyvalue_serializes_as_child_with_keyid_and_text():
    creator = Creator("Context2", "Main")
    asset = Asset({
        "ID": "A300",
        "UserTypeID": "PIXXIO_ASSET",
        "KeyValue": {"KeyID": "ExternalKey", "value": "A300-EXT"},
    })

    creator.add(asset)
    creator.build()

    xml = creator.to_string()
    assert "<KeyValue KeyID=\"ExternalKey\">A300-EXT</KeyValue>" in xml
