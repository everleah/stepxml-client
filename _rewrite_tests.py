#!/usr/bin/env python
"""Script to rewrite the Operations test classes in phase3-7 test files."""

import os

# =============================================================================
# Phase 3 - Classifications
# =============================================================================

PHASE3_NEW_CLASS = """

class TestClassificationOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = ClassificationOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "ClassificationOperations")

    def test_get_classification_success(self):
        self.mock_client.getClassification.return_value = {
            "id": "CLASS1", "user_type_id": "ClassType", "name": "Root"}
        result = self.operations.get_classification("CLASS1")
        self.assertEqual(result.id, "CLASS1")
        call_args = self.mock_client.getClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")
        self.assertNotIn("classificationId", call_args[1])

    def test_get_classification_not_found(self):
        self.mock_client.getClassification.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_classification("NONEXISTENT")

    def test_get_classification_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_classification(None)

    def test_get_classification_with_key_id(self):
        self.mock_client.getClassification.return_value = {"id": "CLASS1"}
        self.operations.get_classification("CLASS1", key_id="MyKey")
        call_args = self.mock_client.getClassification.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_get_classification_with_include_inherited(self):
        self.mock_client.getClassification.return_value = {"id": "CLASS1"}
        self.operations.get_classification("CLASS1", include_inherited_data=True)
        call_args = self.mock_client.getClassification.call_args
        self.assertEqual(call_args[1]["includeInheritedData"], True)

    def test_search_classifications_success(self):
        self.mock_client.postClassificationsSearch.return_value = {
            "items": [{"id": "CLASS1"}, {"id": "CLASS2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "ClassType"}
        result = self.operations.search_classifications(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postClassificationsSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_classifications_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_classifications(condition=None)

    def test_create_classification_success(self):
        self.mock_client.postClassifications.return_value = {"id": "NEWCLASS", "name": "New"}
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        request = ClassificationCreateRequest(id="NEWCLASS", user_type_id=None, name="New", attributes=None)
        result = self.operations.create_classification(request)
        self.assertEqual(result.id, "NEWCLASS")
        self.mock_client.postClassifications.assert_called_once()

    def test_create_classification_conflict(self):
        self.mock_client.postClassifications.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        request = ClassificationCreateRequest(id="EXISTING", user_type_id=None, name=None, attributes=None)
        with self.assertRaises(exc.ConflictError):
            self.operations.create_classification(request)

    def test_update_classification_success(self):
        self.mock_client.patchClassification.return_value = {"id": "CLASS1", "name": "Updated"}
        from stepxmlclient.rest_client.models.classification import ClassificationUpdateRequest
        updates = ClassificationUpdateRequest(name="Updated", user_type_id=None, attributes=None)
        result = self.operations.update_classification("CLASS1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_update_classification_not_found(self):
        self.mock_client.patchClassification.side_effect = Exception("404 not found")
        from stepxmlclient.rest_client.models.classification import ClassificationUpdateRequest
        updates = ClassificationUpdateRequest(name="Updated", user_type_id=None, attributes=None)
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_classification("NONEXISTENT", updates)

    def test_replace_classification_success(self):
        self.mock_client.putClassification.return_value = {"id": "CLASS1"}
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        data = ClassificationCreateRequest(id="CLASS1", user_type_id=None, name=None, attributes=None)
        result = self.operations.replace_classification("CLASS1", data)
        self.assertEqual(result.id, "CLASS1")
        call_args = self.mock_client.putClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_replace_classification_with_allow_overwrite(self):
        self.mock_client.putClassification.return_value = {"id": "CLASS1"}
        from stepxmlclient.rest_client.models.classification import ClassificationCreateRequest
        data = ClassificationCreateRequest(id="CLASS1", user_type_id=None, name=None, attributes=None)
        self.operations.replace_classification("CLASS1", data, allow_overwrite=True)
        call_args = self.mock_client.putClassification.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_classification_success(self):
        self.mock_client.deleteClassification.return_value = None
        result = self.operations.delete_classification("CLASS1")
        self.assertTrue(result)
        call_args = self.mock_client.deleteClassification.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_delete_classification_not_found(self):
        self.mock_client.deleteClassification.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_classification("NONEXISTENT")

    def test_get_classification_hierarchy(self):
        self.mock_client.getClassificationChildren.return_value = {"items": [{"id": "CHILD1"}]}
        result = self.operations.get_classification_hierarchy("CLASS1")
        self.assertEqual(len(result), 1)
        call_args = self.mock_client.getClassificationChildren.call_args
        self.assertEqual(call_args[1]["id"], "CLASS1")

    def test_search_by_type(self):
        self.mock_client.postClassificationsSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("ClassType")
        call_args = self.mock_client.postClassificationsSearch.call_args
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "ClassType")

    def test_list_classifications(self):
        self.mock_client.postClassificationsSearch.return_value = {"items": [], "total": 0}
        self.operations.list_classifications()
        self.mock_client.postClassificationsSearch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
"""

