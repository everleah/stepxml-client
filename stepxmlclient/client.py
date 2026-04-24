import requests
import requests_openapi as roa
import logging
import os
import json
from pathlib import Path


def _lazy_import_inbound_operations():
    """Lazy import InboundOperations to avoid circular imports.
    
    Returns:
        InboundOperations class or None if import fails
    """
    try:
        from stepxmlclient.rest_client.operations.inbound import InboundOperations
        return InboundOperations
    except ImportError:
        return None

class StiboStepRestClient:

    _OPENAPI_CACHE_FILE = "openapi.json"

    def __init__(
            self, location_base, authorisation,
            openapi_file=None, logger=None,
            proxies = None, ssl_version = None, 
            cache_openapi = False, nocert=False,
            context=None, workspace=None):
        self.ssl_version = ssl_version
        self.context = context
        self.workspace = workspace
        
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
        
        # Initialize inbound operations (lazy import to avoid circular dependencies)
        InboundOperations = _lazy_import_inbound_operations()
        if InboundOperations:
            self.inbound = InboundOperations(
                self.client,
                logger=self.logger,
                context=context,
                workspace=workspace
            )
        else:
            self.inbound = None
        
        return

    @staticmethod
    def _get_bundled_openapi_file():
        """Get the path to the bundled openapi.json file.
        
        Returns:
            Path to bundled openapi.json if it exists, None otherwise
        """
        try:
            # Get the directory of this module
            module_dir = Path(__file__).parent
            bundled_file = module_dir / 'openapi.json'
            if bundled_file.exists():
                return str(bundled_file)
        except Exception:
            pass
        return None

    def __create_client(self, location_base, openapi_file, cache_openapi):
        """Create and initialize the OpenAPI client.
        
        Internal method that loads the OpenAPI specification and creates the
        requests-openapi client instance.
        
        Priority order for loading spec:
        1. Specified openapi_file (if exists)
        2. Cache file (if caching enabled and exists)
        3. Bundled openapi.json (shipped with package)
        4. Fetch from STEP server (if caching enabled, save to cache)
        
        Args:
            location_base: Base URL of the STEP API server
            openapi_file: Path to OpenAPI specification file (if available)
            cache_openapi: Whether to cache the OpenAPI spec if fetched
            
        Raises:
            FileNotFoundError: If specified openapi_file doesn't exist and no other source available
        """
        # Determine which file to try to load
        cache_file = self._OPENAPI_CACHE_FILE if cache_openapi else None
        bundled_file = self._get_bundled_openapi_file()
        
        # Try specified openapi_file first
        if openapi_file:
            if os.path.exists(openapi_file):
                self.client = roa.Client().load_spec_from_file(openapi_file)
                return
            elif not cache_openapi:
                # User specified a file that doesn't exist and isn't caching, so fail
                raise FileNotFoundError(
                    f"Open API JSON File '{openapi_file}' not found!")
            # else: continue to try other sources
        
        # Try cache file if caching is enabled
        if cache_file and os.path.exists(cache_file):
            self.logger.debug(f"Loading OpenAPI spec from cache: {cache_file}")
            self.client = roa.Client().load_spec_from_file(cache_file)
            return
        
        # Try bundled file (always available as fallback)
        if bundled_file:
            self.logger.debug(f"Loading OpenAPI spec from bundled file: {bundled_file}")
            self.client = roa.Client().load_spec_from_file(bundled_file)
            return
        
        # Last resort: fetch from server
        self.logger.debug(f"Loading OpenAPI spec from server: {location_base}/specification/openapi.json")
        spec = roa.core.load_spec_from_url(
            f'{location_base}/specification/openapi.json')
        
        # If caching is enabled, save the spec
        if cache_openapi and cache_file:
            self.logger.debug(f"Caching OpenAPI spec to: {cache_file}")
            with open(cache_file, 'w') as f:
                json.dump(spec, f)
        
        self.client = roa.Client()
        self.client.load_spec(spec)
        return

class __Authorisation:
    """Abstract base class for authentication handlers.
    
    Provides the interface that all authentication implementations must follow.
    Subclasses should override adapt_client() and do_authorisation() as needed.
    """

    #: Authentication type identifier (override in subclasses)
    TYPE = None

    def adapt_client(self, client):
        """Adapt the client with authentication-specific configuration.
        
        Called to modify the client's request session or configuration
        before making authenticated requests.
        
        Args:
            client: The requests_openapi.Client instance to configure
        """
        return

    def do_authorisation(self, client):
        """Perform any post-initialization authorization setup.
        
        Called after client creation and adaptation to perform additional
        authorization steps if needed (e.g., token refresh, permission checks).
        
        Args:
            client: The requests_openapi.Client instance
        """
        return

    def get_type(self):
        """Get the authentication type identifier.
        
        Returns:
            String identifying the authentication type (e.g., 'BASIC')
        """
        return self.TYPE

class BasicAuthorisation(__Authorisation):
    """HTTP Basic Authentication handler.
    
    Implements Basic Authentication (username/password) for STEP REST API requests.
    Credentials are sent in the Authorization header with each request.
    """

    #: Authentication type identifier
    TYPE = "BASIC"

    def __init__(self, user, pwd):
        """Initialize BasicAuthorisation with credentials.
        
        Args:
            user: Username for Basic Auth
            pwd: Password for Basic Auth
        """
        self.user = user
        self.pwd = pwd
        return

    def adapt_client(self, client):
        client.requestor.auth = (self.user, self.pwd)
        return


