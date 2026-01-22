# STIBO STEP XML Creator - Send XML to Inbound Endpoint Example

This guide demonstrates how to create XML using the `stepxmlclient.Creator` and send it to STIBO STEP via the inbound endpoint using the `StiboStepRestClient`.

## Prerequisites
- `stepxmlclient` library installed
- Access to a STIBO STEP instance with REST API enabled
- Valid credentials (username and password)

---

## 1. Basic Example: Creating and Sending XML

### Step 1: Import Required Classes

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model.asset import Asset as StepAsset
from stepxmlclient.model.product import Product as StepProduct
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
```

### Step 2: Initialize the REST Client

```python
# Setup authentication
authorisation = BasicAuthorisation(user="your_username", pwd="your_password")

# Create REST client
client = StiboStepRestClient(
    location_base="https://your-step-instance.com/rest/v2",
    authorisation=authorisation
)
```

### Step 3: Create XML Using Creator

```python
# Initialize the Creator with workspace and context
creator = Creator(
    workspace_id="main",      # Your STEP workspace
    context_id="Context1"     # Your STEP context
)

# Create an Asset
step_asset = StepAsset(
    data={
        "ID": "asset_001",
        "Name": "Product Image",
        "Description": "High-quality product image"
    }
)
creator.add(step_asset)

# Create a Product
step_product = StepProduct(
    data={
        "ID": "product_001",
        "Name": "My Product",
        "UserTypeID": "Product",
        "Values": {
            "Description": "A sample product",
            "Price": "99.99"
        }
    }
)
creator.add(step_product)

# Build the XML
creator.build()
```

### Step 4: Get the XML

```python
# Build the XML
creator.build()

# Get XML as string
xml_string = creator.to_string()

# Get XML as bytes
xml_bytes = creator.to_bytes()
```

### Step 5: Send XML to STEP Inbound

```python
# Get the XML as bytes
xml_bytes = creator.to_bytes()

# Send using postInboundIntegrationEndpointUploadAndInvoke
# Parameters:
# - id: inbound endpoint ID (path)
# - context: context ID (REQUIRED query parameter)
# - workspace: workspace ID (optional query parameter, defaults to "Main")
# - fileName: optional file name for the upload
# - body: XML data (bytes or string)

response = client.client.postInboundIntegrationEndpointUploadAndInvoke(
    id="my_inbound_endpoint",
    context="Context1",
    workspace="main",
    fileName="data.xml",
    body=xml_bytes
)

# Handle the response
if response.status_code == 200:
    print("XML successfully sent to STEP")
else:
    print(f"Error: Status code {response.status_code}")
    print(response.text)
```

---

## 2. Complete Example Function

Note: The `stepxmlclient` uses `requests_openapi` which dynamically generates methods from the OpenAPI spec. There is **no `.inbound()` method**. Instead, you must use one of these endpoints:

- **`postInboundIntegrationEndpointUploadAndInvoke`**: Upload binary/text data AND invoke the endpoint
- **`postInboundIntegrationEndpointInvoke`**: Invoke endpoint (data must already be there)

### Correct Implementation Using `postInboundIntegrationEndpointUploadAndInvoke`

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model.asset import Asset as StepAsset
from stepxmlclient.model.product import Product as StepProduct
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

def send_xml_to_step_inbound(
    username: str,
    password: str,
    step_host: str,
    context_id: str,
    inbound_endpoint_id: str,
    workspace_id: str = "main",
    assets_data: list = None,
    products_data: list = None
) -> dict:
    """
    Create XML using Creator and send it to STEP's inbound integration endpoint.
    
    Args:
        username: STEP username
        password: STEP password
        step_host: STEP host URL (e.g., https://my-step.com/rest/v2)
        context_id: STEP context ID (REQUIRED!) (e.g., "Context1")
        inbound_endpoint_id: ID of the inbound integration endpoint to invoke
        workspace_id: STEP workspace ID (default: "main")
        assets_data: List of asset dictionaries with 'ID', 'Name', etc.
        products_data: List of product dictionaries with 'ID', 'Name', etc.
    
    Returns:
        Dictionary with success status and response details
    """
    
    try:
        if not assets_data:
            assets_data = []
        if not products_data:
            products_data = []
        
        # Step 1: Initialize REST client
        authorisation = BasicAuthorisation(user=username, pwd=password)
        client = StiboStepRestClient(
            location_base=step_host,
            authorisation=authorisation
        )
        
        # Step 2: Create XML with Creator
        creator = Creator(
            context_id=context_id,
            workspace_id=workspace_id
        )
        
        # Add assets to XML
        for asset_data in assets_data:
            step_asset = StepAsset(data=asset_data)
            creator.add(step_asset)
        
        # Add products to XML
        for product_data in products_data:
            step_product = StepProduct(data=product_data)
            creator.add(step_product)
        
        # Build the XML
        creator.build()
        
        # Step 3: Get XML as bytes
        xml_bytes = creator.to_bytes()
        
        # Step 4: Send to STEP inbound using postInboundIntegrationEndpointUploadAndInvoke
        # Parameters:
        # - id: inbound_endpoint_id (path parameter)
        # - context: context_id (REQUIRED query parameter)
        # - workspace: workspace_id (optional query parameter)
        # - fileName: optional file name (query parameter)
        response = client.client.postInboundIntegrationEndpointUploadAndInvoke(
            id=inbound_endpoint_id,
            context=context_id,
            workspace=workspace_id,
            fileName="data.xml",
            body=xml_bytes
        )
        
        return {
            "success": True,
            "message": "Successfully sent XML to STEP inbound",
            "response_status": response.status_code if hasattr(response, 'status_code') else 'Unknown',
            "xml_sent": creator.to_string()[:200] + "..."
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Usage Example:
if __name__ == "__main__":
    result = send_xml_to_step_inbound(
        username="admin",
        password="password123",
        step_host="https://my-step-instance.com/rest/v2",
        context_id="Context1",  # REQUIRED!
        inbound_endpoint_id="my_inbound_endpoint",  # ID of your configured inbound endpoint
        workspace_id="main",
        assets_data=[
            {
                "ID": "asset_001",
                "Name": "Product Image",
                "Description": "High-quality product image",
                "Values": {
                    "FileSize": "2048"
                }
            }
        ],
        products_data=[
            {
                "ID": "product_001",
                "Name": "My Product",
                "UserTypeID": "Product",
                "Values": {
                    "Description": "A sample product",
                    "Price": "99.99",
                    "SKU": "SKU-001"
                }
            }
        ]
    )
    
    print(result)
```

