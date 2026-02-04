"""
STEP XML Client Library.

A Python client library for integrating with Stibo Systems STEP MDM (Master Data Management).
Supports standard STEP-XML protocol (OIEP/IIEP) for parsing and creating STEP-XML documents,
and wraps the STEP REST API v2 for direct system integration.

This library provides:
- Parser: Deserialize STEP-XML documents into Python dictionaries
- Creator: Serialize Python objects into STEP-XML documents
- REST Client: Direct integration with STEP REST API v2
- Asset Uploader: Binary file upload support for asset management

Namespaces:
    STEPXML_NS: Dictionary mapping namespace prefixes to their URIs used throughout STEP-XML documents
"""

#: XML namespace URIs used in STEP documents
STEPXML_NS = {
    'step' : 'http://www.stibosystems.com/step',
    'outputtemplate' : 'http://www.stibosystems.com/step/outputtemplate'
}