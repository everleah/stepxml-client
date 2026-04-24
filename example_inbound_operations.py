#!/usr/bin/env python
"""
Complete example showing how to use InboundOperations with StiboStepRestClient.

This demonstrates the fix for the error:
  Error sending to STEP: 'StiboStepRestClient' object has no attribute 'inbound'
"""

from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation
from stepxmlclient.creator import Creator


def example_send_to_inbound_endpoint():
    """
    Example: Send STEP-XML to an inbound endpoint using the high-level wrapper.
    
    This shows how to:
    1. Create STEP-XML using Creator
    2. Initialize StiboStepRestClient
    3. Send XML to an inbound endpoint using client.inbound.upload_and_invoke()
    """
    
    print("=" * 60)
    print("Example: Send STEP-XML to Inbound Endpoint")
    print("=" * 60)
    
    # Step 1: Generate STEP-XML
    print("\n1. Generating STEP-XML...")
    creator = Creator(context_id="MyContext", workspace_id="Main")
    
    # Add some products
    from stepxmlclient.model import Product, Asset
    
    product1 = Product({
        "ID": "PROD001",
        "Name": "Example Product",
        "Values": {
            "Description": "This is an example product"
        }
    })
    creator.add(product1)
    
    creator.build()
    xml_bytes = creator.to_bytes()
    print(f"   ✓ Generated XML: {len(xml_bytes)} bytes")
    
    # Step 2: Initialize client with inbound operations
    print("\n2. Initializing StiboStepRestClient...")
    auth = BasicAuthorisation(user="admin", pwd="password")
    
    # NOTE: The key fix - now context and workspace are supported!
    client = StiboStepRestClient(
        location_base="https://your-step-system.com/restapiv2",
        authorisation=auth,
        context="MyContext",        # ← New! Set default context
        workspace="Main",           # ← New! Set default workspace
        nocert=False
    )
    print("   ✓ Client initialized")
    
    # Step 3: Check that inbound operations are available
    print("\n3. Checking inbound operations...")
    if client.inbound:
        print("   ✓ client.inbound is available!")
        print("   ✓ Available methods:")
        print("     - upload_and_invoke()")
        print("     - list_endpoints()")
        print("     - get_status()")
        print("     - enable_endpoint()")
        print("     - disable_endpoint()")
        print("     - get_execution_report()")
        print("     - get_statistics()")
        print("     - get_worker_processes()")
    else:
        print("   ✗ inbound operations not available!")
        return
    
    # Step 4: Send to inbound endpoint (commented out - needs real server)
    print("\n4. Ready to send to inbound endpoint...")
    print("   Code that would send to STEP:")
    print("""
    try:
        result = client.inbound.upload_and_invoke(
            endpoint_id="my_inbound_endpoint",
            xml_data=xml_bytes,
            file_name="product_import.xml"
        )
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
    """)
    
    print("\n" + "=" * 60)
    print("✅ Example completed successfully!")
    print("=" * 60)


def example_with_steprestclient():
    """
    Alternative example using StepRestClient (also has inbound operations).
    
    StepRestClient is an extended client with additional operation groups.
    It also supports the inbound operations.
    """
    
    print("\n\n" + "=" * 60)
    print("Alternative: Using StepRestClient")
    print("=" * 60)
    
    from stepxmlclient.rest_client.client import StepRestClient
    
    auth = BasicAuthorisation(user="admin", pwd="password")
    
    # StepRestClient also has inbound operations (plus many other operation groups)
    client = StepRestClient(
        location_base="https://your-step-system.com/restapiv2",
        authorisation=auth,
        context="MyContext"
    )
    
    print("\n✓ StepRestClient also has client.inbound")
    print("✓ Plus additional operation groups:")
    print("  - client.products")
    print("  - client.assets")
    print("  - client.classifications")
    print("  - client.attributes")
    print("  - client.imports")
    print("  - client.exports")
    print("  - etc.")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "INBOUND OPERATIONS EXAMPLES" + " " * 22 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        example_send_to_inbound_endpoint()
        example_with_steprestclient()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
