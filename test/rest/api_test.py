import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )
        
    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/3/4"

        with patch('urllib.request.urlopen') as mock_urlopen:
            # Simulate successful response with expected data
            mock_response = unittest.mock.MagicMock()
            mock_response.status = http.client.OK
            mock_response.read.return_value = b'{"result": 12}'  # JSON response
            mock_urlopen.return_value = mock_response

            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")

            # Decode and verify JSON response
            data = json.loads(response.read().decode())
            self.assertEqual(data['result'], 12, "ERROR MULTIPLY")

    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/5/0"

        with patch('urllib.request.urlopen') as mock_urlopen:
            # Simulate error response (406) with expected message
            mock_response = unittest.mock.MagicMock()
            mock_response.status = http.client.NOT_ACCEPTABLE
            mock_response.read.return_value = b'{"error": "Division by zero is not allowed"}'  # JSON response
            mock_urlopen.return_value = mock_response

            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.assertEqual(response.status, http.client.NOT_ACCEPTABLE, f"Error en la petición API a {url}")

            # Decode and verify JSON response for error message
            data = json.loads(response.read().decode())
            self.assertEqual(data['error'], "Division by zero is not allowed", "ERROR DIVIDE BY ZERO")

    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/10/15"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "150", "ERROR ADD"
        )

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/10/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "5", "ERROR ADD"
        )

    def test_api_dividezero(self):
        url = f"{BASE_URL}/calc/divide/10/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, 406, f"Error en la petición API a {url}"
        )
    
    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
