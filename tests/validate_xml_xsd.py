#!/usr/bin/env python3
"""Validate generated XML against STEP.xsd schema."""

from lxml import etree
from stepxmlclient.creator import Creator
from stepxmlclient.model import Product, Asset, Attribute, ListOfValues

# Generate sample XML
creator = Creator("GlobalContext", "Main")
product = Product({"ID": "P001", "Name": "Test Product"})
creator.add(product)
creator.build()
xml_bytes = creator.to_bytes()

# Save for inspection
with open("sample_output.xml", "wb") as f:
    f.write(xml_bytes)
print("✓ Saved generated XML to sample_output.xml")

# Load XSD
try:
    xsd_doc = etree.parse("STEP.xsd")
    xsd_schema = etree.XMLSchema(xsd_doc)
    print("✓ Loaded STEP.xsd schema")
    
    # Parse generated XML
    xml_doc = etree.fromstring(xml_bytes)
    
    # Validate
    if xsd_schema.validate(xml_doc):
        print("✅ XML VALIDATES against XSD")
    else:
        print("❌ XML VALIDATION FAILED")
        print("\nValidation Errors:")
        for error in xsd_schema.error_log:
            print(f"  {error}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
