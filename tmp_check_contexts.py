from stepxmlclient.rest_client.client import StepRestClient
from stepxmlclient.client import BasicAuthorisation

client = StepRestClient('https://bito-preprod.mdm.stibosystems.com/restapiv2', BasicAuthorisation('API_USER_HOERL', 'qMfFDaB2oZTx'), nocert=True)
raw = client.client.getContexts(**client.contexts._build_context_params())
print('RAW TYPE:', type(raw))
print('RAW REPR:', repr(raw))
if hasattr(raw, 'json'):
    try:
        print('RAW JSON:', raw.json())
    except Exception as e:
        print('RAW JSON ERR:', e)
if hasattr(raw, 'text'):
    print('RAW TEXT:', raw.text[:2000])
if hasattr(raw, 'dict'):
    try:
        print('RAW DICT:', raw.dict())
    except Exception as e:
        print('RAW DICT ERR:', e)
if isinstance(raw, dict):
    print('RAW KEYS:', list(raw.keys()))
    for k in list(raw.keys())[:20]:
        print(k, type(raw.get(k)), repr(raw.get(k))[:300])
