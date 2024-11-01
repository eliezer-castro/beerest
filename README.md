# beerest: Simplifying API Testing in Python

## Overview

beerest is a lightweight, intuitive Python library designed to simplify API testing with a fluent and robust interface. It provides a comprehensive set of tools for making HTTP requests, asserting responses, and performing complex API validations.

## Installation

```bash
pip install beerest
```

## Core Components

### 1. Request Class

The `Request` class allows you to construct and send HTTP requests with a fluent, chainable API.

#### Methods

- `.to(endpoint)`: Set the target endpoint
- `.with_headers(headers)`: Add custom headers
- `.with_body(data)`: Set request payload
- `.with_query(params)`: Add query parameters
- `.with_timeout(timeout)`: Set request timeout
- `.get()`: Perform GET request
- `.post()`: Perform POST request
- `.put()`: Perform PUT request
- `.delete()`: Perform DELETE request

#### Example

```python
from beerest.core.request import Request

request = Request()
request.base_url = "https://api.example.com"
response = (request
    .to("/users")
    .with_headers({"Authorization": "Bearer token"})
    .with_query({"active": True})
    .get()
)
```

### 2. Expect Class

The `Expect` class provides a powerful, fluent assertion mechanism for validating API responses.

#### Validation Methods

- `.status(code)`: Check HTTP status code
- `.body(path=None)`: Access response body or JSON path
- `.header(name)`: Access response headers
- `.time()`: Check response time
- `.equals(value)`: Check exact equality
- `.contains(value)`: Check if value is contained
- `.matches(pattern)`: Check regex pattern match
- `.less_than(value)`: Check numerical comparison
- `.greater_than(value)`: Check numerical comparison
- `.has_length(length)`: Check collection length
- `.is_json()`: Validate JSON response
- `.has_keys(*keys)`: Check JSON keys presence
- `.satisfies(predicate)`: Custom validation function

#### Example

```python
from beerest.core.expect import Expect

Expect(response) \
    .status(200) \
    .body("user.name").equals("John Doe") \
    .body("user.age").greater_than(18) \
    .header("Content-Type").contains("application/json")
```

### 3. Assertions Class

Traditional assertion methods for more complex validations.

#### Methods

- `assertEqual(actual, expected)`
- `assertTrue(condition)`
- `assertFalse(condition)`
- `assertNotNull(value)`
- `assertLess(a, b)`
- `assertGreater(a, b)`
- `assertIn(element, collection)`

#### Example

```python
from beerest.core.assertions import Assertions

Assertions.assertEqual(response.status_code, 200)
Assertions.assertNotNull(response.json_data)
```

## Test Setup

Inherit from the `Test` base class to create structured API tests:

```python
from beerest.core.test import Test
from beerest.core.expect import Expect

class TestUserAPI(Test):
    def setup_method(self):
        super().setup_method()
        self.request.base_url = "https://api.example.com"
    
    def test_get_users(self):
        response = self.request.to("/users").get()
        
        Expect(response) \
            .status(200) \
            .body().has_length(10)
```

## Advanced Usage

### Timeout Configuration

```python
response = self.request \
    .to("/slow-endpoint") \
    .with_timeout(5.0)  # 5 seconds timeout
    .get()
```

### Complex Assertions

```python
Expect(response) \
    .status(200) \
    .body("data.users") \
        .has_length(5) \
        .satisfies(lambda users: all(user["active"] for user in users))
```

### Performance Testing

```python
Expect(response) \
    .time().less_than(500)  # Response under 500ms
```

## Best Practices

1. Always set `base_url` in `setup_method()`
2. Use method chaining for readability
3. Combine `Expect` with traditional `Assertions`
4. Write descriptive test method names
5. Test both positive and negative scenarios

## Error Handling

- Invalid URLs will raise `ValueError`
- Assertion failures raise `AssertionError`
- Non-JSON responses are handled gracefully

## Contributing

Contributions are welcome! Please submit issues and pull requests on our GitHub repository.

## License

beerest is open-source software licensed under the MIT License.