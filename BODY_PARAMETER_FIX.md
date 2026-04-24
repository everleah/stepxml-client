# STEP XML Client - Body Parameter Fix

## Problem Summary
When using the STEP XML Client in external projects, users experienced the following error:
```
Session.request() got an unexpected keyword argument 'body'
```

This error occurred when uploading binary data (STEP-XML or asset content) to STEP endpoints.

## Root Cause
The client library used the `requests_openapi` library to generate API operations. For binary uploads with `application/octet-stream` content type, the generated code tried to pass `body=` as a keyword argument to `requests.Session.request()`, which doesn't support this parameter.

The issue specifically affected endpoints that accept binary (octet-stream) request bodies:
- `PUT /assets/{id}/content` - Asset binary upload
- `POST /inbound-integration-endpoints/{id}/upload-and-invoke` - Inbound XML upload
- `POST /import/{importConfigurationId}` - Import binary data

These operations were calling:
```python
self.client.operationName(body=binary_data, ...)
```

But `requests.Session.request()` requires `data=` for binary content, not `body=`.

## Solution
Changed all binary upload operations to use direct HTTP calls via `requests.Session`:

### 1. Inbound XML Upload (`stepxmlclient/rest_client/operations/inbound.py`)
**Before:**
```python
response = self.client.postInboundIntegrationEndpointUploadAndInvoke(
    body=xml_data,
    **params
)
```

**After:**
```python
server_url = self.client.server.url
endpoint_path = f"/inbound-integration-endpoints/{endpoint_id}/upload-and-invoke"
url = f"{server_url}{endpoint_path}"

response = self.client.requestor.post(
    url,
    params=params,
    data=xml_data,
    headers={"Content-Type": "application/octet-stream"}
)
response.raise_for_status()
```

### 2. Asset Content Upload (`stepxmlclient/rest_client/operations/assets.py`)
**Before:**
```python
response = self.client.putAssetContent(
    body=f,
    **call_params
)
```

**After:**
```python
server_url = self.client.server.url
endpoint_path = f"/assets/{asset_id}/content"
url = f"{server_url}{endpoint_path}"

response = self.client.requestor.put(
    url,
    params=call_params,
    data=f.read(),
    headers={'Content-Type': mime_type}
)
response.raise_for_status()
```

### 3. Import Binary Upload (`stepxmlclient/rest_client/operations/exports.py`)
**Before:**
```python
response = self.client.postImport(body=binary_data, **params)
```

**After:**
```python
server_url = self.client.server.url
endpoint_path = f"/import/{import_configuration_id}"
url = f"{server_url}{endpoint_path}"

response = self.client.requestor.post(
    url,
    params=params,
    data=binary_data,
    headers={"Content-Type": "application/octet-stream"}
)
response.raise_for_status()
```

## Key Changes
1. Use `self.client.requestor` (the underlying `requests.Session`) for direct HTTP calls
2. Use `data=` parameter instead of `body=`
3. Explicitly set `Content-Type` header
4. Build URL from `self.client.server.url`
5. Handle response parsing directly instead of relying on `requests_openapi` generated operations

## Impact
- ✅ Fixes all binary upload operations
- ✅ Resolves the "unexpected keyword argument 'body'" error
- ✅ Works with both local files and binary data in memory
- ✅ All upload tests pass (8/8)
- ✅ JSON-based operations (products, assets, classifications, entities) remain unchanged and functional

## Testing
All upload_and_invoke tests pass:
- `test_upload_and_invoke_with_bytes` ✅
- `test_upload_and_invoke_with_string` ✅
- `test_upload_and_invoke_with_file_name` ✅
- `test_upload_and_invoke_missing_endpoint_id` ✅
- `test_upload_and_invoke_missing_xml_data` ✅
- `test_upload_and_invoke_endpoint_not_found` ✅
- `test_upload_and_invoke_endpoint_not_enabled` ✅
- `test_upload_and_invoke_no_rest_receiver` ✅

## Migration Notes for Users
If you were using these operations and had issues:

1. **Inbound Upload**: The method signature remains the same
   ```python
   result = client.inbound.upload_and_invoke(
       endpoint_id="my_endpoint",
       xml_data=xml_bytes
   )
   ```

2. **Asset Content Upload**: The method signature remains the same
   ```python
   result = client.assets.upload_asset_content(
       asset_id="A123",
       file_path="/path/to/file.jpg"
   )
   ```

3. **Import**: The method signature remains the same
   ```python
   result = client.exports.create_import_job(
       import_configuration_id="import_config",
       data=import_data
   )
   ```

**No API changes are required** - the fix is transparent to users. Just update your client library.

## Files Modified
- `stepxmlclient/rest_client/operations/inbound.py`
- `stepxmlclient/rest_client/operations/assets.py`
- `stepxmlclient/rest_client/operations/exports.py`
- `test_inbound_operations.py`

## Related Issues
- Affects external projects using the STEP XML Client
- Specifically impacts environments where binary uploads are used
- Error message: "Session.request() got an unexpected keyword argument 'body'"
