from typing import Any, Dict, Optional, Callable, Union
from dataclasses import dataclass

from beerest.core.schema import SchemaValidator
from .response import Response
import jsonpath_ng
import re

@dataclass
class Check:
    passed: bool
    message: str
    actual: Any
    expected: Any = None

class Expect:
    def __init__(self, response: Response, context: str = None):
        self.response = response
        self.checks: list[Check] = []
        self.context = context
        self._current_value = None
        
    def that(self, context: str = None) -> 'Expect':
        self.context = context
        return self
        
    def all_passed(self) -> bool:
        return all(check.passed for check in self.checks)
        
    def get_failures(self) -> list[str]:
        return [
            f"{check.message}: expected {check.expected}, got {check.actual}"
            for check in self.checks if not check.passed
        ]

    def _add_check(self, passed: bool, message: str, actual: Any, expected: Any = None):
        if self.context:
            message = f"{self.context}: {message}"
        self.checks.append(Check(passed, message, actual, expected))
        return self

    def status(self, code: int = None) -> 'Expect':
        self._current_value = self.response.status_code
        if code is not None:
            return self.equals(code)
        return self
        
        
    def body(self, path: str = None) -> 'Expect':
        if path:
            if not self.response.json_data:
                raise ValueError("Response has no JSON data")
            try:
                jsonpath_expr = jsonpath_ng.parse(path)
                matches = jsonpath_expr.find(self.response.json_data)
                self._current_value = matches[0].value if matches else None
            except:
                raise ValueError(f"Invalid JSONPath: {path}")
        else:
            self._current_value = self.response.json_data
        return self
        
    def header(self, name: str) -> 'Expect':
        self._current_value = self.response.headers.get(name)
        return self
        
    def time(self) -> 'Expect':
        self._current_value = self.response.elapsed_time
        return self
    
    def equals(self, expected: Any) -> 'Expect':
      passed = str(self._current_value) == str(expected)
      self._add_check(
          passed,
          "equality check",
          self._current_value,
          expected
      )
      if not passed:
          raise AssertionError(f"Expected {expected}, but got {self._current_value}")
      return self
    
    def is_not_empty(self) -> 'Expect':
        return self._add_check(
        bool(self._current_value),
        "empty check",
        self._current_value,
        "non-empty value"
    )

        
    def contains(self, expected: Any) -> 'Expect':
        return self._add_check(
            expected in self._current_value,
            "contains check",
            self._current_value,
            expected
        )
        
    def matches(self, pattern: str) -> 'Expect':
        return self._add_check(
            bool(re.match(pattern, str(self._current_value))),
            "pattern match",
            self._current_value,
            pattern
        )
        
    def less_than(self, value: Any) -> 'Expect':
        return self._add_check(
            self._current_value < value,
            "less than check",
            self._current_value,
            value
        )
        
    def greater_than(self, value: Any) -> 'Expect':
        return self._add_check(
            self._current_value > value,
            "greater than check",
            self._current_value,
            value
        )
        
    def has_length(self, length: int) -> 'Expect':
        return self._add_check(
            len(self._current_value) == length,
            "length check",
            len(self._current_value),
            length
        )
        
    def is_json(self) -> 'Expect':
        return self._add_check(
            self.response.json_data is not None,
            "JSON validation",
            bool(self.response.json_data)
        )
        
    def has_keys(self, *keys: str) -> 'Expect':
        missing = [k for k in keys if k not in self._current_value]
        return self._add_check(
            not missing,
            "keys presence check",
            set(self._current_value.keys()),
            set(keys)
        )
    
    def is_in(self, expected: Any) -> 'Expect':
        return self._add_check(
            self._current_value in expected,
            "is in check",
            self._current_value,
            expected
        )

    def satisfies(self, predicate: Callable[[Any], bool], message: str = "custom check") -> 'Expect':
        return self._add_check(
            predicate(self._current_value),
            message,
            self._current_value
        )
    
    def matches_schema(self, schema: Union[Dict[str, Any], str]) -> 'Expect':
        validator = SchemaValidator()
        
        if isinstance(schema, str):
            schema = validator.load_schema(schema)
        
        result = validator.validate(self._current_value, schema)
        
        return self._add_check(
            result.is_valid,
            f"schema validation: {result.error_messages if not result.is_valid else ''}",
            self._current_value,
            schema
        )

    def has_type(self, expected_type: str) -> 'Expect':
        schema = {"type": expected_type}
        return self.matches_schema(schema)

    def has_array_items(self, item_schema: Dict[str, Any]) -> 'Expect':
        schema = {
            "type": "array",
            "items": item_schema
        }
        return self.matches_schema(schema)
