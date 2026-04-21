import json
spec = json.load(open('stepxmlclient/openapi.json'))

ops_of_interest = ['getProduct','deleteProduct','putProduct','patchProduct','postProducts','postProductsSearch',
    'getAsset','deleteAsset','putAsset','patchAsset','postAssets','postAssetsSearch','getAssetContent','putAssetContent',
    'getClassification','deleteClassification','putClassification','patchClassification','postClassifications','postClassificationsSearch',
    'getEntity','deleteEntity','putEntity','patchEntity','postEntities','postEntitiesSearch',
    'getAttribute','getListOfValue','postExport','postImport']

for path, path_item in spec['paths'].items():
    for method, op in path_item.items():
        if method in ('get', 'post', 'put', 'delete', 'patch'):
            op_id = op.get('operationId', '')
            if op_id in ops_of_interest:
                params = op.get('parameters', [])
                resolved = []
                for p in params:
                    if '$ref' in p:
                        ref = p['$ref'].split('/')[-1]
                        p = spec['components']['parameters'][ref]
                    resolved.append(p)
                print(f'{op_id} {method.upper()} {path}')
                for p in resolved:
                    req = 'REQ' if p.get('required') else 'opt'
                    default = p.get('schema', {}).get('default', '')
                    print(f'  [{req}] {p["in"]:6} {p["name"]:35} default={default}')
                print()
