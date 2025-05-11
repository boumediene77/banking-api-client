"""Client for interacting with the Banking API."""
import aiohttp
import asyncio
import requests
import json
from typing import Dict, List, Optional, Union, Any

from .exceptions import BankingAPIError, AuthenticationError, ResourceNotFoundError
from .utils import is_valid_url


class BankingAPIClient:
    """Client for interacting with the Banking API."""
    
    def __init__(self, base_url: str, username: str, password: str, use_async: bool = False):
        """
        Initialize the Banking API client.
        
        Args:
            base_url: Base URL of the API
            username: Username for authentication
            password: Password for authentication
            use_async: Whether to use async client (default: False)
        """
        # URL validation
        if not is_valid_url(base_url):
            raise ValueError("Invalid URL format. Must begin with http:// or https://")
            
        self.base_url = base_url.rstrip('/')
        self._username = username  
        self._password = password  
        self.use_async = use_async
        self.session = None
        self.token = None
        self.token_type = "bearer"  
    
    def __enter__(self):
        """Context manager entry."""
        if not self.use_async:
            self.session = requests.Session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.session and not self.use_async:
            self.session.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        if self.use_async:
            self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session and self.use_async:
            await self.session.close()
        
    def authenticate(self) -> str:
        """
        Authenticate with the API and get token.
        
        Returns:
            Authentication token
            
        Raises:
            AuthenticationError: If authentication fails
            BankingAPIError: For other API errors
        """
        if self.use_async:
            raise RuntimeError("Use authenticate_async for async mode")
        
        auth_url = f"{self.base_url}/oauth/token"
        auth_data = {
            "username": self._username,
            "password": self._password,
            "scope": "stet"
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = self.session.post(auth_url, data=auth_data, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.token = data.get("access_token")
            self.token_type = data.get("token_type", "bearer")
            return self.token
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication failed: Invalid credentials") from e
            else:
                raise BankingAPIError(f"API Error: {e}") from e
        except requests.exceptions.ConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}") from e
        except requests.exceptions.Timeout as e:
            raise BankingAPIError(f"Request timeout: {e}") from e
        except requests.exceptions.RequestException as e:
            raise BankingAPIError(f"Request error: {e}") from e
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}") from e
        
    async def authenticate_async(self) -> str:
        """
        Authenticate with the API asynchronously and get token.
        
        Returns:
            Authentication token
            
        Raises:
            AuthenticationError: If authentication fails
            BankingAPIError: For other API errors
        """
        if not self.use_async:
            raise RuntimeError("Use authenticate for sync mode")
        
        auth_url = f"{self.base_url}/oauth/token"
        auth_data = {
            "username": self._username,
            "password": self._password,
            "scope": "stet"
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            async with self.session.post(auth_url, data=auth_data, headers=headers) as response:
                if response.status == 401:
                    raise AuthenticationError("Authentication failed: Invalid credentials")
                
                response.raise_for_status()
                data = await response.json()
                self.token = data.get("access_token")
                self.token_type = data.get("token_type", "bearer")
                return self.token
                
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {e.request_info.url}") from e
            else:
                raise BankingAPIError(f"API Error: {e}") from e
        except aiohttp.ClientConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}") from e
        except aiohttp.ClientError as e:
            raise BankingAPIError(f"Request error: {e}") from e
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}") from e
        
    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for API requests.
        
        Returns:
            Dictionary of headers
        """
        if not self.token:
            raise ValueError("Not authenticated. Call authenticate() first")
        
        token_type = getattr(self, "token_type", "bearer")
        
        return {
            "Authorization": f"{token_type} {self.token}",
            "Content-Type": "application/json"
        }
    
    def _handle_request_error(self, e, endpoint: str):
        """
        Handle request errors.
        
        Args:
            e: The exception
            endpoint: The API endpoint being accessed
            
        Raises:
            ResourceNotFoundError: For 404 errors
            AuthenticationError: For 401 errors
            BankingAPIError: For other errors
        """
        if isinstance(e, requests.exceptions.HTTPError):
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Resource not found: {endpoint}")
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication error: Token might be expired")
            elif e.response.status_code == 403:
                raise BankingAPIError(f"Access denied to {endpoint}")
            else:
                raise BankingAPIError(f"API Error: {e}")
        elif isinstance(e, requests.exceptions.ConnectionError):
            raise BankingAPIError(f"Connection error: {e}")
        elif isinstance(e, requests.exceptions.Timeout):
            raise BankingAPIError(f"Request timeout: {e}")
        elif isinstance(e, requests.exceptions.RequestException):
            raise BankingAPIError(f"Request error: {e}")
        elif isinstance(e, json.JSONDecodeError):
            raise BankingAPIError(f"Invalid JSON response: {e}")
        else:
            raise BankingAPIError(f"Unexpected error: {e}")
        
    def get_identity(self) -> Dict[str, Any]:
        """
        Get user identity information.
        
        Returns:
            Dictionary containing identity information
            
        Raises:
            ResourceNotFoundError: If identity resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if self.use_async:
            raise RuntimeError("Use get_identity_async for async mode")
        
        url = f"{self.base_url}/stet/identity"
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, "identity")
        
    async def get_identity_async(self) -> Dict[str, Any]:
        """
        Get user identity information asynchronously.
        
        Returns:
            Dictionary containing identity information
            
        Raises:
            ResourceNotFoundError: If identity resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if not self.use_async:
            raise RuntimeError("Use get_identity for sync mode")
        
        url = f"{self.base_url}/stet/identity"
        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {url}")
            elif e.status == 401:
                raise AuthenticationError("Authentication error: Token might be expired")
            else:
                raise BankingAPIError(f"API Error: {e}")
        except aiohttp.ClientConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}")
        except aiohttp.ClientError as e:
            raise BankingAPIError(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}")
        
    def get_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all accounts.
        
        Returns:
            List of accounts
            
        Raises:
            ResourceNotFoundError: If accounts resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if self.use_async:
            raise RuntimeError("Use get_accounts_async for async mode")
        
        url = f"{self.base_url}/stet/account"
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, "accounts")
    
    async def get_accounts_async(self) -> List[Dict[str, Any]]:
        """
        Get all accounts asynchronously.
        
        Returns:
            List of accounts
            
        Raises:
            ResourceNotFoundError: If accounts resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if not self.use_async:
            raise RuntimeError("Use get_accounts for sync mode")
        
        url = f"{self.base_url}/stet/account"
        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {url}")
            elif e.status == 401:
                raise AuthenticationError("Authentication error: Token might be expired")
            else:
                raise BankingAPIError(f"API Error: {e}")
        except aiohttp.ClientConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}")
        except aiohttp.ClientError as e:
            raise BankingAPIError(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}")
    
    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get specific account by ID.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account details
            
        Raises:
            ResourceNotFoundError: If account resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if self.use_async:
            raise RuntimeError("Use get_account_async for async mode")
        
        url = f"{self.base_url}/stet/account/{account_id}"
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"account/{account_id}")
    
    async def get_account_async(self, account_id: str) -> Dict[str, Any]:
        """
        Get specific account by ID asynchronously.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account details
            
        Raises:
            ResourceNotFoundError: If account resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if not self.use_async:
            raise RuntimeError("Use get_account for sync mode")
        
        url = f"{self.base_url}/stet/account/{account_id}"
        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {url}")
            elif e.status == 401:
                raise AuthenticationError("Authentication error: Token might be expired")
            else:
                raise BankingAPIError(f"API Error: {e}")
        except aiohttp.ClientConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}")
        except aiohttp.ClientError as e:
            raise BankingAPIError(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}")
    
    def get_balances(self, account_id: str) -> Dict[str, Any]:
        """
        Get balances for an account.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account balances
            
        Raises:
            ResourceNotFoundError: If balances resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if self.use_async:
            raise RuntimeError("Use get_balances_async for async mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/balance"
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"account/{account_id}/balance")
    
    async def get_balances_async(self, account_id: str) -> Dict[str, Any]:
        """
        Get balances for an account asynchronously.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account balances
            
        Raises:
            ResourceNotFoundError: If balances resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if not self.use_async:
            raise RuntimeError("Use get_balances for sync mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/balance"
        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {url}")
            elif e.status == 401:
                raise AuthenticationError("Authentication error: Token might be expired")
            else:
                raise BankingAPIError(f"API Error: {e}")
        except aiohttp.ClientConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}")
        except aiohttp.ClientError as e:
            raise BankingAPIError(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}")
    
    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Get transactions for an account.
        
        Args:
            account_id: Account ID
        
        Returns:
            List of transactions
            
        Raises:
            ResourceNotFoundError: If transactions resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if self.use_async:
            raise RuntimeError("Use get_transactions_async for async mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/transaction"
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"account/{account_id}/transaction")
    
    async def get_transactions_async(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Get transactions for an account asynchronously.
        
        Args:
            account_id: Account ID
        
        Returns:
            List of transactions
            
        Raises:
            ResourceNotFoundError: If transactions resource not found
            AuthenticationError: If authentication error occurs
            BankingAPIError: For other API errors
        """
        if not self.use_async:
            raise RuntimeError("Use get_transactions for sync mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/transaction"
        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Resource not found: {url}")
            elif e.status == 401:
                raise AuthenticationError("Authentication error: Token might be expired")
            else:
                raise BankingAPIError(f"API Error: {e}")
        except aiohttp.ClientConnectionError as e:
            raise BankingAPIError(f"Connection error: {e}")
        except aiohttp.ClientError as e:
            raise BankingAPIError(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise BankingAPIError(f"Invalid JSON response: {e}")