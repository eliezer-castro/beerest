from typing import Any, Dict, List
from dataclasses import dataclass
from jsonschema import validators
from jsonschema.exceptions import ValidationError
import json

@dataclass
class SchemaValidationResult:
    is_valid: bool
    errors: List[str]
    value: Any
    schema: Dict[str, Any]

    @property
    def error_messages(self) -> str:
        return "\n".join(self.errors)

class SchemaValidator:

    def __init__(self):
        self.validator_cls = validators.validator_for({})
        self.validator_cls.check_schema = classmethod(self._check_schema)
        
        self.custom_formats = {
            "email": self._is_email,
            "date-time-iso": self._is_iso_datetime,
            "uuid": self._is_uuid,
            "url": self._is_url
        }
        
    @staticmethod
    def _check_schema(cls, schema: Dict) -> None:
        validators.validate(schema, cls.META_SCHEMA)

    def _format_error(self, error: ValidationError) -> str:
        path = " -> ".join(str(p) for p in error.path) if error.path else "root"
        return f"At {path}: {error.message}"

    @staticmethod
    def _is_email(value: str) -> bool:
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, value))

    @staticmethod
    def _is_iso_datetime(value: str) -> bool:
        import re
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$"
        return bool(re.match(pattern, value))

    @staticmethod
    def _is_uuid(value: str) -> bool:
        import re
        pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        return bool(re.match(pattern, value.lower()))

    @staticmethod
    def _is_url(value: str) -> bool:
        import re
        pattern = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$"
        return bool(re.match(pattern, value))

    def validate(self, value: Any, schema: Dict[str, Any]) -> SchemaValidationResult:
        validator = self.validator_cls(schema)
        errors = []
        
        try:
            validator.validate(value)
            is_valid = True
        except ValidationError as e:
            errors.append(self._format_error(e))
            is_valid = False
        except Exception as e:
            errors.append(f"Unexpected error during validation: {str(e)}")
            is_valid = False
            
        return SchemaValidationResult(
            is_valid=is_valid,
            errors=errors,
            value=value,
            schema=schema
        )

    def load_schema(self, schema_path: str) -> Dict[str, Any]:
        with open(schema_path, 'r') as f:
            return json.load(f)
