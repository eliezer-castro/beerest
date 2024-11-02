# tests/core/test_schema_validator.py
import pytest
from beerest.core.schema import SchemaValidator

class TestSchemaValidator:
    @pytest.fixture
    def validator(self):
        return SchemaValidator()
        
    @pytest.fixture
    def simple_schema(self):
        return {
            "type": "object",
            "required": ["name", "age", "email"],
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "email": {"type": "string", "format": "email"}
            }
        }

    def test_valid_object_validation(self, validator, simple_schema):
        """Testa validação de um objeto válido"""
        valid_data = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
        
        result = validator.validate(valid_data, simple_schema)
        assert result.is_valid
        assert len(result.errors) == 0
        
    def test_invalid_object_validation(self, validator, simple_schema):
        """Testa validação de um objeto com dados inválidos"""
        invalid_data = {
            "name": "John Doe",
            "age": "not a number",  # deveria ser inteiro
            "email": "invalid-email"  # email inválido
        }
        
        result = validator.validate(invalid_data, simple_schema)
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_missing_required_field(self, validator, simple_schema):
        """Testa validação quando falta um campo obrigatório"""
        incomplete_data = {
            "name": "John Doe",
            "age": 30
            # email está faltando
        }
        
        result = validator.validate(incomplete_data, simple_schema)
        assert not result.is_valid
        assert any("email" in error.lower() for error in result.errors)

    def test_array_validation(self, validator):
        """Testa validação de um array de objetos"""
        array_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        }
        
        valid_data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
        
        result = validator.validate(valid_data, array_schema)
        assert result.is_valid

    @pytest.mark.parametrize("email,expected", [
        ("test@example.com", True),
        ("invalid-email", False),
        ("test@.com", False),
    ])
    def test_email_format(self, validator, email, expected):
        """Testa validação do formato de email"""
        assert validator._is_email(email) == expected

    def test_load_schema_from_file(self, validator, tmp_path):
        """Testa carregamento de schema a partir de arquivo"""
        schema_content = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        }
        
        # Cria arquivo temporário de schema
        schema_file = tmp_path / "test_schema.json"
        schema_file.write_text('{"type": "object", "properties": {"name": {"type": "string"}}}')
        
        loaded_schema = validator.load_schema(str(schema_file))
        assert loaded_schema["type"] == "object"
        assert "properties" in loaded_schema