---

## 3. Integration with Connector Hub (in `stibostep/outbound.py`)

```python
from stepxmlclient.creator import Creator
from stepxmlclient.model.asset import Asset as StepAsset
from stepxmlclient.model.product import Product as StepProduct

class StiboStepOutbound(Outbound):
    _SYSTEM_ID = SYSTEMS.STEP
    _CLIENT_BUILDER = StiboStepClientBuilder
    
    def __init__(self, connector_instance, controller):
        super().__init__(connector_instance, controller)
        self.workspace = self.connector_instance.config.get("workspace", "main")
        self.context = self.connector_instance.config.get("context", "Context1")
        self.inbound_endpoint_id = self.connector_instance.config.get("inbound_endpoint_id")
        self.client = self.get_client()
    
    def send_objects_to_step(self, object_container) -> IntegrationAdapterResult:
        """
        Convert ObjectContainer data to XML and send to STEP inbound.
        
        Args:
            object_container: ObjectContainer with products and assets
        
        Returns:
            IntegrationAdapterResult with success/failure info
        """
        try:
            if not self.inbound_endpoint_id:
                return IntegrationAdapterResult(
                    success=False,
                    message="inbound_endpoint_id not configured in connector instance"
                )
            
            # Initialize Creator
            creator = Creator(
                context_id=self.context,
                workspace_id=self.workspace
            )
            
            # Add assets
            for asset in object_container.get_assets():
                step_asset = StepAsset(data=asset.get_attributes())
                creator.add(step_asset)
            
            # Add products
            for product in object_container.get_products():
                step_product = StepProduct(data=product.get_attributes())
                creator.add(step_product)
            
            # Build XML
            creator.build()
            
            # Get XML as bytes
            xml_bytes = creator.to_bytes()
            
            # Send to STEP inbound using postInboundIntegrationEndpointUploadAndInvoke
            response = self.client.client.postInboundIntegrationEndpointUploadAndInvoke(
                id=self.inbound_endpoint_id,
                context=self.context,
                workspace=self.workspace,
                fileName="connector_hub_data.xml",
                body=xml_bytes
            )
            
            if response.status_code == 200:
                return IntegrationAdapterResult(
                    success=True,
                    message=f"Successfully sent XML to STEP inbound endpoint '{self.inbound_endpoint_id}'"
                )
            else:
                error_msg = response.text if hasattr(response, 'text') else str(response)
                return IntegrationAdapterResult(
                    success=False,
                    message=f"Failed to send XML to STEP: HTTP {response.status_code} - {error_msg}"
                )
                
        except Exception as e:
            return IntegrationAdapterResult(
                success=False,
                message=f"Error sending to STEP inbound: {str(e)}"
            )
```

