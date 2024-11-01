from typing import Dict, Any, Optional
import httpx
from dataclasses import dataclass, field
from .response import Response 

@dataclass
class Request:
    base_url: str = ""
    url: str = ""
    method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    json_data: Optional[Dict[str, Any]] = None
    query_params: Dict[str, Any] = field(default_factory=dict)
    timeout: float = 5.0

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
        with httpx.Client(timeout=httpx.Timeout(self.timeout)) as client:
            response = client.request(
                method=method,
                url=self.url,
                headers=self.headers,
                json=self.json_data if method in ["POST", "PUT", "PATCH"] else None,
                params=self.query_params
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
