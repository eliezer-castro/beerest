import pytest
from beerest.core.request import Request
from beerest.core.response import Response

class TestRequest:
    def setup_method(self):
        self.request = Request()
        
    def test_to_method(self):
        self.request.base_url = "https://api.example.com"
        request = self.request.to("/users")
        assert request.url == "https://api.example.com/users"
        
    def test_with_headers(self):
        headers = {"Authorization": "Bearer token"}
        request = self.request.with_headers(headers)
        assert request.headers == headers
        
    def test_with_body(self):
        data = {"name": "John", "age": 30}
        request = self.request.with_body(data)
        assert request.json_data == data
        
    def test_with_query(self):
        params = {"page": 1, "limit": 10}
        request = self.request.with_query(params)
        assert request.query_params == params
        
    def test_with_timeout(self):
        request = self.request.with_timeout(10.0)
        assert request.timeout == 10.0
        
    def test_invalid_url(self):
        self.request.url = "invalid-url"
        with pytest.raises(ValueError, match="URL must start with 'http://' or 'https://'"):
            self.request._execute("GET")