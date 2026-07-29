#!/usr/bin/env python
"""Quick test that StiboStepRestClient has inbound operations."""

from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

print('Creating mock client...')
auth = BasicAuthorisation(user='test', pwd='test')
try:
    client = StiboStepRestClient(
        location_base='https://fake-step.com/restapiv2',
        authorisation=auth,
        context='TestContext',
        nocert=True
    )
    print(f'✓ StiboStepRestClient has inbound: {hasattr(client, "inbound")}')
    print(f'✓ inbound is not None: {client.inbound is not None}')
    if client.inbound:
        print(f'✓ inbound has upload_and_invoke: {hasattr(client.inbound, "upload_and_invoke")}')
        print(f'✓ inbound has list_endpoints: {hasattr(client.inbound, "list_endpoints")}')
        print(f'✓ inbound has get_status: {hasattr(client.inbound, "get_status")}')
        print('\nAll checks passed! ✅')
except Exception as e:
    import traceback
    print(f'Error: {e}')
    traceback.print_exc()
