"""Example service module demonstrating HTTP client usage with requests."""

import requests
from typing import Dict, Any, Optional


class ExampleService:
    """Example service class that demonstrates HTTP API interactions.
    
    This service provides methods to interact with a REST API using the requests library.
    It includes error handling and demonstrates common HTTP operations.
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """Initialize the ExampleService.
        
        Args:
            base_url: The base URL for the API endpoint
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'ExampleService/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def get_with_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a GET request to {base_url}/get with optional parameters.
        
        Args:
            params: Optional dictionary of query parameters
            
        Returns:
            Dict containing the JSON response
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}/get"
        
        try:
            response = self.session.get(
                url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"GET request to {url} failed: {str(e)}") from e
    
    def ping(self) -> Dict[str, Any]:
        """Simple ping method that calls /get endpoint and returns basic info.
        
        Returns:
            Dict containing status code and response headers
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}/get"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'success': True,
                'message': f'Successfully connected to {url}'
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'status': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                'headers': dict(getattr(e.response, 'headers', {})) if hasattr(e, 'response') and e.response else {},
                'success': False,
                'message': f'Connection to {url} failed: {str(e)}'
            }
    
    def close(self):
        """Close the session and cleanup resources."""
        if hasattr(self, 'session'):
            self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
