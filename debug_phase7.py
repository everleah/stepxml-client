import xml.etree.ElementTree as ET
from stepxmlclient.parser import Parser

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<STEP-ProductInformation xmlns="http://www.stibosystems.com/step">
    <UserTypes>
        <UserType ID="Product">
            <Name>Product Object Type</Name>
        </UserType>
    </UserTypes>
</STEP-ProductInformation>'''

# First check what the tag looks like
root = ET.fromstring(xml)
print(f'Root tag: {root.tag}')
print()

parser = Parser()
try:
    # Handle the namespaced tag
    if root.tag == '{http://www.stibosystems.com/step}STEP-ProductInformation':
        # Strip namespace for assertion
        from stepxmlclient import STEPXML_NS
        parser.parse(root)
    else:
        parser.parse_str(xml)
    
    print(f'User types parsed: {len(parser.user_types)}')
    if parser.user_types:
        print(f'First user type: {parser.user_types[0]}')
    else:
        print('No user types found')
except Exception as e:
    import traceback
    traceback.print_exc()
