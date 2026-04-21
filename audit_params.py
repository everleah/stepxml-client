import json

spec = json.load(open('stepxmlclient/openapi.json'))

# Extract all operations with their parameters
for path, path_item in spec['paths'].items():
    for method, op in path_item.items():
        if method in ('get', 'post', 'put', 'delete', 'patch'):
            op_id = op.get('operationId', '?')
            params = op.get('parameters', [])
            # Resolve $refs
            resolved = []
            for p in params:
                if '$ref' in p:
                    ref = p['$ref'].split('/')[-1]
                    p = spec['components']['parameters'][ref]
                resolved.append(p)
            required = [p for p in resolved if p.get('required')]
            optional = [p for p in resolved if not p.get('required')]
            req_str = [(p['name'], p['in']) for p in required]
            opt_str = [(p['name'], p['in']) for p in optional]
            if req_str or opt_str:
                print(f'{op_id}')
            if req_str:
                print(f'  REQUIRED: {req_str}')
            if opt_str:
                print(f'  OPTIONAL: {opt_str}')
