from beerest import Assertions, Expect, Test

class TestDummyJSON(Test):
    def setup_method(self):
        super().setup_method()
        self.request.base_url = "https://dummyjson.com"
        
    def test_get_all_products(self):
        """Teste de GET para listar todos os produtos"""
        response = self.request.to("/products").get()
            
        Expect(response) \
            .status(200) \
            .is_json() \
            .body("total").greater_than(0) \
            .body("limit").equals(30) \
            .body("products").has_type("array")
            
    def test_get_single_product(self):
        """Teste de GET para um produto específico"""
        response = self.request.to("/products/1").get()
        
        Expect(response) \
            .status(200) \
            .body("id").equals(1) \
            .body().has_keys("title", "price", "description", "category") \
            .body("price").has_type("number")
            
    def test_search_products(self):
        """Teste de busca de produtos"""
        response = self.request \
            .to("/products/search") \
            .with_query({"q": "phone"}) \
            .get()
            
        Expect(response) \
            .status(200) \
            .body("products") \
            .satisfies(lambda products: all("phone" in product["title"].lower() for product in products))
            
    def test_add_product(self):
        """Teste de POST para adicionar um novo produto"""
        new_product = {
            "title": "Test Smartphone",
            "description": "A test smartphone",
            "price": 549.99,
            "category": "smartphones"
        }
        
        response = self.request \
            .to("/products/add") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(new_product) \
            .post()
            
        Expect(response) \
            .status(201) \
            .body("title").equals("Test Smartphone") \
            .body("price").equals(549.99)
            
    def test_update_product(self):
        """Teste de PUT para atualizar um produto"""
        updated_data = {
            "title": "Updated iPhone",
            "price": 1099.99
        }
        
        response = self.request \
            .to("/products/1") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(updated_data) \
            .put()
            
        Expect(response) \
            .status(200) \
            .body("title").equals("Updated iPhone") \
            .body("price").equals(1099.99)
            
    def test_delete_product(self):
        """Teste de DELETE de um produto"""
        response = self.request.to("/products/1").delete()
            
        Expect(response) \
            .status(200) \
            .body("isDeleted").equals(True) \
            .body("deletedOn").is_not_empty()
            
    def test_product_schema(self):
        """Teste de validação do schema de produto"""
        product_schema = {
            "type": "object",
            "required": ["id", "title", "description", "price", "category"],
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "price": {"type": "number"},
                "discountPercentage": {"type": "number"},
                "rating": {"type": "number"},
                "stock": {"type": "integer"},
                "brand": {"type": "string"},
                "category": {"type": "string"},
                "thumbnail": {"type": "string"},
                "images": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
        
        response = self.request.to("/products/1").get()
        
        Expect(response) \
            .status(200) \
            .body() \
            .matches_schema(product_schema)

    def test_get_product_categories(self):
        """Teste para listar todas as categorias de produtos"""
        response = self.request.to("/products/categories").get()
        
        Expect(response) \
            .status(200) \
            .body().has_type("array") \
            .body().is_not_empty()
            
    def test_get_products_by_category(self):
        """Teste para buscar produtos por categoria"""
        response = self.request.to("/products/category/smartphones").get()
        
        Expect(response) \
            .status(200) \
            .body("products") \
            .satisfies(lambda products: all(product["category"] == "smartphones" for product in products))
        
    def test_login_success(self):
        """Teste de login com sucesso e obtenção de token"""
        user = {
          "username":"emilys",
          "password":"emilyspass"
        }
          
        response = self.request \
            .to("/auth/login") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(user)\
            .post()
            
        Expect(response) \
            .status(200) \
            .body().has_keys("id", "username", "email", "firstName", "lastName", "token") \
            .body("token").is_not_empty() \
            .body("username").equals(user["username"])
            
    def test_login_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        invalid_user = {
            "username": "invalid_user",
            "password": "wrong_password"
        }
        
        response = self.request \
            .to("/auth/login") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(invalid_user) \
            .post()
            
        Expect(response) \
            .status(400) \
            .body("message").equals("Invalid credentials")

    def test_get_auth_user(self):
        """Teste para obter informações do usuário autenticado"""
        # Primeiro fazemos login para obter o token

        user = {
          "username":"emilys",
          "password":"emilyspass"
        }

        login_response = self.request \
            .to("/auth/login") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(user) \
            .post()
        
        token = login_response.json_data["accessToken"]
        
        # Agora fazemos a requisição autenticada
        response = self.request \
            .to("/auth/me") \
            .with_bearer_token(token) \
            .get()
            
        Expect(response) \
            .status(200) \
            .body("username").equals(user["username"]) \
            .body().has_keys("id", "username", "email", "firstName", "lastName")
            
    def test_get_auth_user_invalid_token(self):
        """Teste para obter informações do usuário com token inválido"""
        response = self.request \
            .to("/auth/me") \
            .with_bearer_token("invalid_token") \
            .get()
            
        Expect(response) \
            .status(401) \
            .body("message").equals("Invalid/Expired Token!")
            
    def test_auth_user_schema(self):
        """Teste de validação do schema do usuário autenticado"""

        user = {
          "username":"emilys",
          "password":"emilyspass"
        }

        user_schema = {
            "type": "object",
            "required": ["id", "username", "email", "firstName", "lastName"],
            "properties": {
                "id": {"type": "integer"},
                "username": {"type": "string"},
                "email": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "gender": {"type": "string"},
                "image": {"type": "string"},
                "token": {"type": "string"}
            }
        }
        
        # Fazemos login primeiro
        login_response = self.request \
            .to("/auth/login") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(user) \
            .post()
            
        token = login_response.json_data["accessToken"]
        
        # Validamos o schema da resposta do usuário autenticado
        response = self.request \
            .to("/auth/me") \
            .with_bearer_token(token) \
            .get()
            
        Expect(response) \
            .status(200) \
            .body() \
            .matches_schema(user_schema)

    def test_login_with_expiresInMins(self):
        """Teste de login especificando tempo de expiração do token"""
        login_data = {
            "username":"emilys",
            "password":"emilyspass",
            "expiresInMins": 60  # Token expira em 1 hora
        }
        
        response = self.request \
            .to("/auth/login") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(login_data) \
            .post()
            
        Expect(response) \
            .status(200) \
            .body("token").is_not_empty() \
            .body("username").equals(login_data["username"])