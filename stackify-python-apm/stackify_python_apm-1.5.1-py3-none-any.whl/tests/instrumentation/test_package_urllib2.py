from unittest import TestCase
from unittest import SkipTest
try:
    from unittest import mock
except Exception:
    import mock

try:
    import urllib2
except Exception:
    raise SkipTest('Skipping due to version incompatibility')

from stackifyapm.base import Client
from stackifyapm.traces import execution_context
from stackifyapm.instrumentation import register
from stackifyapm.instrumentation import control

CONFIG = {
    "SERVICE_NAME": "service_name",
    "ENVIRONMENT": "production",
    "HOSTNAME": "sample_host",
    "FRAMEWORK_NAME": "framework",
    "FRAMEWORK_VERSION": "1.0",
    "APPLICATION_NAME": "sample_application",
    "BASE_DIR": "path/to/application/",
}


class HttpResponseMock(object):

    def __init__(self, code):
        self.code = code


class Urllib2InstrumentationTest(TestCase):
    def setUp(self):
        self.client = Client(CONFIG)
        register._cls_registers = {
            "stackifyapm.instrumentation.packages.urllib2.Urllib2Instrumentation",
        }

    def setUpSuccess(self):
        self.http_response = HttpResponseMock(200)
        self.setUpContinue()

    def setUpFailed(self):
        self.http_response = HttpResponseMock(404)
        self.setUpContinue()

    def setUpContinue(self):
        self.openurl = mock.patch('urllib2.urlopen')
        self.openurl_mock = self.openurl.start()
        self.openurl_mock.return_value = self.http_response

    def tearDown(self):
        control.uninstrument()
        self.openurl.stop()

    def test_successful_request(self):
        self.setUpSuccess()
        control.instrument()
        self.client.begin_transaction("transaction_test")

        urllib2.urlopen('http://www.python.org/')
        self.assert_span(status=200)

    def test_unsuccessful_request(self):
        self.setUpFailed()
        control.instrument()
        self.client.begin_transaction("transaction_test")

        urllib2.urlopen('http://www.python.org/')
        self.assert_span(status=404)

    def assert_span(self, status):
        transaction = execution_context.get_transaction()
        assert transaction
        assert transaction.get_spans()

        span = transaction.get_spans()[0]
        span_data = span.to_dict()

        assert span_data['reqBegin']
        assert span_data['reqEnd']
        assert span_data['transaction_id']
        assert span_data['call'] == 'ext.http.urllib2'
        assert span_data['props']
        assert span_data['props']['CATEGORY'] == 'Web External'
        assert span_data['props']['SUBCATEGORY'] == 'Execute'
        assert span_data['props']['COMPONENT_CATEGORY'] == 'Web External'
        assert span_data['props']['COMPONENT_DETAIL'] == 'Execute'
        assert span_data['props']['URL'] == 'http://www.python.org/'
        assert span_data['props']['STATUS'] == status