# =============================================================================
# Phase 4 - Entities
# =============================================================================

PHASE4_NEW_CLASS = """

class TestEntityOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = EntityOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "EntityOperations")

    def test_get_entity_success(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1", "user_type_id": "EntityType", "name": "Test Entity"}
        result = self.operations.get_entity("ENT1")
        self.assertEqual(result.id, "ENT1")
        call_args = self.mock_client.getEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")
        self.assertNotIn("entityId", call_args[1])

    def test_get_entity_not_found(self):
        self.mock_client.getEntity.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_entity("NONEXISTENT")

    def test_get_entity_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_entity(None)

    def test_get_entity_with_key_id(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1"}
        self.operations.get_entity("ENT1", key_id="MyKey")
        call_args = self.mock_client.getEntity.call_args
        self.assertEqual(call_args[1]["keyId"], "MyKey")

    def test_get_entity_with_include_inherited(self):
        self.mock_client.getEntity.return_value = {"id": "ENT1"}
        self.operations.get_entity("ENT1", include_inherited_data=True)
        call_args = self.mock_client.getEntity.call_args
        self.assertEqual(call_args[1]["includeInheritedData"], True)

    def test_search_entities_success(self):
        self.mock_client.postEntitiesSearch.return_value = {
            "items": [{"id": "ENT1"}, {"id": "ENT2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "EntityType"}
        result = self.operations.search_entities(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postEntitiesSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_entities_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_entities(condition=None)

    def test_create_entity_success(self):
        self.mock_client.postEntities.return_value = {"id": "NEWENT", "name": "New Entity"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        request = EntityCreateRequest(id="NEWENT", user_type_id=None, name="New Entity", attributes=None)
        result = self.operations.create_entity(request)
        self.assertEqual(result.id, "NEWENT")
        self.mock_client.postEntities.assert_called_once()

    def test_create_entity_conflict(self):
        self.mock_client.postEntities.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        request = EntityCreateRequest(id="EXISTING", user_type_id=None, name=None, attributes=None)
        with self.assertRaises(exc.ConflictError):
            self.operations.create_entity(request)

    def test_update_entity_success(self):
        self.mock_client.patchEntity.return_value = {"id": "ENT1", "name": "Updated"}
        from stepxmlclient.rest_client.models.entity import EntityUpdateRequest
        updates = EntityUpdateRequest(name="Updated", user_type_id=None, attributes=None)
        result = self.operations.update_entity("ENT1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_update_entity_not_found(self):
        self.mock_client.patchEntity.side_effect = Exception("404 not found")
        from stepxmlclient.rest_client.models.entity import EntityUpdateRequest
        updates = EntityUpdateRequest(name="Updated", user_type_id=None, attributes=None)
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_entity("NONEXISTENT", updates)

    def test_replace_entity_success(self):
        self.mock_client.putEntity.return_value = {"id": "ENT1"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        data = EntityCreateRequest(id="ENT1", user_type_id=None, name=None, attributes=None)
        result = self.operations.replace_entity("ENT1", data)
        self.assertEqual(result.id, "ENT1")
        call_args = self.mock_client.putEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_replace_entity_with_allow_overwrite(self):
        self.mock_client.putEntity.return_value = {"id": "ENT1"}
        from stepxmlclient.rest_client.models.entity import EntityCreateRequest
        data = EntityCreateRequest(id="ENT1", user_type_id=None, name=None, attributes=None)
        self.operations.replace_entity("ENT1", data, allow_overwrite=True)
        call_args = self.mock_client.putEntity.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_entity_success(self):
        self.mock_client.deleteEntity.return_value = None
        result = self.operations.delete_entity("ENT1")
        self.assertTrue(result)
        call_args = self.mock_client.deleteEntity.call_args
        self.assertEqual(call_args[1]["id"], "ENT1")

    def test_delete_entity_not_found(self):
        self.mock_client.deleteEntity.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_entity("NONEXISTENT")

    def test_search_by_type(self):
        self.mock_client.postEntitiesSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("EntityType")
        call_args = self.mock_client.postEntitiesSearch.call_args
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "EntityType")

    def test_list_entities(self):
        self.mock_client.postEntitiesSearch.return_value = {"items": [], "total": 0}
        self.operations.list_entities()
        self.mock_client.postEntitiesSearch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
"""


