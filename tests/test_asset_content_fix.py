#!/usr/bin/env python3
"""Test that download and upload asset content methods work with correct operation names."""

import sys
import io
from unittest.mock import MagicMock
from stepxmlclient.rest_client.operations.assets import AssetOperations

print("Test 1: Testing download_asset_content() with correct getAssetContent call...")

# Create a mock client
mock_client = MagicMock()
mock_client.server = MagicMock()
mock_client.server.url = "https://hoerl-sb01.mdm.stibosystems.com"

# Mock the getAssetContent operation to return binary content
mock_response = MagicMock()
mock_response.content = b"binary asset content here"
mock_response.filename = "test_asset.bin"
mock_response.size = 24
mock_response.mime_type = "application/octet-stream"
mock_response.content_url = None
mock_response.expires_at = None
mock_client.getAssetContent.return_value = mock_response

# Create AssetOperations instance
asset_ops = AssetOperations(mock_client)

try:
    # Call download method
    result = asset_ops.download_asset_content("22215")
    
    # Verify that getAssetContent was called with id= parameter (not assetId=)
    mock_client.getAssetContent.assert_called_once()
    call_kwargs = mock_client.getAssetContent.call_args.kwargs
    
    if 'id' in call_kwargs and call_kwargs['id'] == "22215":
        print("[PASS] download_asset_content() correctly calls getAssetContent(id=...)")
        print(f"  Called with: {call_kwargs}")
    else:
        print("[FAIL] download_asset_content() not calling with correct parameter name")
        print(f"  Expected: id='22215'")
        print(f"  Got: {call_kwargs}")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Exception in download_asset_content(): {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTest 2: Testing upload_asset_content() with correct replaceAssetContent call...")

# Reset mock
mock_client.reset_mock()
mock_client.server = MagicMock()
mock_client.server.url = "https://hoerl-sb01.mdm.stibosystems.com"
mock_upload_response = MagicMock()
mock_client.replaceAssetContent.return_value = mock_upload_response

# Create a temporary test file
import tempfile
import os
with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
    test_file = f.name
    f.write(b"fake image data")

try:
    # Call upload method
    result = asset_ops.upload_asset_content("22215", test_file)
    
    # Verify that replaceAssetContent was called with id= parameter (not assetId=)
    mock_client.replaceAssetContent.assert_called_once()
    call_kwargs = mock_client.replaceAssetContent.call_args.kwargs
    
    if 'id' in call_kwargs and call_kwargs['id'] == "22215":
        print("[PASS] upload_asset_content() correctly calls replaceAssetContent(id=...)")
        print(f"  Called with: id='{call_kwargs['id']}', fileName='{call_kwargs.get('fileName')}'")
        if call_kwargs.get('fileName') == os.path.basename(test_file):
            print("[PASS] fileName parameter correctly extracted from file path")
        else:
            print(f"[FAIL] fileName mismatch: expected '{os.path.basename(test_file)}', got '{call_kwargs.get('fileName')}'")
            sys.exit(1)
    else:
        print("[FAIL] upload_asset_content() not calling with correct parameter name")
        print(f"  Expected: id='22215'")
        print(f"  Got: {call_kwargs}")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Exception in upload_asset_content(): {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)

print("\nTest 3: Verify operation names match OpenAPI spec...")
from pathlib import Path
import json

spec_file = Path(__file__).parent / 'stepxmlclient' / 'openapi.json'
try:
    with open(spec_file) as f:
        spec = json.load(f)
    
    # The content endpoint is /assets/{id}/content, NOT /assets/{id}
    get_op_id = spec['paths']['/assets/{id}/content']['get']['operationId']
    put_op_id = spec['paths']['/assets/{id}/content']['put']['operationId']
    
    if get_op_id == 'getAssetContent':
        print(f"[PASS] GET /assets/{{id}}/content has operationId: {get_op_id}")
    else:
        print(f"[FAIL] GET operation is {get_op_id}, expected getAssetContent")
        sys.exit(1)
    
    if put_op_id == 'replaceAssetContent':
        print(f"[PASS] PUT /assets/{{id}}/content has operationId: {put_op_id}")
    else:
        print(f"[FAIL] PUT operation is {put_op_id}, expected replaceAssetContent")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Error reading OpenAPI spec: {e}")
    sys.exit(1)

print("\n[SUCCESS] All tests passed! Asset download and upload operations are fixed.")
