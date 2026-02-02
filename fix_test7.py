import re

with open('test_parser_phase7_system.py', 'r') as f:
    content = f.read()

# Replace all parse_str with parse(ET.fromstring
content = re.sub(
    r'parser\.parse_str\(xml\)',
    'parser.parse(ET.fromstring(xml))',
    content
)

# Remove all XML namespaces
content = content.replace(' xmlns="http://www.stibosystems.com/step"', '')

# Remove XML declaration
content = re.sub(r'<?xml version="1\.0" encoding="UTF-8"\?>\s*', '', content)

with open('test_parser_phase7_system.py', 'w') as f:
    f.write(content)

print('File updated')
