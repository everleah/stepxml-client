# STEP XML Client Models - AGENTS.md

## Purpose
Local contract for the STEP XML object model classes under `stepxmlclient/model/`.

## Ownership
- `asset.py`
- `attribute.py`
- `business.py`
- `classification.py`
- `complex_elements.py`
- `deletion.py`
- `entity.py`
- `metadata.py`
- `organization.py`
- `product.py`
- `relations.py`
- `replacement.py`
- `__init__.py`

## Local Contracts
- All entity classes inherit from `BaseObject` and use declarative class-level serialization metadata.
- Model field names must stay aligned with creator output and the STEP XML schema.
- Keep child element handling compatible with the recursive serialization behavior in `BaseObject`.

## Work Guidance
- When adding or changing a model, update the related creator and parser behavior at the same time.
- Prefer changes that preserve existing XML element names and attribute names.
- Add or update model-focused tests when the serialized XML shape changes.

## Verification
- `test_complex_element_objects.py`
- `test_creator_roundtrip.py`
- `test_creator_xml.py`
- `validate_xml_xsd.py`

## Child DOX Index
- None.