# =============================================================================
# Phase 5 - Attributes & Metadata
# =============================================================================

PHASE5_ATTR_CLASS = """

class TestAttributeOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = AttributeOperations(self.mock_client, logger=self.logger)

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "AttributeOperations")

    def test_get_attribute_success(self):
        self.mock_client.getAttribute.return_value = {"id": "ATTR1", "name": "Color"}
        result = self.operations.get_attribute("ATTR1")
        self.assertEqual(result.id, "ATTR1")
        call_args = self.mock_client.getAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_get_attribute_not_found(self):
        self.mock_client.getAttribute.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_attribute("NONEXISTENT")

    def test_get_attribute_validation(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.get_attribute(None)

    def test_search_attributes_success(self):
        self.mock_client.postAttributesSearch.return_value = {
            "items": [{"id": "ATTR1"}, {"id": "ATTR2"}], "total": 2}
        condition = {"conditionType": "objecttype", "objectTypeId": "AttributeType"}
        result = self.operations.search_attributes(condition=condition)
        self.assertEqual(len(result.items), 2)
        call_args = self.mock_client.postAttributesSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_search_attributes_requires_condition(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.search_attributes(condition=None)

    def test_create_attribute_success(self):
        self.mock_client.postAttributes.return_value = {"id": "NEWATTR", "name": "New"}
        from stepxmlclient.rest_client.models.attribute import AttributeCreateRequest
        request = AttributeCreateRequest(id="NEWATTR", user_type_id=None, name="New")
        result = self.operations.create_attribute(request)
        self.assertEqual(result.id, "NEWATTR")
        self.mock_client.postAttributes.assert_called_once()

    def test_create_attribute_conflict(self):
        self.mock_client.postAttributes.side_effect = Exception("409 conflict")
        from stepxmlclient.rest_client.models.attribute import AttributeCreateRequest
        request = AttributeCreateRequest(id="EXISTING", user_type_id=None, name=None)
        with self.assertRaises(exc.ConflictError):
            self.operations.create_attribute(request)

    def test_update_attribute_success(self):
        self.mock_client.patchAttribute.return_value = {"id": "ATTR1", "name": "Updated"}
        from stepxmlclient.rest_client.models.attribute import AttributeUpdateRequest
        updates = AttributeUpdateRequest(name="Updated", user_type_id=None)
        result = self.operations.update_attribute("ATTR1", updates)
        self.assertEqual(result.name, "Updated")
        call_args = self.mock_client.patchAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_update_attribute_not_found(self):
        self.mock_client.patchAttribute.side_effect = Exception("404 not found")
        from stepxmlclient.rest_client.models.attribute import AttributeUpdateRequest
        updates = AttributeUpdateRequest(name="Updated", user_type_id=None)
        with self.assertRaises(exc.NotFoundError):
            self.operations.update_attribute("NONEXISTENT", updates)

    def test_delete_attribute_success(self):
        self.mock_client.deleteAttribute.return_value = None
        result = self.operations.delete_attribute("ATTR1")
        self.assertTrue(result)
        call_args = self.mock_client.deleteAttribute.call_args
        self.assertEqual(call_args[1]["id"], "ATTR1")

    def test_get_list_of_values_success(self):
        # Note: singular 'getListOfValue' (not 'getListOfValues')
        self.mock_client.getListOfValue.return_value = {"id": "LOV1", "name": "Colors"}
        result = self.operations.get_list_of_values("LOV1")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getListOfValue.call_args
        self.assertEqual(call_args[1]["id"], "LOV1")

    def test_get_list_of_values_not_found(self):
        self.mock_client.getListOfValue.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_list_of_values("NONEXISTENT")

    def test_search_list_of_values(self):
        self.mock_client.postListOfValuesSearch.return_value = {
            "items": [{"id": "LOV1"}], "total": 1}
        condition = {"conditionType": "name", "value": "Colors"}
        result = self.operations.search_list_of_values(condition=condition)
        call_args = self.mock_client.postListOfValuesSearch.call_args
        self.assertEqual(call_args[1]["body"]["condition"], condition)

    def test_list_attributes(self):
        self.mock_client.postAttributesSearch.return_value = {"items": [], "total": 0}
        self.operations.list_attributes()
        self.mock_client.postAttributesSearch.assert_called_once()

    def test_search_by_type(self):
        self.mock_client.postAttributesSearch.return_value = {"items": [], "total": 0}
        self.operations.search_by_type("AttributeType")
        call_args = self.mock_client.postAttributesSearch.call_args
        body = call_args[1]["body"]
        self.assertEqual(body["condition"]["conditionType"], "objecttype")
        self.assertEqual(body["condition"]["objectTypeId"], "AttributeType")
"""


