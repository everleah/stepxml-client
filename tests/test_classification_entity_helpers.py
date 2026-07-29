from stepxmlclient.creator import Creator
from stepxmlclient.model import (
    Classification,
    Entity,
    Asset,
    SequenceProduct,
    Task,
    CurrentTasks,
    Term,
    Terms,
    Tables,
)


def test_classification_helpers_accept_prebuilt_objects():
    creator = Creator("Context2", "Main")
    classification = Classification({"ID": "C200", "UserTypeID": "UT_CLASS"})

    classification.add_sequence_product(sequence_object=SequenceProduct({"ID": "PSEQ200"}))
    classification.add_current_task(
        current_tasks_object=CurrentTasks(
            {"Task": [Task({"STEPWorkflowID": "WF1", "StateID": "S1", "AssigneeID": "U1", "AssignedToGroup": True, "EntryTime": "2026-01-01T00:00:00Z"})]}
        )
    )
    classification.add_table(tables_object=Tables({"Table": [{"ID": "T1"}]}))
    classification.add_asset(asset=Asset({"ID": "A900", "UserTypeID": "UT_ASSET"}))

    creator.add(classification)
    creator.build()

    xml = creator.to_string()
    assert "<SequenceProduct ID=\"PSEQ200\"" in xml
    assert "<CurrentTasks><Task STEPWorkflowID=\"WF1\" StateID=\"S1\" AssigneeID=\"U1\" AssignedToGroup=\"True\" EntryTime=\"2026-01-01T00:00:00Z\"" in xml
    assert "<Tables><Table ID=\"T1\"" in xml
    assert "<Asset ID=\"A900\" UserTypeID=\"UT_ASSET\"" in xml


def test_entity_helpers_accept_prebuilt_objects():
    creator = Creator("Context2", "Main")
    entity = Entity({"ID": "E200", "UserTypeID": "UT_ENTITY"})

    entity.add_current_task(task_object=Task({
        "STEPWorkflowID": "WF2",
        "StateID": "S2",
        "AssigneeID": "U2",
        "AssignedToGroup": False,
        "EntryTime": "2026-02-02T00:00:00Z",
    }))
    entity.add_term(terms_object=Terms({"Term": [Term({"TermsListID": "TL1", "MinimumQuantity": "1", "value": "Net 30"})]}))

    creator.add(entity)
    creator.build()

    xml = creator.to_string()
    assert "<CurrentTasks><Task STEPWorkflowID=\"WF2\" StateID=\"S2\" AssigneeID=\"U2\" AssignedToGroup=\"False\" EntryTime=\"2026-02-02T00:00:00Z\"" in xml
    assert "<Terms><Term TermsListID=\"TL1\" MinimumQuantity=\"1\">Net 30</Term></Terms>" in xml
