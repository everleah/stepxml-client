import requests
import requests_openapi as roa
import logging
import os
import json

class StiboStepRestClient:

    _OPENAPI_CACHE_FILE = "openapi.json"

    def __init__(
            self, location_base, authorisation,
            openapi_file=None, logger=None,
            proxies = None, ssl_version = None, 
            cache_openapi = False, nocert=False):
        self.ssl_version = ssl_version
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
        else:
            self.logger = logger
        # build location base
        location_base = location_base.lower()
        if not location_base.startswith('http'):
            location_base = '%s://%s' % ('https', location_base)
        if location_base.endswith('/'):
            location_base = location_base[:-1]
        # create client
        self.__create_client(location_base, openapi_file, cache_openapi)
        # set server
        self.client.set_server(roa.Server(url=location_base))
        if isinstance(self.client.requestor, requests.Session):
            # no ssl verify?
            if nocert or os.path.exists('nocert'):
                self.client.requestor.verify=False
            # proxies
            if isinstance(proxies, dict):
                self.client.requestor.proxies.update(proxies)
        self.proxies = proxies
        # authorisation (Always after creating client!)
        authorisation.adapt_client(self.client)
        authorisation.do_authorisation(self.client)
        return

    def __create_client(self, location_base, openapi_file, cache_openapi):
        if cache_openapi:
            if openapi_file is None:
                openapi_file = self._OPENAPI_CACHE_FILE
        if openapi_file:
            if os.path.exists(openapi_file):
                self.client = roa.Client().load_spec_from_file(openapi_file)
            elif cache_openapi:
                spec = roa.core.load_spec_from_url(
                    f'{location_base}/specification/openapi.json')
                with open(openapi_file,'w') as oaf:
                    json.dump(spec, oaf)
                self.client = roa.Client()
                self.client.load_spec(spec)
            else:
                raise FileNotFoundError(
                    f"Open API JSON File '{openapi_file}' not found!")
        else:
            self.client = roa.Client().load_spec_from_url(
                f'{location_base}/specification/openapi.json')
        return

class __Authorisation:

    TYPE = None

    def adapt_client(self, client):
        return

    def do_authorisation(self, client):
        return

    def get_type(self):
        return self.TYPE

class BasicAuthorisation(__Authorisation):

    TYPE = "BASIC"

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        return

    def adapt_client(self, client):
        client.requestor.auth = (self.user, self.pwd)
        return


