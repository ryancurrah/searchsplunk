[![Build Status](https://travis-ci.org/ryancurrah/searchsplunk.svg?branch=master)](https://travis-ci.org/ryancurrah/searchsplunk) [![Coverage Status](https://coveralls.io/repos/github/ryancurrah/searchsplunk/badge.svg?branch=master)](https://coveralls.io/github/ryancurrah/searchsplunk?branch=master)


# Search Splunk

Easily create Splunk searches from Python and get the result as a Python object

# Requires

- requests>=2.7.0: https://pypi.python.org/pypi/requests

# Installation instructions

[Searchsplunk](https://pypi.python.org/pypi/searchsplunk) can be installed from PyPi.

```bash
pip install searchsplunk
```

# Usage instructions

```python
from searchsplunk.searchsplunk import SearchSplunk
s = SearchSplunk('https://splunk.acme.com:8089', 'MYUSER', 'MYPASS', ssl_verify=True)
result = s.search('sourcetype=salt:grains openstack_uid=e0303456c-d5a3-789f-ab68-8f27561ffa0f | dedup openstack_uid')

import json
print json.dumps(result, sort_keys=True, indent=2)
{
  "fields": [
    {
      "name": "_bkt"
    },
    {
      "name": "_cd"
    },
    {
      "name": "_indextime"
    },
    {
      "name": "_kv"
    },
    {
      "name": "_raw"
    },
    {
      "name": "_serial"
    },
    {
      "name": "_si"
    },
    {
      "name": "_sourcetype"
    },
    {
      "name": "_subsecond"
    },
    {
      "name": "_time"
    },
    {
      "name": "host"
    },
    {
      "name": "index"
    },
    {
      "name": "linecount"
    },
    {
      "name": "openstack_uid"
    },
    {
      "name": "source"
    },
    {
      "name": "sourcetype"
    },
    {
      "name": "splunk_server"
    }
  ],
  "init_offset": 0,
  "messages": [],
  "preview": false,
  "results": [
    {
      "_bkt": "main~1122~25B521A6-9612-407D-A1BA-F8KJSEBB7628",
      "_cd": "1122:290410720",
      "_indextime": "1435071966",
      "_kv": "1",
      "_raw": "somefile contents",
      "_serial": "0",
      "_si": [
        "splunkserv",
        "main"
      ],
      "_sourcetype": "salt:grains",
      "_time": "2015-06-23T11:06:05.000-04:00",
      "host": "server-7654.acme.com",
      "index": "main",
      "linecount": "17",
      "openstack_uid": "e0303456c-d5a3-789f-ab68-8f27561ffa0f",
      "source": "/etc/salt/grains",
      "sourcetype": "salt:grains",
      "splunk_server": "splunkmaster"
    }
  ]
}
```

## Contributors

  - [pkeeper](https://github.com/pkeeper)

## Author

[Ryan Currah](ryan@currah.ca)

## License

GPL v2
