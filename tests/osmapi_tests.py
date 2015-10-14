from __future__ import unicode_literals
from nose.tools import *  # noqa
from osmapi import OsmApi
import mock
import os
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


class TestOsmApi(unittest.TestCase):
    def setUp(self):
        self.api_base = "http://api06.dev.openstreetmap.org"
        self.api = OsmApi(
            api=self.api_base
        )
        self.maxDiff = None
        print(self._testMethodName)
        print(self.api)

    def _conn_mock(self, auth=False, filenames=None, status=200, reason=None):
        if auth:
            self.api._username = 'testuser'
            self.api._password = 'testpassword'

        response_mock = mock.Mock()
        response_mock.status_code = status
        return_values = self._return_values(filenames)
        if len(return_values) > 1:
            print('Need to split these tests')  # TODO: remove debug
        if return_values:
            response_mock.text = return_values[0]

        conn_mock = mock.Mock()
        conn_mock.get = mock.Mock(return_value=response_mock)
        conn_mock.post = mock.Mock(return_value=response_mock)
        conn_mock.update = mock.Mock(return_value=response_mock)
        conn_mock.delete = mock.Mock(return_value=response_mock)
        conn_mock.head = mock.Mock(return_value=response_mock)
        conn_mock.put = mock.Mock(return_value=response_mock)

        self.api._get_http_connection = mock.Mock(return_value=conn_mock)
        self.api._conn = conn_mock

        self.api._sleep = mock.Mock()

    def _return_values(self, filenames):
        if filenames is None:
            filenames = [self._testMethodName + ".xml"]

        return_values = []
        for filename in filenames:
            path = os.path.join(
                __location__,
                'fixtures',
                filename
            )
            try:
                with open(path) as file:
                    return_values.append(file.read())
            except:
                pass
        return return_values

    def teardown(self):
        pass

    def test_constructor(self):
        assert_true(isinstance(self.api, OsmApi))
