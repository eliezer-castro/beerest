from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Response:
    status_code: int
    headers: Dict[str, str]
    json_data: Optional[Dict[str, Any]]
    text: str
    elapsed_time: float