
from stepxmlclient.client import StiboStepRestClient, BasicAuthorisation

authorisation = BasicAuthorisation('CLHA', 'CLHA')
rest_client = StiboStepRestClient(
    location_base='https://hoerl-sb01.mdm.stibosystems.com/restapiv2',
    authorisation=authorisation, 
    cache_openapi=True, 
    nocert=True)

print(rest_client)