---

## 4. Key Methods and Parameters in stepxmlclient

### Creator Class

```python
Creator(context_id, workspace_id="Main")
```
- **context_id**: STEP context identifier (REQUIRED)
- **workspace_id**: STEP workspace identifier (optional, defaults to "Main")

**Methods:**
- `.add(step_asset)` - Add an Asset to the XML
- `.add(step_product)` - Add a Product to the XML
- `.build()` - Build and finalize the XML structure
- `.to_string()` - Get XML as string (includes XML declaration)
- `.to_bytes()` - Get XML as bytes (includes XML declaration)

### StiboStepRestClient - Inbound Endpoints

The client uses `requests_openapi` which generates methods from the OpenAPI spec. Available inbound methods:

#### postInboundIntegrationEndpointUploadAndInvoke (RECOMMENDED)
```python
client.client.postInboundIntegrationEndpointUploadAndInvoke(
    id="endpoint_id",           # Path parameter: inbound endpoint ID
    context="Context1",         # Query parameter: REQUIRED context ID
    workspace="main",           # Query parameter: optional workspace ID
    fileName="data.xml",        # Query parameter: optional file name
    body=xml_bytes              # Request body: binary data (bytes or string)
)
```

**Returns:** HTTP response object with `.status_code`, `.text`, etc.

#### postInboundIntegrationEndpointInvoke
```python
client.client.postInboundIntegrationEndpointInvoke(
    id="endpoint_id",           # Path parameter: inbound endpoint ID
    context="Context1",         # Query parameter: REQUIRED context ID
    workspace="main"            # Query parameter: optional workspace ID
)
```

**Returns:** HTTP response object

---

## 5. Tips & Best Practices

### Tip 1: Debug XML Before Sending
```python
creator.build()
# Get XML as string
xml_string = creator.to_string()
print(xml_string)
```

### Tip 2: Handle Errors Gracefully
```python
try:
    response = client.client.postInboundIntegrationEndpointUploadAndInvoke(
        id="endpoint_id",
        context="Context1",
        workspace="main",
        fileName="data.xml",
        body=xml_bytes
    )
    if response.status_code == 200:
        print("Success!")
    else:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)  # Contains error details
except requests.exceptions.ConnectionError:
    print("Cannot connect to STEP server")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Tip 3: Batch Multiple Objects
```python
import xml.etree.ElementTree as ET

creator = Creator(context_id="Context1", workspace_id="main")

# Add multiple assets and products
for asset_data in list_of_assets:
    creator.add(StepAsset(data=asset_data))

for product_data in list_of_products:
    creator.add(StepProduct(data=product_data))

creator.build()
xml_bytes = creator.to_bytes()

# Send all at once
response = client.client.postInboundIntegrationEndpointUploadAndInvoke(
    id="endpoint_id",
    context="Context1",
    workspace="main",
    fileName="batch_data.xml",
    body=xml_bytes
)
```

### Tip 4: Use Attributes Mapping
```python
# Map external data to STEP attributes
asset_attributes = {
    "ID": external_asset["id"],
    "Name": external_asset["name"],
    "Values": {
        "FileSize": str(external_asset["size_bytes"]),
        "MimeType": external_asset["file_type"]
    }
}

step_asset = StepAsset(data=asset_attributes)
```

---

## 6. Response Handling

```python
import xml.etree.ElementTree as ET

creator.build()
xml_bytes = creator.to_bytes()

response = client.client.postInboundIntegrationEndpointUploadAndInvoke(
    id="endpoint_id",
    context="Context1",
    workspace="main",
    fileName="data.xml",
    body=xml_bytes
)

# Check status code
if response.status_code == 200:
    print("Success!")
else:
    print(f"Failed with HTTP {response.status_code}")
    error_details = response.text if hasattr(response, 'text') else str(response)
    print(f"Error: {error_details}")
```

---

## 7. Configuration Required

For the connector_hub integration to work, you need to configure:

```json
{
  "inbound_endpoint_id": "my_inbound_endpoint",  // REQUIRED: ID of your STEP inbound endpoint
  "context": "Context1",                          // REQUIRED: STEP context
  "workspace": "main",                            // Optional: STEP workspace (defaults to "main")
  "host": "https://my-step.com/rest/v2",         // REQUIRED: STEP REST API host
  "user": "username",                             // REQUIRED: STEP username
  "pwd": "password"                               // REQUIRED: STEP password
}
```

---

## References
- stepxmlclient documentation: https://github.com/hoerlim/stepxml-client
- STIBO STEP REST API: https://step.stibosystems.com/rest-api
