import json

from resultsdb_frontend.proxy import ReverseProxied
from resultsdb_frontend.requests_session import ErrorResponse
from resultsdb_frontend.resultsdb_api import _prepare_params


class TestPrepareParams:
    def test_string_values(self):
        assert _prepare_params(foo="bar") == {"foo": "bar"}

    def test_list_values(self):
        assert _prepare_params(items=["a", "b"]) == {"items": "a,b"}

    def test_none_values_excluded(self):
        assert _prepare_params(foo="bar", empty=None) == {"foo": "bar"}

    def test_empty(self):
        assert _prepare_params() == {}

    def test_integer_values(self):
        assert _prepare_params(page=1, limit=10) == {"page": "1", "limit": "10"}


class TestErrorResponse:
    def test_status_code(self):
        resp = ErrorResponse(504, "timeout", "http://example.com")
        assert resp.status_code == 504

    def test_content(self):
        resp = ErrorResponse(502, "connection error", "http://example.com")
        data = json.loads(resp.content)
        assert data == {"message": "connection error"}

    def test_url(self):
        resp = ErrorResponse(504, "timeout", "http://example.com/api")
        assert resp.url == "http://example.com/api"


class TestReverseProxied:
    def _make_environ(self, **kwargs):
        environ = {
            "PATH_INFO": "/test",
            "REQUEST_METHOD": "GET",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "5000",
        }
        environ.update(kwargs)
        return environ

    def test_script_name(self):
        app_calls = []

        def mock_app(environ, start_response):
            app_calls.append(environ.copy())
            return []

        proxied = ReverseProxied(mock_app)
        environ = self._make_environ(
            HTTP_X_SCRIPT_NAME="/prefix",
            PATH_INFO="/prefix/test",
        )
        proxied(environ, None)
        assert app_calls[0]["SCRIPT_NAME"] == "/prefix"
        assert app_calls[0]["PATH_INFO"] == "/test"

    def test_forwarded_host(self):
        app_calls = []

        def mock_app(environ, start_response):
            app_calls.append(environ.copy())
            return []

        proxied = ReverseProxied(mock_app)
        environ = self._make_environ(HTTP_X_FORWARDED_HOST="example.com")
        proxied(environ, None)
        assert app_calls[0]["HTTP_HOST"] == "example.com"

    def test_scheme(self):
        app_calls = []

        def mock_app(environ, start_response):
            app_calls.append(environ.copy())
            return []

        proxied = ReverseProxied(mock_app)
        environ = self._make_environ(HTTP_X_SCHEME="https")
        proxied(environ, None)
        assert app_calls[0]["wsgi.url_scheme"] == "https"

    def test_no_proxy_headers(self):
        app_calls = []

        def mock_app(environ, start_response):
            app_calls.append(environ.copy())
            return []

        proxied = ReverseProxied(mock_app)
        environ = self._make_environ()
        proxied(environ, None)
        assert "SCRIPT_NAME" not in app_calls[0]
        assert app_calls[0]["PATH_INFO"] == "/test"
