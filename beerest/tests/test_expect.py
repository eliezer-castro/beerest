import pytest
from beerest.core.expect import Expect
from beerest.core.response import Response

class TestExpect:
    def setup_method(self):
        self.response = Response(
            status_code=200,
            headers={"Content-Type": "application/json"},
            json_data={"data": "test"},
            text='{"data": "test"}',
            elapsed_time=100.0
        )
        self.expect = Expect(self.response)
        
    def test_status_check(self):
        self.expect.status(200)
        assert self.expect.all_passed()
        
    def test_body_check(self):
        self.expect.body("$.data").equals("test")
        assert self.expect.all_passed()
        
    def test_header_check(self):
        self.expect.header("Content-Type").equals("application/json")
        assert self.expect.all_passed()
        
    def test_time_check(self):
        self.expect.time().less_than(1000)
        assert self.expect.all_passed()
        
    def test_multiple_checks(self):
        self.expect\
            .status(200)\
            .body("$.data").equals("test")\
            .header("Content-Type").contains("json")
        assert self.expect.all_passed()

    def test_failed_check(self):
        with pytest.raises(AssertionError):
            self.expect.status().equals(404)