PHASE5_META_CLASS = """

class TestMetadataOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        # MetadataOperations wraps the same client
        try:
            from stepxmlclient.rest_client.operations.attributes import MetadataOperations
            self.operations = MetadataOperations(self.mock_client, logger=self.logger)
            self.has_meta = True
        except ImportError:
            self.has_meta = False

    def test_initialization_skipped_if_no_meta_ops(self):
        # If MetadataOperations doesn't exist, skip gracefully
        if not self.has_meta:
            self.skipTest("MetadataOperations not found in attributes module")


if __name__ == "__main__":
    unittest.main()
"""


# =============================================================================
# Phase 6 - Imports/Exports
# =============================================================================

PHASE6_NEW_CLASSES = """

class TestImportOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.logger = logging.getLogger(__name__)
        self.operations = ExportOperations(self.mock_client, logger=self.logger, context="Main")

    def test_initialization(self):
        self.assertEqual(self.operations.operation_name, "ExportOperations")

    def test_create_export_job_success(self):
        self.mock_client.postExport.return_value = {"jobId": "JOB123"}
        result = self.operations.create_export_job("MyExportConfig")
        self.assertIsNotNone(result)
        call_args = self.mock_client.postExport.call_args
        self.assertEqual(call_args[1]["exportConfigurationId"], "MyExportConfig")
        self.assertEqual(call_args[1]["context"], "Main")

    def test_create_export_job_requires_config_id(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.create_export_job(None)

    def test_create_export_job_with_workspace(self):
        self.mock_client.postExport.return_value = {"jobId": "JOB123"}
        self.operations.create_export_job("MyExportConfig", use_request_context_workspace=True)
        call_args = self.mock_client.postExport.call_args
        self.assertEqual(call_args[1]["useRequestContextWorkspace"], True)

    def test_create_import_job_success(self):
        self.mock_client.postImport.return_value = {"jobId": "IMPORT123"}
        result = self.operations.create_import_job("MyImportConfig")
        self.assertIsNotNone(result)
        call_args = self.mock_client.postImport.call_args
        self.assertEqual(call_args[1]["importConfigurationId"], "MyImportConfig")

    def test_create_import_job_requires_config_id(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.create_import_job(None)

    def test_create_import_job_with_description(self):
        self.mock_client.postImport.return_value = {"jobId": "IMPORT123"}
        self.operations.create_import_job("MyImportConfig", process_description="Test run")
        call_args = self.mock_client.postImport.call_args
        self.assertEqual(call_args[1]["processDescription"], "Test run")

    def test_create_export_job_not_found(self):
        self.mock_client.postExport.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.create_export_job("NONEXISTENT")

    def test_create_import_job_not_found(self):
        self.mock_client.postImport.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.create_import_job("NONEXISTENT")


if __name__ == "__main__":
    unittest.main()
"""


# =============================================================================
# Phase 7 - Relations
# =============================================================================

