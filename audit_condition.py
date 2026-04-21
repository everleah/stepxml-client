import json

spec = json.load(open('stepxmlclient/openapi.json'))

# Look at the Condition schema
cond_schema = spec['components']['schemas'].get('Condition', {})
print("Condition schema:")
print(json.dumps(cond_schema, indent=2)[:5000])
print()

# Also look at the SearchRequest schema referenced in search bodies
for schema_name, schema in spec['components']['schemas'].items():
    if 'search' in schema_name.lower() or 'query' in schema_name.lower() or 'condition' in schema_name.lower():
        print(f"Schema: {schema_name}")
        print(json.dumps(schema, indent=2)[:2000])
        print()
