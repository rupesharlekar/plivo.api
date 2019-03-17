import json
import pytest
import requests
from requests.auth import HTTPBasicAuth

from tests import PlivoConfig


class RestClient:
    def __init__(self, host, version, path_prefix='', scheme='https://'):
        """
        :param host: Base URL
        :param version: API version
        :param path_prefix:
        :param scheme: whether http or https

        request session is created with Basic Authentication
        """
        self.uri = scheme + host + version + path_prefix

        self.req = requests.session()
        self.req.verify = False
        self.req.auth = HTTPBasicAuth(PlivoConfig.AUTH_ID, PlivoConfig.AUTH_TOKEN)

    def send_request(self, *api_name, **api_data):
        """

        :param api_name: the endpoint on which the request will take place, will be used for GET, POST both
        :param api_data: will be used only for POST request which has a request payload key=value pairs
                         combination is sent here
        :return: perform actual HTTP call and retun HTTP status code and Response content
        """
        api_url = self.uri + api_name[0]

        if api_data:
            # import pdb;pdb.set_trace()
            resp = self.req.post(api_url, json=api_data)
        else:
            resp = self.req.get(api_url)

        if resp.status_code in [requests.codes.ok, requests.codes.created, requests.codes.accepted]:
            return (resp.status_code, json.loads(resp.text))

@pytest.fixture(autouse=True, scope="session")
def initialise():
    """
    Based on the highest scope 'Session' this method is called first
    RestClient named callerRestClient is created
    """
    caller_server_host      = PlivoConfig.CLOUD_FQDN
    caller_api_version      = '/v1'
    caller_api_path_prefix  = '/Account/'
    caller_scheme           = 'https://'

    __builtins__['callerRestClient'] = RestClient(caller_server_host, caller_api_version,
                                            path_prefix=caller_api_path_prefix, scheme=caller_scheme)
