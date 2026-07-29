from stepxmlclient.creator import Creator
from stepxmlclient.model import Product, Asset


def test_product_new_helpers_serialize_expected_tags():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P200", "UserTypeID": "UT_PRODUCT"})

    product.set_workflow_state_bind(workflow_id="WF1", state_id="S1")
    product.add_sequence_product(product_id="P201")
    product.add_current_task({})
    product.add_term({})
    product.add_table({})
    product.add_override_sub_product({})
    product.add_packaging_reference({})

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<STEPWorkflowStateBind WorkflowID=\"WF1\" StateID=\"S1\"" in xml
    assert "<SequenceProduct ID=\"P201\"" in xml
    assert "<CurrentTasks" in xml
    assert "<Terms" in xml
    assert "<Tables" in xml
    assert "<OverrideSubProduct" in xml
    assert "<PackagingReference" in xml


def test_asset_new_helpers_serialize_expected_tags():
    creator = Creator("Context2", "Main")
    asset = Asset({"ID": "A200", "UserTypeID": "UT_ASSET"})

    asset.add_asset_push_location({"ConfigurationID": "CFG1", "Status": "DONE"})
    asset.add_current_task({})
    asset.add_page({})
    asset.add_asset_content({})
    asset.add_asset_binary_content({})

    creator.add(asset)
    creator.build()

    xml = creator.to_string()
    assert "<AssetPushLocation" in xml
    assert "<CurrentTasks" in xml
    assert "<Pages" in xml
    assert "<AssetContent" in xml
    assert "<AssetBinaryContent" in xml


def test_product_workflow_helper_normalizes_legacy_keys():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P201", "UserTypeID": "UT_PRODUCT"})
    product.set_workflow_state_bind(bind_data={"ID": "WF2", "CurrentStateID": "S2"})

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<STEPWorkflowStateBind WorkflowID=\"WF2\" StateID=\"S2\"" in xml
