from stepxmlclient.creator import Creator
from stepxmlclient.model import (
    Product,
    Asset,
    STEPWorkflowStateBind,
    SequenceProduct,
    PackagingReference,
    AssetPushLocation,
    AssetContent,
    AssetContentSpecification,
    AssetBinaryContent,
    BinaryContent,
)


def test_product_accepts_prebuilt_complex_objects():
    creator = Creator("Context2", "Main")
    product = Product({"ID": "P300", "UserTypeID": "UT_PRODUCT"})

    product.set_workflow_state_bind(
        bind_object=STEPWorkflowStateBind({"WorkflowID": "WF_PRE", "StateID": "S_PRE"})
    )
    product.add_sequence_product(sequence_object=SequenceProduct({"ID": "P_CHILD", "Changed": False}))
    product.add_packaging_reference(packaging_object=PackagingReference({"ProductID": "P_BOX", "Quantity": "12"}))

    creator.add(product)
    creator.build()

    xml = creator.to_string()
    assert "<STEPWorkflowStateBind WorkflowID=\"WF_PRE\" StateID=\"S_PRE\"" in xml
    assert "<SequenceProduct ID=\"P_CHILD\" Changed=\"False\"" in xml
    assert "<PackagingReference ProductID=\"P_BOX\" Quantity=\"12\"" in xml


def test_asset_accepts_prebuilt_complex_objects():
    creator = Creator("Context2", "Main")
    asset = Asset({"ID": "A300", "UserTypeID": "UT_ASSET"})

    asset.add_asset_push_location_object(
        AssetPushLocation({"ConfigurationID": "CFG_PRE", "Status": "DONE", "value": "https://push.example"})
    )

    content = AssetContent(
        {
            "QualifierID": "en",
            "AssetContentSpecification": [
                AssetContentSpecification(
                    {
                        "ImageConversionConfigurationID": "IMG_CFG",
                        "IncludesBinaryContent": True,
                        "RelativeURL": "/assets/a300.jpg",
                    }
                )
            ],
        }
    )
    asset.add_asset_content(content_object=content)

    binary = AssetBinaryContent(
        {
            "MIMEType": "image/jpeg",
            "Filename": "a300.jpg",
            "BinaryContent": BinaryContent({"value": "YmFzZTY0"}),
        }
    )
    asset.add_asset_binary_content(binary_content_object=binary)

    creator.add(asset)
    creator.build()

    xml = creator.to_string()
    assert "<AssetPushLocation Status=\"DONE\" ConfigurationID=\"CFG_PRE\"" in xml
    assert ">https://push.example</AssetPushLocation>" in xml
    assert "<AssetContent QualifierID=\"en\"" in xml
    assert "<AssetContentSpecification ImageConversionConfigurationID=\"IMG_CFG\" IncludesBinaryContent=\"True\" RelativeURL=\"/assets/a300.jpg\"" in xml
    assert "<AssetBinaryContent MIMEType=\"image/jpeg\" Filename=\"a300.jpg\"" in xml
    assert "<BinaryContent>YmFzZTY0</BinaryContent>" in xml
