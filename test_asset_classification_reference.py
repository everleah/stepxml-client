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
