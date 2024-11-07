from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import httpx
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from .response import Response

class Authentication(ABC):
    @abstractmethod
    def apply(self, headers: Dict[str, str], auth: Optional[Any]) -> Tuple[Dict[str, str], Optional[Any]]:
        """Apply authentication to the request"""
        pass

class BearerTokenAuth(Authentication):
    def __init__(self, token: str):
        self.token = token
    
    def apply(self, headers: Dict[str, str], auth: Optional[Any]) -> Tuple[Dict[str, str], Optional[Any]]:
        headers['Authorization'] = f'Bearer {self.token}'
        return headers, auth

class BasicAuth(Authentication):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def apply(self, headers: Dict[str, str], auth: Optional[Any]) -> Tuple[Dict[str, str], Optional[Any]]:
        return headers, HTTPBasicAuth(self.username, self.password)

class DigestAuth(Authentication):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def apply(self, headers: Dict[str, str], auth: Optional[Any]) -> Tuple[Dict[str, str], Optional[Any]]:
        return headers, HTTPDigestAuth(self.username, self.password)

@dataclass
class Request:
    base_url: str = ""
    url: str = ""
    method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    json_data: Optional[Dict[str, Any]] = None
    query_params: Dict[str, Any] = field(default_factory=dict)
    timeout: float = 5.0
    authentication: Optional[Authentication] = None

    def to(self, endpoint: str) -> 'Request':
        self.url = f"{self.base_url}{endpoint}"
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'Request':
        self.headers.update(headers)
        return self

    def with_body(self, data: Dict[str, Any]) -> 'Request':
        self.json_data = data
        return self

    def with_query(self, params: Dict[str, Any]) -> 'Request':
        self.query_params.update(params)
        return self

    def with_timeout(self, timeout: float) -> 'Request':
        self.timeout = timeout
        return self

    def with_basic_auth(self, username: str, password: str) -> 'Request':
        self.authentication = BasicAuth(username, password)
        return self

    def with_digest_auth(self, username: str, password: str) -> 'Request':
        self.authentication = DigestAuth(username, password)
        return self

    def with_bearer_token(self, token: str) -> 'Request':
        self.authentication = BearerTokenAuth(token)
        return self

    def with_custom_auth(self, auth: Authentication) -> 'Request':
        self.authentication = auth
        return self

    def get(self) -> 'Response':
        return self._execute("GET")

    def post(self) -> 'Response':
        return self._execute("POST")

    def put(self) -> 'Response':
        return self._execute("PUT")

    def delete(self) -> 'Response':
        return self._execute("DELETE")

    def _execute(self, method: str) -> 'Response':
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with 'http://' or 'https://'")

        self.method = method
        headers = self.headers.copy()
        auth = None

        if self.authentication:
            headers, auth = self.authentication.apply(headers, auth)

        with httpx.Client(timeout=httpx.Timeout(self.timeout)) as client:
            response = client.request(
                method=method,
                url=self.url,
                headers=headers,
                json=self.json_data if method in ["POST", "PUT", "PATCH"] else None,
                params=self.query_params,
                auth=auth
            )

            json_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    json_data = response.json()
                except ValueError:
                    pass

            return Response(
                status_code=response.status_code,
                headers=dict(response.headers),
                json_data=json_data,
                text=response.text,
                elapsed_time=response.elapsed.total_seconds() * 1000
            )