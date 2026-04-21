import json

spec = json.load(open('stepxmlclient/openapi.json'))

print("=== OPERATION RESPONSES FROM SPEC ===\n")
for path, methods in sorted(spec['paths'].items()):
    for method, op in methods.items():
        if method == 'parameters':
            continue
        op_id = op.get('operationId', '?')
        responses = op.get('responses', {})
        for code, resp in responses.items():
            schema_ref = None
            content = resp.get('content', {})
            for ct, cv in content.items():
                schema = cv.get('schema', {})
                ref = schema.get('$ref')
                typ = schema.get('type')
                if ref:
                    schema_ref = ref.split('/')[-1]
                elif typ:
                    schema_ref = typ
            print(f"{method.upper():6s} {op_id:55s} {code}: {schema_ref}")

print("\n=== SCHEMA DEFINITIONS ===\n")
schemas = spec.get('components', {}).get('schemas', {})
for name, schema in sorted(schemas.items()):
    required = schema.get('required', [])
    props = list(schema.get('properties', {}).keys())
    print(f"{name}: required={required}, props={props[:6]}{'...' if len(props)>6 else ''}")
