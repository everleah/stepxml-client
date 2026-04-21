import json
spec = json.load(open('stepxmlclient/openapi.json'))

# Show all operations for the main entity endpoints - with their param names
for path, path_item in spec['paths'].items():
    if any(x in path for x in ['/product', '/asset', '/classification', '/entit', '/attribute', '/list-of-value']):
        for method, op in path_item.items():
            if method in ('get', 'post', 'put', 'delete', 'patch'):
                op_id = op.get('operationId', '?')
                print(f'{op_id} -> {method.upper()} {path}')
                for p in op.get('parameters', []):
                    if '$ref' in p:
                        ref = p['$ref'].split('/')[-1]
                        p = spec['components']['parameters'][ref]
                    req = 'REQ' if p.get('required') else 'opt'
                    default = p.get('schema', {}).get('default', '')
                    print(f'   [{req}] {p["in"]:6} {p["name"]:35} default={default}')
