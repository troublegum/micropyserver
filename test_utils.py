import unittest
import utils


class TestUtils(unittest.TestCase):
    def test_get_request_method_should_return_get(self):
        request = "GET / HTTP/1.1\r\nHost: localhost"
        self.assertEqual(utils.get_request_method(request), "GET", "Should be GET")

    def test_get_request_method_should_return_post(self):
        request = "POST /post HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 0\r\n\r\n"
        self.assertEqual(utils.get_request_method(request), "POST", "Should be POST")

    def test_get_request_query_string_method_should_return_string(self):
        request = "GET /?param_one=one&param_two=two HTTP/1.1\r\nHost: localhost\r\n\r\n"
        self.assertEqual(utils.get_request_query_string(request), "param_one=one&param_two=two",
                         "Should be 'param_one=one&param_two=two'")

    def test_parse_query_string_method_should_return_two_params(self):
        query_string = "param_one=one&param_two=two"
        self.assertEqual(utils.parse_query_string(query_string), {"param_one": "one", "param_two": "two"},
                         "Should be result with two params")

    def test_get_request_query_params_method_should_return_two_params(self):
        request = "GET /?param_one=one&param_two=two HTTP/1.1\r\nHost: localhost\r\n\r\n"
        self.assertEqual(utils.get_request_query_params(request), {"param_one": "one", "param_two": "two"},
                         "Should be 'param_one=one&param_two=two'")

    def test_get_request_post_params_method_should_return_two_params(self):
        request = "POST /post HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nparam_one=one&param_two=two"
        self.assertEqual(utils.get_request_post_params(request), {"param_one": "one", "param_two": "two"},
                         "Should be 'param_one=one&param_two=two'")

    def test_unquote_method_should_return_empty_string(self):
        self.assertEqual(utils.unquote(""), "", "Should be empty string")

    def test_unquote_method_should_return_string(self):
        self.assertEqual(utils.unquote("param"), "param", "Should be 'param'")

    def test_unquote_method_should_return_unquoted_string(self):
        self.assertEqual(utils.unquote(
            "%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%20%D0%B8%20%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%25"),
                         "параметр и значение %",
                         "Should be 'параметр и значение %'")


if __name__ == "__main__":
    unittest.main()
