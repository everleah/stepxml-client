import json

spec = json.load(open('stepxmlclient/openapi.json'))

# Look at the search body condition schema detail
for path, path_item in spec['paths'].items():
    for method, op in path_item.items():
        if method == 'post' and 'search' in path and op.get('operationId', '').startswith('postProducts'):
            body = op.get('requestBody', {})
            content = body.get('content', {})
            for ct, ct_data in content.items():
                schema = ct_data.get('schema', {})
                if '$ref' in schema:
                    ref = schema['$ref'].split('/')[-1]
                    schema = spec['components']['schemas'].get(ref, {})
                print(f"Schema for {op['operationId']} body:")
                print(json.dumps(schema, indent=2)[:3000])
                print()

# Also check if there are any global pagination parameters
print("=== Components Parameters ===")
for name, param in spec['components']['parameters'].items():
    print(f"  {name}: {param.get('in')} / {param.get('name')} - required={param.get('required',False)}")
