# beerest: A Modern API Testing Framework for Python

## Overview

beerest is a powerful, fluent Python library designed to simplify API testing while providing robust validation capabilities. It combines a clean, chainable syntax with comprehensive testing features to make API testing more intuitive and maintainable.

## Features

- 🔗 Fluent, chainable API for building requests
- 🔍 Rich assertion library for response validation
- 🛡️ Built-in authentication support (Basic, Digest, Bearer Token)
- 📊 JSON Schema validation
- ⏱️ Response time assertions
- 🔄 Custom validation functions
- 🎯 JSONPath support for precise data access

## Installation

```bash
pip install beerest
```

## Quick Start

### Basic Example

```python
from beerest import Test, Expect

class TestAPI(Test):
    def setup_method(self):
        super().setup_method()
        self.request.base_url = "https://api.example.com"
        
    def test_get_user(self):
        response = self.request.to("/users/1").get()
            
        Expect(response) \
            .status(200) \
            .is_json() \
            .body("name").equals("John Doe") \
            .body("age").greater_than(18)
```

## Core Components

### Request Builder

Build HTTP requests with a fluent interface:

```python
response = (request
    .to("/api/users")                                  # Set endpoint
    .with_headers({"Content-Type": "application/json"}) # Add headers
    .with_body({"name": "John"})                       # Set request body
    .with_query({"active": True})                      # Add query parameters
    .with_timeout(5.0)                                 # Set timeout
    .post()                                            # Send request
)
```

### Authentication Support

Multiple authentication methods available:

```python
# Bearer Token
request.with_bearer_token("your-token")

# Basic Auth
request.with_basic_auth("username", "password")

# Digest Auth
request.with_digest_auth("username", "password")

# Custom Authentication
request.with_custom_auth(MyCustomAuth())
```

### Response Validation

Comprehensive response validation with the `Expect` class:

```python
Expect(response) \
    .status(200) \
    .body("data.users").has_type("array") \
    .body("data.users").has_length(5) \
    .body("metadata.total").greater_than(0) \
    .header("Content-Type").contains("application/json") \
    .time().less_than(500)
```

### Schema Validation

Validate response structure against JSON schemas:

```python
user_schema = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "age": {"type": "integer"}
    }
}

Expect(response) \
    .body() \
    .matches_schema(user_schema)
```

### Custom Validations

Create custom validation rules:

```python
Expect(response) \
    .body("users") \
    .satisfies(
        lambda users: all(user["age"] >= 18 for user in users),
        "All users must be adults"
    )
```

## Advanced Features

### JSONPath Support

Access nested data using JSONPath expressions:

```python
Expect(response) \
    .body("$.data[?(@.type=='user')].name") \
    .contains("John")
```

### Response Time Assertions

Monitor API performance:

```python
Expect(response) \
    .time() \
    .less_than(500)  # Response time under 500ms
```

### Format Validation

Built-in format validators:

```python
Expect(response) \
    .body("email").matches_schema({"type": "string", "format": "email"}) \
    .body("created_at").matches_schema({"type": "string", "format": "date-time-iso"}) \
    .body("id").matches_schema({"type": "string", "format": "uuid"})
```

## Best Practices

1. **Test Organization**
   - Group related tests in test classes
   - Use descriptive test method names
   - Set up common configuration in `setup_method()`

2. **Request Structure**
   - Chain request methods for readability
   - Set base URL in setup
   - Use timeout for all requests

3. **Assertions**
   - Use clear, specific assertions
   - Chain validations logically
   - Include both positive and negative tests

4. **Error Handling**
   - Test error responses
   - Validate error messages
   - Check edge cases

## Example Test Suite

```python
class TestUserAPI(Test):
    def setup_method(self):
        super().setup_method()
        self.request.base_url = "https://api.example.com"
        
    def test_create_user(self):
        """Test user creation with valid data"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 25
        }
        
        response = self.request \
            .to("/users") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(user_data) \
            .post()
            
        Expect(response) \
            .status(201) \
            .body("id").is_not_empty() \
            .body("name").equals(user_data["name"]) \
            .body("email").equals(user_data["email"])
            
    def test_get_user_not_found(self):
        """Test handling of non-existent user"""
        response = self.request.to("/users/999999").get()
            
        Expect(response) \
            .status(404) \
            .body("error").equals("User not found")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.