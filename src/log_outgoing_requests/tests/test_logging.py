from django.test import TestCase, override_settings

import requests
import requests_mock
from freezegun import freeze_time

from ..models import OutgoingRequestsLog


@requests_mock.Mocker()
@freeze_time("2021-10-18 13:00:00")
class OutgoingRequestsLoggingTests(TestCase):
    def _setUpMocks(self, m):
        m.get(
            "http://example.com/some-path?version=2.0",
            status_code=200,
            content=b"some content",
        )

    def test_outgoing_requests_are_logged(self, m):
        self._setUpMocks(m)

        with self.assertLogs("requests", level="DEBUG") as logs:
            requests.get("http://example.com/some-path?version=2.0")

        self.assertEqual(logs.output, ["DEBUG:requests:Outgoing request"])
        self.assertEqual(logs.records[0].name, "requests")
        self.assertEqual(logs.records[0].getMessage(), "Outgoing request")
        self.assertEqual(logs.records[0].levelname, "DEBUG")

    @override_settings(LOG_OUTGOING_REQUESTS_DB_SAVE=True)
    def test_expected_data_is_saved_when_saving_enabled(self, m):
        self._setUpMocks(m)

        methods = [
            ("POST", requests.post, m.post),
            ("PUT", requests.put, m.put),
            ("PATCH", requests.patch, m.patch),
            ("DELETE", requests.delete, m.delete),
            ("HEAD", requests.head, m.head),
        ]

        for method, func, mocked in methods:
            with self.subTest():
                mocked(
                    "http://example.com/some-path?version=2.0",
                    status_code=200,
                    content=b"some content",
                )

                response = func("http://example.com/some-path?version=2.0")

                request_log = OutgoingRequestsLog.objects.last()

                self.assertEqual(
                    request_log.url, "http://example.com/some-path?version=2.0"
                )
                self.assertEqual(request_log.hostname, "example.com")
                self.assertEqual(request_log.params, "")
                self.assertEqual(request_log.query_params, "version=2.0")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(request_log.method, method)
                self.assertEqual(request_log.req_content_type, "")
                self.assertEqual(request_log.res_content_type, "")
                self.assertEqual(request_log.response_ms, 0)
                self.assertEqual(
                    request_log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "2021-10-18 13:00:00",
                )
                self.assertIsNone(request_log.trace)

    def test_data_is_not_saved_when_saving_disabled(self, m):
        self._setUpMocks(m)

        with self.assertLogs("requests", level="DEBUG") as logs:
            requests.get("http://example.com/some-path?version=2.0")

        self.assertEqual(logs.output, ["DEBUG:requests:Outgoing request"])
        self.assertEqual(logs.records[0].name, "requests")
        self.assertEqual(logs.records[0].getMessage(), "Outgoing request")
        self.assertEqual(logs.records[0].levelname, "DEBUG")
        self.assertFalse(OutgoingRequestsLog.objects.exists())

    @override_settings(LOG_OUTGOING_REQUESTS_DB_SAVE=False)
    def test_outgoing_requests_are_logged_when_saving_disabled(self, m):
        self._setUpMocks(m)

        with self.assertLogs("requests", level="DEBUG") as logs:
            requests.get("http://example.com/some-path?version=2.0")

        self.assertEqual(logs.output, ["DEBUG:requests:Outgoing request"])
        self.assertEqual(logs.records[0].name, "requests")
        self.assertEqual(logs.records[0].getMessage(), "Outgoing request")
        self.assertEqual(logs.records[0].levelname, "DEBUG")

    @override_settings(LOG_OUTGOING_REQUESTS_DB_SAVE=False)
    def test_request_data_is_not_saved_when_saving_disabled(self, m):
        self._setUpMocks(m)

        requests.get("http://example.com/some-path?version=2.0")

        self.assertFalse(OutgoingRequestsLog.objects.exists())