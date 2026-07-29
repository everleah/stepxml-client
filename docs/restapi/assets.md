# Assets

> **Operation group:** `client.assets` | **Source:** `stepxmlclient/rest_client/operations/assets.py`

Full CRUD, search, binary content upload/download, approval, values, and lifecycle for STEP assets.

## Operations

### CRUD

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_asset` | `(asset_id, key_id=None) -> AssetResponse` | Retrieve by ID or key |
| `search_assets` | `(condition: dict) -> AssetListResponse` | Search via `queryAssets` |
| `create_asset` | `(asset_data: AssetCreateRequest) -> AssetResponse` | Create with auto-generated ID |
| `replace_asset` | `(asset_id, asset_data, key_id=None, allow_overwrite=False) -> AssetResponse` | Full replace (PUT) |
| `update_asset` | `(asset_id, updates: AssetUpdateRequest, key_id=None) -> AssetResponse` | Partial update (PATCH) |
| `delete_asset` | `(asset_id, key_id=None) -> bool` | Delete |

### Binary Content

| Method | Signature | Description |
|--------|-----------|-------------|
| `upload_asset_content` | `(asset_id, file_path, mime_type=None, key_id=None) -> AssetResponse` | Upload binary content |
| `download_asset_content` | `(asset_id, output_path=None, key_id=None, conversion_configuration_id=None) -> AssetDownloadResponse` | Download binary content |
| `get_asset_content_url` | `(asset_id) -> str` | Construct content URL |

### Values

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_asset_value` | `(asset_id, attribute_id, key_id=None) -> dict` | Get attribute value |
| `replace_asset_value` | `(asset_id, attribute_id, value, key_id=None) -> dict` | Replace attribute value |
| `delete_asset_value` | `(asset_id, attribute_id, key_id=None) -> bool` | Delete attribute value |

### Approval & Lifecycle

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_asset_approval_status` | `(asset_id, key_id=None) -> dict` | Get approval status |
| `approve_asset` | `(asset_id, key_id=None) -> dict` | Approve |
| `approve_asset_deletion` | `(asset_id, key_id=None) -> dict` | Approve deletion |
| `purge_asset` | `(asset_id, key_id=None) -> dict` | Purge from recycle bin |
| `get_asset_incoming_references` | `(asset_id, key_id=None) -> dict` | Incoming references |


## Examples

### Upload a file to an asset
```python
client.assets.upload_asset_content("A001", "product_image.jpg")
```

### Download asset content
```python
result = client.assets.download_asset_content("A001", output_path="./downloaded.jpg")
print(f"Downloaded {result.filename} ({result.size} bytes)")
```

### Create asset with classification
```python
from stepxmlclient.rest_client.models.asset import AssetCreateRequest

created = client.assets.create_asset(AssetCreateRequest(
    objectType="ProductImage",
    classifications=["ProductImageRoot"],
    name="hero-shot.jpg"
))
```


