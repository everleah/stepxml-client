"""Classification operations for STEP REST API v2."""

import logging
from typing import Any, Optional

from ..base import BaseOperation, handle_rest_errors
from ..exceptions import NotFoundError, ValidationError
from ..models.classification import ClassificationListResponse, ClassificationResponse


class ClassificationOperations(BaseOperation):
    """Operations for STEP Classifications."""
    
    def __init__(self, client, logger: Optional[logging.Logger] = None,
                 context: str | None = None, workspace: str | None = None):
        """Initialize classification operations.
        
        Args:
            client: The REST API client
            logger: Optional logger instance
            context: STEP context ID for all API calls
            workspace: STEP workspace ID (defaults to "Main" server-side)
        """
        super().__init__(client, operation_name="ClassificationOperations", logger=logger,
                         context=context, workspace=workspace)
    
    @handle_rest_errors
    def get_classification(self, classification_id: str,
                          key_id: str | None = None,
                          include_inherited_data: bool = False) -> ClassificationResponse:
        """Get a single classification by ID.
        
        Args:
            classification_id: The classification ID (or alternate key value if key_id is set)
            key_id: Alternate key ID to use for lookup (optional)
            include_inherited_data: Whether to include inherited attribute values (default: False)
            
        Returns:
            ClassificationResponse with classification data
            
        Raises:
            ValidationError: If classification_id is missing
            NotFoundError: If classification not found
            RestApiError: For other API errors
        """
        self._validate_required_params(
            {"classification_id": classification_id},
            ["classification_id"]
        )
        
        query_params: dict[str, Any] = self._build_context_params()
        if key_id:
            query_params["keyId"] = key_id
        if include_inherited_data:
            query_params["includeInheritedData"] = include_inherited_data
        self._log_operation("getClassification", {"classification_id": classification_id})
        
        try:
            response = self.client.getClassification(id=classification_id, **query_params)
        except Exception as e:
            if "404" in str(e):
                raise NotFoundError(classification_id, "Classification")
            raise
        
        if isinstance(response, dict):
            return ClassificationResponse(**response)
        return response
    
    @handle_rest_errors
    def search_classifications(self, condition: dict) -> ClassificationListResponse:
        """Search classifications using a STEP condition query.
        
        Args:
            condition: A STEP condition object defining the search criteria.
                       Supported conditionTypes: 'and', 'or', 'id', 'name',
                       'textvalue', 'numericvalue', 'objecttype', 'simplebelow',
                       'lovvalue', 'hasreferenceto', 'hasdatacontainerobject'.
            
        Returns:
            ClassificationListResponse with matching classifications
            
        Raises:
            ValidationError: If condition is invalid
            RestApiError: For API errors
        """
        self._validate_required_params({"condition": condition}, ["condition"])
        body = {"condition": condition}
        self._log_operation("createClassificationSearch", {"condition": condition})
        
        response = self.client.createClassificationSearch(json=body, **self._build_context_params())
        
        if isinstance(response, dict):
            return ClassificationListResponse(**response)
        return response
    
    def search_by_type(self, classification_type: str) -> ClassificationListResponse:
        """Search classifications by object type (convenience method).
        
        Args:
            classification_type: The object type ID to filter by
            
        Returns:
            ClassificationListResponse filtered by type
        """
        return self.search_classifications(
            condition={"conditionType": "objecttype", "objectType": classification_type}
        )


    @handle_rest_errors
    def get_classification_approval_status(self, classification_id: str,
                                           key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"classification_id": classification_id}, ["classification_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getClassificationApprovalStatus", {"id": classification_id})
        try:
            r = self.client.getClassificationApprovalStatus(id=classification_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_classification(self, classification_id: str,
                               key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"classification_id": classification_id}, ["classification_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveClassification", {"id": classification_id})
        try:
            r = self.client.approveClassification(id=classification_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def approve_classification_deletion(self, classification_id: str,
                                        key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"classification_id": classification_id}, ["classification_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("approveClassificationDeletion", {"id": classification_id})
        try:
            r = self.client.approveClassificationDeletion(id=classification_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def purge_classification(self, classification_id: str,
                             key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"classification_id": classification_id}, ["classification_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("purgeClassification", {"id": classification_id})
        try:
            r = self.client.purgeClassification(id=classification_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_classification_assets(self, classification_id: str,
                                  key_id: str | None = None) -> list[dict[str, Any]]:
        self._validate_required_params({"classification_id": classification_id}, ["classification_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getClassificationAssets", {"id": classification_id})
        try:
            r = self.client.getClassificationAssets(id=classification_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, list) else []

    @handle_rest_errors
    def get_classification_incoming_references(self, classification_id: str,
                                               key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params({"classification_id": classification_id}, ["classification_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getClassificationIncomingReferences", {"id": classification_id})
        try:
            r = self.client.getClassificationIncomingReferences(id=classification_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def get_classification_value(self, classification_id: str, attribute_id: str,
                                 key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params(
            {"classification_id": classification_id, "attribute_id": attribute_id},
            ["classification_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("getClassificationValueByAttributeId",
                           {"id": classification_id, "attributeId": attribute_id})
        try:
            r = self.client.getClassificationValueByAttributeId(
                id=classification_id, attributeId=attribute_id, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def replace_classification_value(self, classification_id: str, attribute_id: str,
                                     value: dict[str, Any],
                                     key_id: str | None = None) -> dict[str, Any]:
        self._validate_required_params(
            {"classification_id": classification_id, "attribute_id": attribute_id},
            ["classification_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("replaceClassificationValueByAttributeId",
                           {"id": classification_id, "attributeId": attribute_id})
        try:
            r = self.client.replaceClassificationValueByAttributeId(
                id=classification_id, attributeId=attribute_id, json=value, **qp)
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            if "400" in str(e): raise ValidationError(str(e))
            raise
        return r if isinstance(r, dict) else r

    @handle_rest_errors
    def delete_classification_value(self, classification_id: str, attribute_id: str,
                                    key_id: str | None = None) -> bool:
        self._validate_required_params(
            {"classification_id": classification_id, "attribute_id": attribute_id},
            ["classification_id", "attribute_id"])
        qp = self._build_context_params()
        if key_id: qp["keyId"] = key_id
        self._log_operation("deleteClassificationValueByAttributeId",
                           {"id": classification_id, "attributeId": attribute_id})
        try:
            self.client.deleteClassificationValueByAttributeId(
                id=classification_id, attributeId=attribute_id, **qp)
            return True
        except Exception as e:
            if "404" in str(e): raise NotFoundError(classification_id, "Classification")
            raise
