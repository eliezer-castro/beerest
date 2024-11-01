from beerest.core.response import Response

class TestResponse:
    def test_response_creation(self):
        response = Response(
            status_code=200,
            headers={"Content-Type": "application/json"},
            json_data={"data": "test"},
            text='{"data": "test"}',
            elapsed_time=100.0
        )
        
        assert response.status_code == 200
        assert response.headers == {"Content-Type": "application/json"}
        assert response.json_data == {"data": "test"}
        assert response.text == '{"data": "test"}'
        assert response.elapsed_time == 100.0