import re
import warnings
import requests
from xml.dom import minidom
from xml.parsers.expat import ExpatError
from .exceptions import SplunkInvalidCredentials
from .version import __version__

warnings.filterwarnings('ignore')


class Splunk(object):
    """
    Splunk base class
    """
    session_key = None

    def __init__(self, url, username, password, ssl_verify=True):
        """
        Initialize Splunk search client

        :param url: Url of splunk server eg: https://splunk.acme.com:8089
        :param username: Splunk username
        :param password: Splunk password
        :param ssl_verify: True or False whether or not to verify Splunk
                           SSL certificate
        """
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        self.ssl_verify = ssl_verify
        self.__login()
        return

    @property
    def version(self):
        """
        Get the module version

        :return: The module version
        """
        return __version__

    def __login(self):
        """
        Gets and sets a session key, sessions by default in Splunk are
        valid for one hour
        """
        method = 'POST'
        uri = '/services/auth/login'

        r = self.request(
            method,
            uri,
            body={'username': self.username, 'password': self.password}
        )

        try:
            self.session_key = minidom.parseString(
                r.text
            ).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
        except (IndexError, KeyError, ExpatError):
            raise SplunkInvalidCredentials(
                'HTTP status code:\n{0}\nError message:\n{1}'.format(
                    r.status_code,
                    r.text
                )
            )
        return

    @property
    def session_header(self):
        """
        Return dictionary auth session header if logged in
        """
        return {
            'Authorization': 'Splunk {0}'.format(self.session_key)
        } if self.session_key else {}

    def request(self, method, uri, body={}, params={}, headers={}, auth=()):
        """
        Make HTTP requests

        :param method: post, get, put, delete
        :param uri: /some/api/uri/url/will/be/appended/automatically
        :param body: body data of dict
        :param params: get parameters of dict
        :param headers: http headers of dict
        :param auth: auth tuple username, password of tuple
        :return: A Requests response object
        """
        headers.update(self.session_header)

        return requests.request(
            method,
            '{0}{1}'.format(self.url, uri),
            headers=headers,
            data=body,
            params=params,
            auth=auth,
            verify=self.ssl_verify
        )


class SearchSplunk(Splunk):
    """
    Splunk search class
    """
    def search(self, search_query):
        """
        Creates search jobs in Splunk and returns the result or raises
        exception

        :param search_query: The search query string
        :return: Search result python object
        """
        sid = self.__start_search(search_query)

        search_done = False
        while not search_done:
            if self.__search_status(sid):
                search_done = True
        return self.__search_result(sid)

    def __start_search(self, search_query):
        """
        Starts a search job in Splunk

        :param search_query: The search query string
        :return: The Splunk search job id otherwise raises exceptions
        """
        method = 'POST'
        uri = '/services/search/jobs'

        if not search_query.startswith('search'):
            search_query = '{0} {1}'.format('search ', search_query)

        s = self.request(method, uri, body={'search': search_query})

        return minidom.parseString(
            s.text
        ).getElementsByTagName('sid')[0].childNodes[0].nodeValue

    def __search_status(self, sid):
        """
        Gets the status of a search job

        :param sid: The Splunk search job id
        :return: True for search job done or False for search job not done
        """
        method = 'GET'
        uri = '/services/search/jobs/{0}'

        s = self.request(method, uri.format(sid))
        return int(re.compile('isDone">(0|1)').search(s.text).groups()[0])

    def __search_result(self, sid):
        """
        Returns the results of a search job

        :param sid: The Splunk search job id
        :return: The search job as a python object
        """
        method = 'GET'
        uri = '/services/search/jobs/{0}/results'

        return self.request(
            method,
            uri.format(sid),
            params={'output_mode': 'json'}
        ).json()
