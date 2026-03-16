#!/usr/bin/env python3
"""Test that get_asset_content_url() works after the fix."""

import sys
from unittest.mock import MagicMock, patch

# Test 1: Direct test with mocked client
print("Test 1: Testing get_asset_content_url() with mocked client...")

from stepxmlclient.rest_client.operations.assets import AssetOperations

# Create a mock client with server URL
mock_client = MagicMock()
mock_client.server = MagicMock()
mock_client.server.url = "https://hoerl-sb01.mdm.stibosystems.com"

# Create AssetOperations instance
asset_ops = AssetOperations(mock_client)

# Test the method
asset_id = "22215"
try:
    url = asset_ops.get_asset_content_url(asset_id)
    expected = f"https://hoerl-sb01.mdm.stibosystems.com/assets/{asset_id}/content"
    
    if url == expected:
        print(f"[PASS] Correct URL generated")
        print(f"  Generated URL: {url}")
    else:
        print(f"[FAIL] URL mismatch")
        print(f"  Expected: {expected}")
        print(f"  Got:      {url}")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Exception raised: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTest 2: Verify openapi.json is bundled...")
from pathlib import Path
bundle_file = Path(__file__).parent / 'stepxmlclient' / 'openapi.json'
if bundle_file.exists():
    print(f"[PASS] Bundled openapi.json found at {bundle_file}")
    file_size = bundle_file.stat().st_size
    print(f"  File size: {file_size:,} bytes")
else:
    print(f"[FAIL] Bundled openapi.json not found at {bundle_file}")
    sys.exit(1)

print("\n[SUCCESS] All tests passed!")
