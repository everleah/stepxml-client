import json
import re


mapping = {
    '/assets/{id}/references/{referenceTypeId}' : '/assets/{id}/references',
    '/classifications/{id}/references/{referenceTypeId}' : '/classifications/{id}/references',
    '/entities/{id}/references/{referenceTypeId}' : '/entities/{id}/references',
    '/products/{id}/references/{referenceTypeId}' : '/products/{id}/references'}

def simplify_path(path):
    # Teile den Pfad in Segmente, um ihn schrittweise zu verarbeiten
    segments = path.split("/")
    simplified_segments = []
    
    for i, segment in enumerate(segments):
        # Wenn das Segment ein Platzhalter ist ({...}), das vorherige Segment prüfen
        if re.match(r"\{[^/]+\}", segment) and i > 0:
            # Entferne Plural nur vom vorherigen Segment, falls sinnvoll
            previous_segment = simplified_segments.pop()
            # Ersetze "-tasks" mit "-task" oder "s" nur am Ende von Wörtern
            previous_segment = re.sub(r"s\b", "", previous_segment, flags=re.IGNORECASE)
            simplified_segments.append(previous_segment)
        elif segment:  # Füge normale Segmente unverändert hinzu
            simplified_segments.append(segment)
    
    # Kombiniere die Segmente zurück zu einem Pfad
    return "/" + "/".join(simplified_segments)

def to_camel_case(path):
    if 'processe/' in path:
        path = path.replace("processe/","process/")
    elif  path.endswith('/processe'):
        path = path[:-1]
    if 'entitie/' in path:
        path = path.replace("entitie/","entity/")
    elif path.endswith('/entitie'):
        path = path.replace("/entitie","/entity")
    # Entferne doppelte oder führende/trailing Slashes
    cleaned_path = re.sub(r"/+", "/", path.strip("/"))
    # Teile den String anhand von '/' oder '-' auf
    parts = re.split(r"[/-]", cleaned_path)
    # Kombiniere die Teile: Der erste Teil bleibt klein, der Rest wird großgeschrieben
    camel_case = parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
    return camel_case


with open("openapi_orig.json","r") as f:
    data = json.load(f)
        
paths = data["paths"] 
    
operations = {}

for path, path_data in paths.items():
    simplified = mapping.get(path, simplify_path(path))
    for cmd_key, cmd_data in path_data.items():
        operation_id = to_camel_case(f"{cmd_key}/{simplified}")
        if operation_id in operations:
            print(f"{operation_id} for {cmd_key}:{path} already in use by {operations[operation_id]}")
            cnt=1
            while f"{operation_id}{cnt}" in operations:
                cnt+=1
            operation_id = f"{operation_id}{cnt}"
            print(f"--> use {operation_id} instead")
        operations[operation_id] = f"{cmd_key}:{path}"
        cmd_data['operationId'] = operation_id
            
with open("openapi.json","w") as f:
    data = json.dump(data,f)
    
print("ready.")

        
    
    
