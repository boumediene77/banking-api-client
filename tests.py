"""
Tests for the Banking API Client.
"""
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import aiohttp
import json
from banking_api_client import BankingAPIClient, BankingDataCollector


class TestBankingAPIClient(unittest.TestCase):
    """Tests for the BankingAPIClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://dsp2-technical-test.iliad78.net"
        self.username = "mdupuis"
        self.password = "111111"
        
        # Sample response data
        self.token_data = {
            "access_token": "fake-token-12345",
            "token_type": "bearer"
        }
        self.identity_data = {
            "id": "user_TIMLjQYdrPd07YVuuLdK3Dvw",
            "prefix": "MIST",
            "first_name": "Maurice",
            "last_name": "Dupuis",
            "date_of_birth": "1970-05-06"
        }
        self.accounts_data = [
            {
                "id": "acct_Ms99YLcC2LETpC4KKK7VcjPY",
                "name": "Compte Carte",
                "type": "CACC",
                "usage": "PRIV",
                "iban": "FR7610096000505687604467V48",
                "currency": "EUR"
            },
            {
                "id": "acct_ruguKBdKe3Tr3e3iLsPwieqB",
                "name": "Compte Courant",
                "type": "CACC",
                "usage": "PRIV",
                "iban": "FR7610096000501234567890123",
                "currency": "EUR"
            }
        ]
        self.balances_data = [
            {
                "amount": 66871,
                "currency": "EUR"
            }
        ]
        self.transactions_data = [
            {
                "id": "tx123",
                "amount": 100.50,
                "currency": "EUR",
                "description": "Supermarket",
                "date": "2023-01-01T10:00:00Z"
            },
            {
                "id": "tx456",
                "amount": -50.25,
                "currency": "EUR",
                "description": "ATM Withdrawal",
                "date": "2023-01-02T14:30:00Z"
            }
        ]
    
    @patch('requests.Session')
    def test_authenticate(self, mock_session):
        """Test authentication."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.token_data
        mock_session.return_value.post.return_value = mock_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.session = mock_session.return_value
        
        token = client.authenticate()
        
        # Assertions
        self.assertEqual(token, "fake-token-12345")
        mock_session.return_value.post.assert_called_once_with(
            f"{self.base_url}/oauth/token",
            data={"username": self.username, "password": self.password, "scope": "stet"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    
    @patch('requests.Session')
    def test_get_identity(self, mock_session):
        """Test getting identity."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.identity_data
        mock_session.return_value.get.return_value = mock_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.session = mock_session.return_value
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        identity = client.get_identity()
        
        # Assertions
        self.assertEqual(identity, self.identity_data)
        mock_session.return_value.get.assert_called_once_with(
            f"{self.base_url}/stet/identity",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
    
    @patch('requests.Session')
    def test_get_accounts(self, mock_session):
        """Test getting accounts."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.accounts_data
        mock_session.return_value.get.return_value = mock_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.session = mock_session.return_value
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        accounts = client.get_accounts()
        
        # Assertions
        self.assertEqual(accounts, self.accounts_data)
        mock_session.return_value.get.assert_called_once_with(
            f"{self.base_url}/stet/account",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
    
    @patch('requests.Session')
    def test_get_balances(self, mock_session):
        """Test getting balances."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.balances_data
        mock_session.return_value.get.return_value = mock_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.session = mock_session.return_value
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        balances = client.get_balances("acct_Ms99YLcC2LETpC4KKK7VcjPY")
        
        # Assertions
        self.assertEqual(balances, self.balances_data)
        mock_session.return_value.get.assert_called_once_with(
            f"{self.base_url}/stet/account/acct_Ms99YLcC2LETpC4KKK7VcjPY/balance",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
    
    @patch('requests.Session')
    def test_get_transactions(self, mock_session):
        """Test getting transactions."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.transactions_data
        mock_session.return_value.get.return_value = mock_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.session = mock_session.return_value
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        transactions = client.get_transactions("acct_Ms99YLcC2LETpC4KKK7VcjPY")
        
        # Assertions
        self.assertEqual(transactions, self.transactions_data)
        mock_session.return_value.get.assert_called_once_with(
            f"{self.base_url}/stet/account/acct_Ms99YLcC2LETpC4KKK7VcjPY/transaction",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
    
    @patch('requests.Session')
    def test_data_collector(self, mock_session):
        """Test the data collector."""
        # Mock responses
        mock_responses = {
            f"{self.base_url}/stet/identity": MagicMock(json=lambda: self.identity_data),
            f"{self.base_url}/stet/account": MagicMock(json=lambda: self.accounts_data),
            f"{self.base_url}/stet/account/acct_Ms99YLcC2LETpC4KKK7VcjPY/balance": MagicMock(json=lambda: self.balances_data),
            f"{self.base_url}/stet/account/acct_ruguKBdKe3Tr3e3iLsPwieqB/balance": MagicMock(json=lambda: self.balances_data),
            f"{self.base_url}/stet/account/acct_Ms99YLcC2LETpC4KKK7VcjPY/transaction": MagicMock(json=lambda: self.transactions_data),
            f"{self.base_url}/stet/account/acct_ruguKBdKe3Tr3e3iLsPwieqB/transaction": MagicMock(json=lambda: self.transactions_data),
        }
        
        def side_effect(url, headers):
            return mock_responses[url]
        
        mock_session.return_value.get.side_effect = side_effect
        
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.session = mock_session.return_value
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        collector = BankingDataCollector(client)
        data = collector.collect_all_data()
        
        # Assertions
        self.assertEqual(data["identity"], self.identity_data)
        self.assertEqual(len(data["accounts"]), 2)
        self.assertEqual(data["accounts"][0]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][0]["transactions"], self.transactions_data)
        self.assertEqual(data["accounts"][1]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][1]["transactions"], self.transactions_data)


# Patching the aiohttp.ClientSession methods directly for async tests
class TestAsyncBankingAPIClient(unittest.IsolatedAsyncioTestCase):
    """Tests for the asynchronous BankingAPIClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://dsp2-technical-test.iliad78.net"
        self.username = "agribard"
        self.password = "222222"
        
        # Sample response data
        self.token_data = {
            "access_token": "fake-token-12345",
            "token_type": "bearer"
        }
        self.identity_data = {
            "id": "user456",
            "prefix": "MIST",
            "first_name": "Antoinette",
            "last_name": "Gribard",
            "date_of_birth": "1980-02-15"
        }
        self.accounts_data = [
            {
                "id": "acct_789",
                "name": "Compte Professionnel",
                "type": "CACC",
                "usage": "PRIV",
                "iban": "FR7610096000507890123456789",
                "currency": "EUR"
            },
            {
                "id": "acct_012",
                "name": "Compte Épargne",
                "type": "SVGS",
                "usage": "PRIV",
                "iban": "FR7610096000501234567890987",
                "currency": "EUR"
            }
        ]
        self.balances_data = [
            {
                "amount": 25000,
                "currency": "EUR"
            }
        ]
        self.transactions_data = [
            {
                "id": "tx789",
                "amount": 200.00,
                "currency": "EUR",
                "description": "Rent",
                "date": "2023-01-05T09:00:00Z"
            },
            {
                "id": "tx012",
                "amount": -75.50,
                "currency": "EUR",
                "description": "Restaurant",
                "date": "2023-01-06T19:30:00Z"
            }
        ]
    
    async def asyncSetUp(self):
        """Set up async test fixtures."""
        pass
    
    @patch('aiohttp.ClientSession.post')
    async def test_authenticate_async(self, mock_post):
        """Test async authentication."""
        # Create a mock context manager response
        cm_response = AsyncMock()
        mock_response = cm_response.__aenter__.return_value
        mock_response.json.return_value = self.token_data
        mock_post.return_value = cm_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        client.session = aiohttp.ClientSession()
        
        token = await client.authenticate_async()
        
        # Assertions
        self.assertEqual(token, "fake-token-12345")
        mock_post.assert_called_once_with(
            f"{self.base_url}/oauth/token",
            data={"username": self.username, "password": self.password, "scope": "stet"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Clean up
        if client.session and not client.session.closed:
            await client.session.close()
    
    @patch('aiohttp.ClientSession.get')
    async def test_get_identity_async(self, mock_get):
        """Test getting identity asynchronously."""
        # Create a mock context manager response
        cm_response = AsyncMock()
        mock_response = cm_response.__aenter__.return_value
        mock_response.json.return_value = self.identity_data
        mock_get.return_value = cm_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        client.session = aiohttp.ClientSession()
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        identity = await client.get_identity_async()
        
        # Assertions
        self.assertEqual(identity, self.identity_data)
        mock_get.assert_called_once_with(
            f"{self.base_url}/stet/identity",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
        
        # Clean up
        if client.session and not client.session.closed:
            await client.session.close()
    
    @patch('aiohttp.ClientSession.get')
    async def test_get_accounts_async(self, mock_get):
        """Test getting accounts asynchronously."""
        # Create a mock context manager response
        cm_response = AsyncMock()
        mock_response = cm_response.__aenter__.return_value
        mock_response.json.return_value = self.accounts_data
        mock_get.return_value = cm_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        client.session = aiohttp.ClientSession()
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        accounts = await client.get_accounts_async()
        
        # Assertions
        self.assertEqual(accounts, self.accounts_data)
        mock_get.assert_called_once_with(
            f"{self.base_url}/stet/account",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
        
        # Clean up
        if client.session and not client.session.closed:
            await client.session.close()
    
    @patch('aiohttp.ClientSession.get')
    async def test_get_balances_async(self, mock_get):
        """Test getting balances asynchronously."""
        # Create a mock context manager response
        cm_response = AsyncMock()
        mock_response = cm_response.__aenter__.return_value
        mock_response.json.return_value = self.balances_data
        mock_get.return_value = cm_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        client.session = aiohttp.ClientSession()
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        balances = await client.get_balances_async("acct_789")
        
        # Assertions
        self.assertEqual(balances, self.balances_data)
        mock_get.assert_called_once_with(
            f"{self.base_url}/stet/account/acct_789/balance",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
        
        # Clean up
        if client.session and not client.session.closed:
            await client.session.close()
    
    @patch('aiohttp.ClientSession.get')
    async def test_get_transactions_async(self, mock_get):
        """Test getting transactions asynchronously."""
        # Create a mock context manager response
        cm_response = AsyncMock()
        mock_response = cm_response.__aenter__.return_value
        mock_response.json.return_value = self.transactions_data
        mock_get.return_value = cm_response
        
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        client.session = aiohttp.ClientSession()
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        transactions = await client.get_transactions_async("acct_789")
        
        # Assertions
        self.assertEqual(transactions, self.transactions_data)
        mock_get.assert_called_once_with(
            f"{self.base_url}/stet/account/acct_789/transaction",
            headers={"Authorization": "bearer fake-token-12345", "Content-Type": "application/json"}
        )
        
        # Clean up
        if client.session and not client.session.closed:
            await client.session.close()
    
    @patch('aiohttp.ClientSession.get')
    async def test_data_collector_async(self, mock_get):
        """Test the data collector asynchronously."""
        # We need to patch multiple calls to the same method but with different responses
        # First, create the mock responses
        identity_response = AsyncMock()
        identity_response.__aenter__.return_value.json.return_value = self.identity_data
        
        accounts_response = AsyncMock()
        accounts_response.__aenter__.return_value.json.return_value = self.accounts_data
        
        balances_response = AsyncMock()
        balances_response.__aenter__.return_value.json.return_value = self.balances_data
        
        transactions_response = AsyncMock()
        transactions_response.__aenter__.return_value.json.return_value = self.transactions_data
        
        # Set up the side effect to return different responses based on the URL
        def side_effect(url, headers):
            if url == f"{self.base_url}/stet/identity":
                return identity_response
            elif url == f"{self.base_url}/stet/account":
                return accounts_response
            elif "/balance" in url:
                return balances_response
            elif "/transaction" in url:
                return transactions_response
            else:
                raise ValueError(f"Unexpected URL: {url}")
        
        mock_get.side_effect = side_effect
        
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        client.session = aiohttp.ClientSession()
        client.token = "fake-token-12345"
        client.token_type = "bearer"
        
        collector = BankingDataCollector(client)
        data = await collector.collect_all_data_async()
        
        # Assertions
        self.assertEqual(data["identity"], self.identity_data)
        self.assertEqual(len(data["accounts"]), 2)
        self.assertEqual(data["accounts"][0]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][0]["transactions"], self.transactions_data)
        self.assertEqual(data["accounts"][1]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][1]["transactions"], self.transactions_data)
        
        # Clean up
        if client.session and not client.session.closed:
            await client.session.close()


if __name__ == "__main__":
    unittest.main()