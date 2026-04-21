import json

spec = json.load(open('stepxmlclient/openapi.json'))

# Look at search operation bodies and GET parameter lists for key entities
ops = ['postProductsSearch', 'postAssetsSearch', 'postClassificationsSearch', 'postEntitiesSearch',
       'getProduct', 'getAsset', 'getClassification', 'getEntity', 'getAttribute', 'getListOfValue',
       'deleteProduct', 'deleteAsset', 'deleteClassification', 'deleteEntity',
       'patchProduct', 'patchAsset', 'patchClassification', 'patchEntity',
       'putProduct', 'putAsset', 'putClassification', 'putEntity',
       'postProducts', 'postAssets', 'postClassifications', 'postEntities']

for path, path_item in spec['paths'].items():
    for method, op in path_item.items():
        if method in ('get', 'post', 'put', 'delete', 'patch'):
            op_id = op.get('operationId', '')
            if op_id in ops:
                print(f'=== {op_id} {method.upper()} {path} ===')
                # Parameters
                params = op.get('parameters', [])
                for p in params:
                    if '$ref' in p:
                        ref = p['$ref'].split('/')[-1]
                        p = spec['components']['parameters'][ref]
                    req = 'REQ' if p.get('required') else 'opt'
                    print(f'  param [{req}] {p["in"]:6} {p["name"]}')
                # Request body
                body = op.get('requestBody', {})
                if body:
                    content = body.get('content', {})
                    for ct, ct_data in content.items():
                        schema = ct_data.get('schema', {})
                        if '$ref' in schema:
                            ref = schema['$ref'].split('/')[-1]
                            schema = spec['components']['schemas'].get(ref, {})
                        props = schema.get('properties', {})
                        req_fields = schema.get('required', [])
                        print(f'  body ({ct}): required={req_fields}, fields={list(props.keys())[:10]}')
                print()
