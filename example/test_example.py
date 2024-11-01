from beerest import Assertions, Expect, Test


class TestExample(Test):
    def setup_method(self):
        super().setup_method()
        self.request.base_url = "https://jsonplaceholder.typicode.com"
        
    def test_get_posts(self):
        """Teste básico de GET request"""
        response = self.request.to("/posts").get()
        
        Expect(response) \
            .status(200) \
            .is_json() \
            .body() \
            .has_length(100)
            
    def test_get_single_post(self):
        """Teste com path parameters e verificação de conteúdo"""
        response = self.request.to("/posts/1").get()
        
        Expect(response) \
            .status(200) \
            .body("title").contains("sunt") \
            .body("userId").equals(1)
            
    def test_create_post(self):
        """Teste de POST com payload"""
        new_post = {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
        
        response = self.request \
            .to("/posts") \
            .with_headers({"Content-Type": "application/json"}) \
            .with_body(new_post) \
            .post()
            
        Expect(response) \
            .status(201) \
            .body("title").equals("Test Post") \
            .body("id").satisfies(lambda x: isinstance(x, int))
            
    def test_get_with_query_params(self):
        """Teste com query parameters"""
        response = self.request \
            .to("/posts") \
            .with_query({"userId": 1}) \
            .get()
            
        Expect(response) \
            .status(200) \
            .body() \
            .satisfies(lambda posts: all(post["userId"] == 1 for post in posts))
            
    def test_response_time(self):
        """Teste de performance"""
        response = self.request.to("/posts/1").get()
        
        Expect(response) \
            .time() \
            .less_than(1000)  # menos que 1000ms
            
    def test_headers(self):
        """Teste de headers"""
        response = self.request.to("/posts/1").get()
        
        Expect(response) \
            .header("content-type") \
            .contains("application/json")
            
    def test_error_handling(self):
        """Teste de tratamento de erro"""
        response = self.request.to("/posts/999").get()
        
        Expect(response) \
            .status(404)
            
    def test_complex_assertions(self):
        """Teste com múltiplas assertions complexas"""
        response = self.request.to("/posts/1").get()
        
        Expect(response) \
            .status(200) \
            .body("id").equals(1) \
            .body("title").matches(r"^[a-zA-Z\s]+$") \
            .body().has_keys("id", "title", "body", "userId") \
            .time().less_than(2000)
            
        # Usando assertions tradicionais junto com Expect
        Assertions.assertEqual(response.status_code, 200)
        Assertions.assertTrue(len(response.json_data["title"]) > 0)

    def test_with_timeout(self):
        """Teste com timeout customizado"""
        response = self.request \
            .to("/posts/1") \
            .with_timeout(2.0) \
            .get()
            
        Expect(response) \
            .status(200) \
            .time() \
            .less_than(2000)