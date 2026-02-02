import xml.etree.ElementTree as ET
from stepxmlclient.parser import Parser

xml_str = '''
<STEP-ProductInformation>
    <Attributes/>
    <AttributeGroups/>
    <ListOfValuesGroupList/>
    <ListOfValues>
        <ListOfValue ID="ProductCategoryLOV" UseValueID="true" AllowUserValueAddition="false" DefaultUnitID="DefaultUnit">
            <Name>Product Categories</Name>
            <Validation Base="Text"/>
            <DimensionLink DimensionID="Region"/>
            <MetaData>
                <Value AttributeID="source">Master Data</Value>
            </MetaData>
            <AttributeGroupLink AttributeGroupID="ProductProperties"/>
            <Value ID="ELEC">Electronics</Value>
            <Value ID="CLOTH">Clothing</Value>
            <ValueGroup ID="FoodGroup">
                <Value ID="FOOD_DRY">Dry Foods</Value>
                <Value ID="FOOD_FRZ">Frozen Foods</Value>
            </ValueGroup>
            <DeleteValue Force="true" GenerateEvents="false">OBSOLETE</DeleteValue>
        </ListOfValue>
    </ListOfValues>
    <Products/>
    <Assets/>
    <DeleteAssets/>
    <DeleteProducts/>
    <Classifications/>
</STEP-ProductInformation>
'''

parser = Parser()
parser.parse(ET.fromstring(xml_str))
lov = parser.list_of_values[0]
print(f'Keys in LOV: {list(lov.keys())}')
if 'Value' in lov:
    print(f'Number of Values: {len(lov["Value"])}')
    for i, v in enumerate(lov['Value']):
        print(f'  Value {i}: ID={v.get("ID")}, value={v.get("value")}')
else:
    print('No Values parsed')
if 'ValueGroup' in lov:
    print(f'Number of ValueGroups: {len(lov["ValueGroup"])}')
else:
    print('No ValueGroups parsed')

