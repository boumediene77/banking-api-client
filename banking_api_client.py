"""
Banking API Client

A library to consume the banking API available at https://dsp2-technical-test.iliad78.net
"""
import aiohttp
import asyncio
import requests
from typing import Dict, List, Optional, Union, Any
import json


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
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.use_async = use_async
        self.session = None
        self.token = None
        self.token_type = "bearer"  # Default value
    
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
        """
        if self.use_async:
            raise RuntimeError("Use authenticate_async for async mode")
        
        auth_url = f"{self.base_url}/oauth/token"
        auth_data = {
            "username": self.username,
            "password": self.password,
            "scope": "stet"
        }
        
        # Utilisation de data au lieu de json et ajout du header Content-Type approprié
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.post(auth_url, data=auth_data, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        # Stockage de l'access_token et du token_type
        self.token = data.get("access_token")
        self.token_type = data.get("token_type", "bearer")
        return self.token
        
    async def authenticate_async(self) -> str:
        """
        Authenticate with the API asynchronously and get token.
        
        Returns:
            Authentication token
        """
        if not self.use_async:
            raise RuntimeError("Use authenticate for sync mode")
        
        auth_url = f"{self.base_url}/oauth/token"
        auth_data = {
            "username": self.username,
            "password": self.password,
            "scope": "stet"
        }
        
        # Utilisation de data au lieu de json et ajout du header Content-Type approprié
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with self.session.post(auth_url, data=auth_data, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            # Stockage de l'access_token et du token_type
            self.token = data.get("access_token")
            self.token_type = data.get("token_type", "bearer")
            return self.token
        
    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for API requests.
        
        Returns:
            Dictionary of headers
        """
        if not self.token:
            raise ValueError("Not authenticated. Call authenticate() first")
        
        # Utiliser le token_type stocké, avec "bearer" comme valeur par défaut
        token_type = getattr(self, "token_type", "bearer")
        
        return {
            "Authorization": f"{token_type} {self.token}",
            "Content-Type": "application/json"
        }
        
    def get_identity(self) -> Dict[str, Any]:
        """
        Get user identity information.
        
        Returns:
            Dictionary containing identity information
        """
        if self.use_async:
            raise RuntimeError("Use get_identity_async for async mode")
        
        # Correction de l'URL : /stet/identity au lieu de /identity
        url = f"{self.base_url}/stet/identity"
        response = self.session.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
        
    async def get_identity_async(self) -> Dict[str, Any]:
        """
        Get user identity information asynchronously.
        
        Returns:
            Dictionary containing identity information
        """
        if not self.use_async:
            raise RuntimeError("Use get_identity for sync mode")
        
        # Correction de l'URL : /stet/identity au lieu de /identity
        url = f"{self.base_url}/stet/identity"
        async with self.session.get(url, headers=self._get_headers()) as response:
            response.raise_for_status()
            return await response.json()
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all accounts.
        
        Returns:
            List of accounts
        """
        if self.use_async:
            raise RuntimeError("Use get_accounts_async for async mode")
        
        url = f"{self.base_url}/stet/account"
        response = self.session.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    async def get_accounts_async(self) -> List[Dict[str, Any]]:
        """
        Get all accounts asynchronously.
        
        Returns:
            List of accounts
        """
        if not self.use_async:
            raise RuntimeError("Use get_accounts for sync mode")
        
        url = f"{self.base_url}/stet/account"
        async with self.session.get(url, headers=self._get_headers()) as response:
            response.raise_for_status()
            return await response.json()
    
    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get specific account by ID.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account details
        """
        if self.use_async:
            raise RuntimeError("Use get_account_async for async mode")
        
        url = f"{self.base_url}/stet/account/{account_id}"
        response = self.session.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    async def get_account_async(self, account_id: str) -> Dict[str, Any]:
        """
        Get specific account by ID asynchronously.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account details
        """
        if not self.use_async:
            raise RuntimeError("Use get_account for sync mode")
        
        url = f"{self.base_url}/stet/account/{account_id}"
        async with self.session.get(url, headers=self._get_headers()) as response:
            response.raise_for_status()
            return await response.json()
    
    def get_balances(self, account_id: str) -> Dict[str, Any]:
        """
        Get balances for an account.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account balances
        """
        if self.use_async:
            raise RuntimeError("Use get_balances_async for async mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/balance"
        response = self.session.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    async def get_balances_async(self, account_id: str) -> Dict[str, Any]:
        """
        Get balances for an account asynchronously.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account balances
        """
        if not self.use_async:
            raise RuntimeError("Use get_balances for sync mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/balance"
        async with self.session.get(url, headers=self._get_headers()) as response:
            response.raise_for_status()
            return await response.json()
    
    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Get transactions for an account.
        
        Args:
            account_id: Account ID
        
        Returns:
            List of transactions
        """
        if self.use_async:
            raise RuntimeError("Use get_transactions_async for async mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/transaction"
        response = self.session.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    async def get_transactions_async(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Get transactions for an account asynchronously.
        
        Args:
            account_id: Account ID
        
        Returns:
            List of transactions
        """
        if not self.use_async:
            raise RuntimeError("Use get_transactions for sync mode")
        
        url = f"{self.base_url}/stet/account/{account_id}/transaction"
        async with self.session.get(url, headers=self._get_headers()) as response:
            response.raise_for_status()
            return await response.json()
    



class BankingDataCollector:
    """Utility for collecting all data from the Banking API."""
    
    def __init__(self, client: BankingAPIClient):
        """
        Initialize the data collector.
        
        Args:
            client: Authenticated BankingAPIClient instance
        """
        self.client = client
    
    def collect_all_data(self) -> Dict[str, Any]:
        """
        Collect all data from the API.
        
        Returns:
            Dictionary containing all data (identity, accounts, balances, transactions)
        """
        if self.client.use_async:
            raise RuntimeError("Use collect_all_data_async for async mode")
        
        # Get identity
        identity = self.client.get_identity()
        
        # Get accounts
        accounts = self.client.get_accounts()
        
        # Get balances and transactions for each account
        for account in accounts:
            account_id = account.get("id")
            account["balances"] = self.client.get_balances(account_id)
            account["transactions"] = self.client.get_transactions(account_id)
        
        return {
            "identity": identity,
            "accounts": accounts
        }
    
    async def collect_all_data_async(self) -> Dict[str, Any]:
        """
        Collect all data from the API asynchronously.
        
        Returns:
            Dictionary containing all data (identity, accounts, balances, transactions)
        """
        if not self.client.use_async:
            raise RuntimeError("Use collect_all_data for sync mode")
        
        # Get identity
        identity = await self.client.get_identity_async()
        
        # Get accounts
        accounts = await self.client.get_accounts_async()
        
        # Problem: Get balances and transactions for each account
        # Fix: Instead of parallel calls which might cause token issues,
        # do them sequentially to ensure token validity
        for account in accounts:
            account_id = account.get("id")
            # Get balances and transactions sequentially for each account
            account["balances"] = await self.client.get_balances_async(account_id)
            account["transactions"] = await self.client.get_transactions_async(account_id)
        
        return {
            "identity": identity,
            "accounts": accounts
        }
    
