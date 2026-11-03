"""Phase 5 - Read-only attribute, LOV and type-definition operations."""

import unittest
from unittest.mock import Mock

from pydantic import ValidationError as ModelValidationError

from stepxmlclient.rest_client import exceptions as exc
from stepxmlclient.rest_client.models.attribute import AttributeResponse, ListOfValueResponse
from stepxmlclient.rest_client.operations.attributes import AttributeOperations
from tests.test_rest_response_handling import json_response


class TestAttributeModels(unittest.TestCase):
    def test_spec_attribute_fields_without_legacy_type(self):
        payload = {
            "id": "Color", "name": "Color", "validator": {"name": "text"},
            "multivalued": True, "calculated": False, "specification": True,
            "dataTypeGroups": ["Technical"], "listOfValues": "Colors",
            "units": [], "defaultUnit": None, "values": {},
            "validForObjectTypes": ["SalesItem"],
        }
        attribute = AttributeResponse.model_validate(payload)
        for key, value in payload.items():
            self.assertEqual(getattr(attribute, key), value)
        self.assertIsNone(attribute.type)

    def test_legacy_attribute_fields_remain_accepted(self):
        attribute = AttributeResponse.model_validate({
            "id": "Color", "name": "Color", "type": "Text",
            "lovId": "Colors", "multiValued": True,
        })
        self.assertEqual(attribute.type, "Text")
        self.assertEqual(attribute.lovId, "Colors")
        self.assertTrue(attribute.multiValued)

    def test_attribute_validator_shape_is_checked(self):
        with self.assertRaises(ModelValidationError):
            AttributeResponse.model_validate({"id": "Color", "validator": "text"})

    def test_lov_definition_contains_metadata_not_entries(self):
        payload = {
            "id": "Colors", "name": "Colors", "extendable": False, "usesValueIds": True,
            "validator": {"name": "text"}, "dataTypeGroups": ["Technical"],
            "values": {"Description": {"value": {"value": "Available colors"}}},
        }
        lov = ListOfValueResponse.model_validate(payload)
        for key, value in payload.items():
            self.assertEqual(getattr(lov, key), value)

    def test_legacy_lov_entry_lists_remain_accepted(self):
        lov = ListOfValueResponse.model_validate({
            "id": "Colors", "items": [{"id": "RED", "name": "Red"}],
            "values": [{"id": "BLUE", "name": "Blue"}],
        })
        self.assertIsNotNone(lov.items)
        assert lov.items is not None
        self.assertEqual(lov.items[0].id, "RED")
        self.assertIsInstance(lov.values, list)
        assert isinstance(lov.values, list)
        self.assertEqual(lov.values[0].id, "BLUE")


class TestAttributeOperations(unittest.TestCase):
    def setUp(self):
        self.client = Mock(spec_set=[
            "getAttribute", "getListOfValues", "getListOfValuesEntries",
            "getDataContainerType", "getDataTypeGroup", "getObjectType",
            "getObjectTypeChildren", "getReferenceType", "getUnit", "getUniqueKey",
        ])
        self.operations = AttributeOperations(self.client, context="C", workspace="Main")

    def test_get_attribute_success(self):
        self.client.getAttribute.return_value = json_response({
            "id": "Color", "name": "Color", "validator": {"name": "text"},
        })
        result = self.operations.get_attribute("Color")
        self.assertIsInstance(result, AttributeResponse)
        self.assertEqual(result.validator, {"name": "text"})
        self.client.getAttribute.assert_called_once_with(id="Color", context="C", workspace="Main")

    def test_get_attribute_not_found(self):
        self.client.getAttribute.return_value = json_response({"message": "No attribute"}, status=404)
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_attribute("Missing")

    def test_required_identifiers_are_validated(self):
        for method in (self.operations.get_attribute, self.operations.get_list_of_values,
                       self.operations.get_list_of_values_entries):
            with self.subTest(method=method.__name__), self.assertRaises(exc.ValidationError):
                method(None)
        self.assertEqual(self.client.mock_calls, [])

    def test_get_list_of_values_success(self):
        self.client.getListOfValues.return_value = json_response({
            "id": "Colors", "validator": {"name": "text"}, "values": {},
        })
        result = self.operations.get_list_of_values("Colors")
        self.assertIsInstance(result, ListOfValueResponse)
        self.assertEqual(result.values, {})
        self.client.getListOfValues.assert_called_once_with(id="Colors", context="C", workspace="Main")

    def test_get_list_of_values_not_found(self):
        self.client.getListOfValues.return_value = json_response({"message": "No LOV"}, status=404)
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_list_of_values("Missing")

    def test_lov_entries_are_retrieved_separately(self):
        entries = [{"valueId": "RED", "value": "Red"}, {"value": "Blue", "unit": "unit"}]
        self.client.getListOfValuesEntries.return_value = json_response(entries)
        self.assertEqual(self.operations.get_list_of_values_entries("Colors"), entries)
        self.client.getListOfValuesEntries.assert_called_once_with(
            id="Colors", context="C", workspace="Main")

    def test_type_definitions(self):
        for method, operation in (
            ("get_data_container_type", "getDataContainerType"),
            ("get_data_type_group", "getDataTypeGroup"),
            ("get_object_type", "getObjectType"),
            ("get_reference_type", "getReferenceType"),
            ("get_unit", "getUnit"),
            ("get_unique_key", "getUniqueKey"),
        ):
            with self.subTest(method=method):
                getattr(self.client, operation).return_value = {"id": "T"}
                self.assertEqual(getattr(self.operations, method)("T"), {"id": "T"})
                getattr(self.client, operation).assert_called_once_with(
                    id="T", context="C", workspace="Main")

    def test_object_type_children(self):
        self.client.getObjectTypeChildren.return_value = json_response(["Child"])
        self.assertEqual(self.operations.get_object_type_children("Root"), ["Child"])

    def test_no_unsupported_attribute_write_or_search_wrappers(self):
        for name in ("create_attribute", "update_attribute", "delete_attribute", "search_attributes"):
            with self.subTest(method=name):
                self.assertFalse(hasattr(self.operations, name))


if __name__ == "__main__":
    unittest.main()
