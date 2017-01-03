import re
import httpretty
import pytest
from searchsplunk.searchsplunk import SearchSplunk
from searchsplunk.exceptions import SplunkInvalidCredentials


auth_response = """<response>
  <sessionKey>abc123efg456</sessionKey>
</response>
"""

bad_auth_response = """
Invalid login credentials!
"""

search_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
  <sid>1483419124.3</sid>
</response>
"""

search_status = """<s:key name="isDone">1</s:key>
"""

search_result = """
{
    "fields":[
        {
            "name":"_bkt"
        },
        {
            "name":"_cd"
        },
        {
            "name":"_indextime"
        },
        {
            "name":"_kv"
        },
        {
            "name":"_raw"
        },
        {
            "name":"_serial"
        },
        {
            "name":"_si"
        },
        {
            "name":"_sourcetype"
        },
        {
            "name":"_subsecond"
        },
        {
            "name":"_time"
        },
        {
            "name":"host"
        },
        {
            "name":"index"
        },
        {
            "name":"linecount"
        },
        {
            "name":"openstack_uid"
        },
        {
            "name":"source"
        },
        {
            "name":"sourcetype"
        },
        {
            "name":"splunk_server"
        }
    ],
    "init_offset":0,
    "messages":[

    ],
    "preview":false,
    "results":[
        {
            "_bkt":"main~1122~25B521A6-9612-407D-A1BA-F8KJSEBB7628",
            "_cd":"1122:290410720",
            "_indextime":"1435071966",
            "_kv":"1",
            "_raw":"somefile contents",
            "_serial":"0",
            "_si":[
                "splunkserv",
                "main"
            ],
            "_sourcetype":"salt:grains",
            "_time":"2015-06-23T11:06:05.000-04:00",
            "host":"server-7654.acme.com",
            "index":"main",
            "linecount":"17",
            "openstack_uid":"e0303456c-d5a3-789f-ab68-8f27561ffa0f",
            "source":"/etc/salt/grains",
            "sourcetype":"salt:grains",
            "splunk_server":"splunkmaster"
        }
    ]
}
"""


@pytest.mark.httpretty
def test_searchsplunk():
    """
    Login and running a search should return a result
    """
    httpretty.register_uri(
        httpretty.POST,
        'http://example.com/services/auth/login',
        body=auth_response
    )
    httpretty.register_uri(
        httpretty.POST,
        'http://example.com/services/search/jobs',
        body=search_response
    )
    httpretty.register_uri(
        httpretty.GET,
        'http://example.com/services/search/jobs/1483419124.3',
        body=search_status
    )
    httpretty.register_uri(
        httpretty.GET,
        'http://example.com/services/search/jobs/1483419124.3/results',
        body=search_result
    )

    s = SearchSplunk(
        'http://example.com/',
        'MYUSER',
        'MYPASS'
    )

    result = s.search(
        'sourcetype=salt:grains '
        'openstack_uid=e0303456c-d5a3-789f-ab68-8f27561ffa0f | '
        'dedup openstack_uid'
    )
    assert len(result['results']) == 1


@pytest.mark.httpretty
def test_version_is_valid():
    """
    Getting the module version should work as expected
    """
    httpretty.register_uri(
        httpretty.POST,
        'http://example.com/services/auth/login',
        body=auth_response
    )

    s = SearchSplunk(
        'http://example.com/',
        'MYUSER',
        'MYPASS'
    )
    assert bool(re.match(r'^\d+\.\d+\.\d+$', str(s.version))) is True


@pytest.mark.httpretty
def test_bad_login():
    """
    Bad login should raise a SplunkInvalidCredentials exception
    """
    httpretty.register_uri(
        httpretty.POST,
        'http://example.com/services/auth/login',
        body=bad_auth_response
    )

    with pytest.raises(SplunkInvalidCredentials):
        SearchSplunk(
            'http://example.com/',
            'MYUSER',
            'MYPASS'
        )
