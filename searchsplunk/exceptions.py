"""
Splunk exception clasess
"""


class SplunkError(Exception):
    pass


class SplunkInvalidCredentials(SplunkError):
    pass
