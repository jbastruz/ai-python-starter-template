"""Tests for the ExampleService module."""
import pytest
from unittest.mock import Mock, patch
import requests
from requests import RequestException

from src.ai_starter.services.example_service import ExampleService


class TestExampleService:
    """Test class for ExampleService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = ExampleService(base_url="https://httpbin.org", timeout=30)

    def teardown_method(self):
        """Clean up after tests."""
        self.service.close()

    @patch('requests.Session.get')
    def test_ping_success(self, mock_get):
        """Test ping method with successful 200 response."""
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the method
        result = self.service.ping()

        # Assertions
        assert result['success'] is True
        assert result['status'] == 200
        assert result['headers']['Content-Type'] == 'application/json'
        assert 'Successfully connected to' in result['message']
        mock_get.assert_called_once_with('https://httpbin.org/get', timeout=30)

    @patch('requests.Session.get')
    def test_get_with_params_success(self, mock_get):
        """Test get_with_params method with successful response."""
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'args': {'param1': 'value1', 'param2': 'value2'},
            'url': 'https://httpbin.org/get?param1=value1&param2=value2'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test parameters
        params = {'param1': 'value1', 'param2': 'value2'}

        # Call the method
        result = self.service.get_with_params(params=params)

        # Assertions
        assert result['args'] == params
        assert 'httpbin.org' in result['url']
        mock_get.assert_called_once_with(
            'https://httpbin.org/get',
            params=params,
            timeout=30
        )

    @patch('requests.Session.get')
    def test_get_with_params_request_exception(self, mock_get):
        """Test get_with_params method raising RequestException on failure."""
        # Mock to raise RequestException
        mock_get.side_effect = RequestException("Connection error")

        # Test parameters
        params = {'test': 'value'}

        # Call the method and expect exception
        with pytest.raises(RequestException) as exc_info:
            self.service.get_with_params(params=params)

        # Assertions
        assert "GET request to https://httpbin.org/get failed" in str(exc_info.value)
        assert "Connection error" in str(exc_info.value)
        mock_get.assert_called_once_with(
            'https://httpbin.org/get',
            params=params,
            timeout=30
        )

    @patch('requests.Session.get')
    def test_ping_handles_exception_gracefully(self, mock_get):
        """Test that ping method handles exceptions gracefully and returns error info."""
        # Mock to raise RequestException
        mock_get.side_effect = RequestException("Network timeout")

        # Call the method
        result = self.service.ping()

        # Assertions
        assert result['success'] is False
        assert result['status'] is None
        assert 'Connection to https://httpbin.org/get failed' in result['message']
        assert 'Network timeout' in result['message']
        mock_get.assert_called_once_with('https://httpbin.org/get', timeout=30)

    def test_context_manager(self):
        """Test that ExampleService works as a context manager."""
        with ExampleService(base_url="https://httpbin.org") as service:
            assert service.base_url == "https://httpbin.org"
            assert hasattr(service, 'session')

    def test_initialization(self):
        """Test ExampleService initialization."""
        service = ExampleService(base_url="https://api.example.com/", timeout=60)
        
        assert service.base_url == "https://api.example.com"
        assert service.timeout == 60
        assert service.session.headers['User-Agent'] == 'ExampleService/1.0'
        assert service.session.headers['Accept'] == 'application/json'
        assert service.session.headers['Content-Type'] == 'application/json'
        
        service.close()
