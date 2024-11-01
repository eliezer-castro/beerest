from typing import Any

class Assertions:
    @staticmethod
    def assertEqual(actual: Any, expected: Any, message: str = None):
        if actual != expected:
            raise AssertionError(message or f"Expected '{expected}', but got '{actual}'")

    @staticmethod
    def assertTrue(condition: bool, message: str = None):
        if not condition:
            raise AssertionError(message or "Condition is not True")

    @staticmethod
    def assertFalse(condition: bool, message: str = None):
        if condition:
            raise AssertionError(message or "Condition is not False")

    @staticmethod
    def assertNotNull(value: Any, message: str = None):
        if value is None:
            raise AssertionError(message or "Value is None")

    @staticmethod
    def assertLess(a: Any, b: Any, message: str = None):
        if not a < b:
            raise AssertionError(message or f"Expected '{a}' to be less than '{b}'")

    @staticmethod
    def assertGreater(a: Any, b: Any, message: str = None):
        if not a > b:
            raise AssertionError(message or f"Expected '{a}' to be greater than '{b}'")

    @staticmethod
    def assertIn(element: Any, collection: Any, message: str = None):
        if element not in collection:
            raise AssertionError(message or f"Expected '{element}' to be in '{collection}'")
