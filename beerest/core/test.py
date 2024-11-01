from .request import Request

class Test:
    def setup_method(self):
        self.request = Request()

    def teardown_method(self):
        pass