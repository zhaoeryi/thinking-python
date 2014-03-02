import thinking
import httplib
import json
import urllib
from oslo.config import cfg
import logging

CONF = cfg.CONF
_opts = [
    cfg.StrOpt('auth_host'),
    cfg.StrOpt('auth_port'),
    cfg.StrOpt('os_user'),
    cfg.StrOpt('os_password'),
    cfg.StrOpt('os_tenant_name'),
    cfg.StrOpt('admin_token'),
    ]
thinking.CONF.register_opts(_opts)

LOG = logging.getLogger("hacking")

def safe_quote(s):
    """URL-encode strings that are not already URL-encoded."""
    return urllib.quote(s) if s == urllib.unquote(s) else s

def json_request(host, port, method, path, body=None, additional_headers=None):
    """HTTP request helper used to make json requests.

    :param method: http method
    :param path: relative request url
    :param body: dict to encode to json as request body. Optional.
    :param additional_headers: dict of additional headers to send with
                                   http request. Optional.
    :return (http response object, response body parsed as json)
    :raise ServerError when unable to communicate with keystone
    """
    kwargs = {
            'headers': {
                'Content-type': 'application/json',
                'Accept': 'application/json',
            },
    }
    
    if additional_headers:
        kwargs['headers'].update(additional_headers)

    if body:
        kwargs['body'] = body

    conn = httplib.HTTPConnection(host, port)
    conn.request(method, path, **kwargs)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data = json.loads(data)
    except ValueError:
        LOG.debug('Keystone did not return json-encoded body')
        data = {}

    return response, data

class KeystoneTestCase(thinking.HackingTestCase):


    def verify_uuid_token(self, user_token):
        """Authenticate user token with keystone.

        :param user_token: user's token id
        :param retry: flag that forces the middleware to retry
                      user authentication when an indeterminate
                      response is received. Optional.
        :return token object received from keystone on success
        :raise InvalidUserToken if token is rejected
        :raise ServiceError if unable to authenticate token

        """
        
        # verify user token by admin token
        headers = {'X-Auth-Token': CONF.admin_token}
        response, data = json_request(CONF.auth_host,
                                     CONF.auth_port,
                                     "GET",
                                     '/v2.0/tokens/%s' % safe_quote(user_token),
                                     additional_headers=headers)
        if response.status == 200:
            LOG.info("Authorization success for token %s", user_token)
            return data
        if response.status == 404:
            LOG.warn("Authorization failed for token %s", user_token)
            raise Exception('Token authorization failed')
        if response.status == 401:
            LOG.info(
                'Keystone rejected admin token %s, resetting', headers)
        else:
            LOG.error('Bad response code while validating token: %s' % 
                           response.status)
        
        LOG.warn("Invalid user token: %s. Keystone response: %s.",
                          user_token, data)
        
        raise Exception()
        
    def test_get_user_token(self):
        params = {
            'auth': {
                'passwordCredentials': {
                    'username': CONF.os_user,
                    'password': CONF.os_password,
                },
                'tenantName': CONF.os_tenant_name,
            }
        }
        
        body = json.dumps(params)
        resonse, data = json_request(CONF.auth_host, CONF.auth_port, "POST", "/v2.0/tokens", body=body)
        
        # pretty print
        print 'data=', json.dumps(data, sort_keys=True, indent=4)
        
        apitoken = data['access']['token']['id']

        print "Your token is: %s" % apitoken

        self.verify_uuid_token(apitoken)