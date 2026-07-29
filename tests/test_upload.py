"""
Test script for asset binary upload functionality.

This script demonstrates how to upload binary files to STEP assets.
"""

from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.upload import AssetUploader

# Configure connection
authorisation = BasicAuthorisation('CLHA', 'CLHA')
rest_client = StiboStepRestClient(
    location_base='https://hoerl-sb01.mdm.stibosystems.com/restapiv2',
    authorisation=authorisation, 
    cache_openapi=True, 
    nocert=True
)

# Create uploader
uploader = AssetUploader(rest_client)

print("=== Asset Upload Test ===\n")

# Example 1: Upload a local file
try:
    print("Example 1: Upload local file")
    print("-" * 40)
    result = uploader.upload_file(
        file_path='path/to/your/image.jpg',  # Replace with actual file path
        asset_id='YOUR_ASSET_ID',            # Replace with actual asset ID
        filename='custom_name.jpg',          # Optional: custom filename
        context_id='Context1',               # Your STEP context
        workspace_id=None                    # Optional: workspace
    )
    print(f"✓ Upload successful!")
    print(f"  Asset ID: {result['asset_id']}")
    print(f"  Filename: {result['filename']}")
    print(f"  Status: {result['status_code']}")
    print()
except FileNotFoundError as e:
    print(f"✗ File not found: {e}")
    print()
except Exception as e:
    print(f"✗ Upload failed: {e}")
    print()

# Example 2: Upload from URL
try:
    print("Example 2: Upload from URL")
    print("-" * 40)
    result = uploader.upload_file(
        file_path='https://example.com/image.jpg',  # URL to download from
        asset_id='YOUR_ASSET_ID',                   # Replace with actual asset ID
        context_id='Context1'
    )
    print(f"✓ Upload successful!")
    print(f"  Asset ID: {result['asset_id']}")
    print(f"  Filename: {result['filename']}")
    print(f"  Status: {result['status_code']}")
    print()
except Exception as e:
    print(f"✗ Upload failed: {e}")
    print()

# Example 3: Download asset content
try:
    print("Example 3: Download asset content")
    print("-" * 40)
    content = uploader.get_content(
        asset_id='YOUR_ASSET_ID',  # Replace with actual asset ID
        context_id='Context1'
    )
    print(f"✓ Download successful!")
    print(f"  Content size: {len(content)} bytes")
    print()
    
    # Save to file
    with open('downloaded_asset.bin', 'wb') as f:
        f.write(content)
    print(f"✓ Saved to: downloaded_asset.bin")
    print()
except Exception as e:
    print(f"✗ Download failed: {e}")
    print()

print("=== Test Complete ===")