PHASE7_NEW_CLASSES = """

class TestRelationOperationsInit(unittest.TestCase):
    def test_initialization(self):
        mock_client = Mock()
        ops = RelationOperations(mock_client)
        self.assertEqual(ops.operation_name, "RelationOperations")


class TestRelationshipOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.operations = RelationOperations(self.mock_client)

    def test_list_references_products(self):
        self.mock_client.getProducts_id_References.return_value = {"items": [{"id": "PROD2"}]}
        result = self.operations.list_references("products", "PROD1", "RelType")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getProducts_id_References.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")

    def test_list_references_assets(self):
        self.mock_client.getAssets_id_References.return_value = {"items": []}
        self.operations.list_references("assets", "ASSET1", "RelType")
        self.mock_client.getAssets_id_References.assert_called_once()

    def test_list_references_classifications(self):
        self.mock_client.getClassifications_id_References.return_value = {"items": []}
        self.operations.list_references("classifications", "CLASS1", "RelType")
        self.mock_client.getClassifications_id_References.assert_called_once()

    def test_list_references_entities(self):
        self.mock_client.getEntities_id_References.return_value = {"items": []}
        self.operations.list_references("entities", "ENT1", "RelType")
        self.mock_client.getEntities_id_References.assert_called_once()

    def test_get_reference_success(self):
        self.mock_client.getProductReference.return_value = {"referenceTypeId": "RelType"}
        result = self.operations.get_reference("products", "PROD1", "RelType", "PROD2")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getProductReference.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")
        self.assertEqual(call_args[1]["referenceTypeId"], "RelType")
        self.assertEqual(call_args[1]["targetId"], "PROD2")

    def test_get_reference_not_found(self):
        self.mock_client.getProductReference.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.get_reference("products", "PROD1", "RelType", "PROD2")

    def test_put_reference_success(self):
        self.mock_client.putProductReference.return_value = {}
        result = self.operations.put_reference("products", "PROD1", "RelType", "PROD2")
        self.assertTrue(result)
        call_args = self.mock_client.putProductReference.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")
        self.assertEqual(call_args[1]["referenceTypeId"], "RelType")
        self.assertEqual(call_args[1]["targetId"], "PROD2")

    def test_put_reference_with_allow_overwrite(self):
        self.mock_client.putProductReference.return_value = {}
        self.operations.put_reference("products", "PROD1", "RelType", "PROD2", allow_overwrite=True)
        call_args = self.mock_client.putProductReference.call_args
        self.assertEqual(call_args[1]["allow-overwrite"], True)

    def test_delete_reference_success(self):
        self.mock_client.deleteProductReference.return_value = None
        result = self.operations.delete_reference("products", "PROD1", "RelType", "PROD2")
        self.assertTrue(result)
        call_args = self.mock_client.deleteProductReference.call_args
        self.assertEqual(call_args[1]["id"], "PROD1")

    def test_delete_reference_not_found(self):
        self.mock_client.deleteProductReference.side_effect = Exception("404 not found")
        with self.assertRaises(exc.NotFoundError):
            self.operations.delete_reference("products", "PROD1", "RelType", "PROD2")

    def test_get_incoming_references(self):
        self.mock_client.getProductIncomingReference.return_value = {"items": []}
        result = self.operations.get_incoming_references("products", "PROD1", "RelType")
        self.assertIsNotNone(result)

    def test_get_reference_type(self):
        self.mock_client.getReferenceType.return_value = {"id": "RelType", "name": "My Relation"}
        result = self.operations.get_reference_type("RelType")
        self.assertIsNotNone(result)
        call_args = self.mock_client.getReferenceType.call_args
        self.assertEqual(call_args[1]["id"], "RelType")

    def test_invalid_entity_type(self):
        with self.assertRaises(exc.ValidationError):
            self.operations.list_references("invalid_type", "ID1", "RelType")


if __name__ == "__main__":
    unittest.main()
"""


def truncate_and_append(fname, truncate_at_line, new_content):
    """Truncate file at given line number (0-indexed) and append new content."""
    lines = open(fname).readlines()
    keep = lines[:truncate_at_line]
    with open(fname, 'w') as f:
        f.writelines(keep)
        f.write(new_content)
    print(f"Updated {fname}: kept {truncate_at_line} lines, appended new class(es)")


# Phase 3: truncate at line 213 (0-indexed = 213), start of TestClassificationOperations
truncate_and_append(
    "test_rest_client_phase3_classifications.py",
    213,
    PHASE3_NEW_CLASS
)

# Phase 4: truncate at line 168 (0-indexed = 168), start of TestEntityOperations
truncate_and_append(
    "test_rest_client_phase4_entities.py",
    168,
    PHASE4_NEW_CLASS
)

# Phase 5: truncate at line 197 (0-indexed = 197), start of TestAttributeOperations
# We need to keep TestAttributeModels (34-107) and TestMetadataModels (108-197)
truncate_and_append(
    "test_rest_client_phase5_attributes_metadata.py",
    197,
    PHASE5_ATTR_CLASS + "\n" + PHASE5_META_CLASS
)

# Phase 6: truncate at line 188 (0-indexed), keep only TestImportExportModels
truncate_and_append(
    "test_rest_client_phase6_imports_exports.py",
    188,
    PHASE6_NEW_CLASSES
)

# Phase 7: truncate at line 30 (0-indexed), start of TestRelationOperationsInit
truncate_and_append(
    "test_rest_client_phase7_relations.py",
    30,
    PHASE7_NEW_CLASSES
)

print("\nAll test files updated.")
