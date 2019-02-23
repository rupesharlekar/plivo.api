import json
import pytest
import requests
from requests.auth import HTTPBasicAuth

from plivoConfig import PlivoConfig

class RestClient:
    def __init__(self, host, version, path_prefix='', scheme='https://'):
        self.uri = scheme + host + version + path_prefix

    def send_request(self, *api_name, **api_data):

        requests.session().auth = HTTPBasicAuth(PlivoConfig.AUTH_ID, PlivoConfig.AUTH_TOKEN)

        self.uri = self.uri + '/' + PlivoConfig.AUTH_ID + '/'

        api_url = self.uri + api_name[0]

        if api_data:
            resp = requests.post(api_url, json=api_data)
        else:
            resp = requests.get(api_url)

        if resp.status_code == requests.codes.ok:
            return json.loads(resp.text)

@pytest.fixture(autouse=True, scope="session")
def initialise():

    caller_server_host      = PlivoConfig.CLOUD_FQDN
    caller_api_version      = '/v1'
    caller_api_path_prefix  = '/Account'
    caller_scheme           = 'https://'

    __builtins__['callerRestClient'] = RestClient(caller_server_host, caller_api_version,
                                            path_prefix=caller_api_path_prefix, scheme=caller_scheme)
