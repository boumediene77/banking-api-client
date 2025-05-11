"""
Unit tests for the BankingDataCollector class.
"""
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import json

from banking_api_client import BankingAPIClient
from banking_api_client import BankingDataCollector
from banking_api_client import BankingAPIError


class TestBankingDataCollector(unittest.TestCase):
    """Tests for the BankingDataCollector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://dsp2-technical-test.iliad78.net"
        self.username = "mdupuis"
        self.password = "111111"
        
        # Sample response data
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
    def test_data_collector(self, mock_session):
        """Test the data collector."""
        # Create mock client
        client = BankingAPIClient(self.base_url, self.username, self.password)
        client.get_identity = MagicMock(return_value=self.identity_data)
        client.get_accounts = MagicMock(return_value=self.accounts_data)
        client.get_balances = MagicMock(return_value=self.balances_data)
        client.get_transactions = MagicMock(return_value=self.transactions_data)
        
        # Create collector
        collector = BankingDataCollector(client)
        data = collector.collect_all_data()
        
        # Assertions
        self.assertEqual(data["identity"], self.identity_data)
        self.assertEqual(len(data["accounts"]), 2)
        self.assertEqual(data["accounts"][0]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][0]["transactions"], self.transactions_data)
        self.assertEqual(data["accounts"][1]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][1]["transactions"], self.transactions_data)
        
        # Verify method calls
        client.get_identity.assert_called_once()
        client.get_accounts.assert_called_once()
        client.get_balances.assert_called_with("acct_ruguKBdKe3Tr3e3iLsPwieqB")
        client.get_transactions.assert_called_with("acct_ruguKBdKe3Tr3e3iLsPwieqB")
    
    def test_verify_account_consistency(self):
        """Test account consistency verification."""
        # Create mock client
        client = BankingAPIClient(self.base_url, self.username, self.password)
        
        # Create collector
        collector = BankingDataCollector(client)
        
        # Test with consistent data
        account_data = {
            "balances": [{"amount": 50.25, "currency": "EUR"}],
            "transactions": [
                {"amount": 100.50, "currency": "EUR"},
                {"amount": -50.25, "currency": "EUR"}
            ]
        }
        
        # 100.50 - 50.25 = 50.25, which matches the balance
        is_consistent = collector.verify_account_consistency(account_data)
        self.assertTrue(is_consistent)
        
        # Test with inconsistent data
        account_data = {
            "balances": [{"amount": 100.00, "currency": "EUR"}],
            "transactions": [
                {"amount": 100.50, "currency": "EUR"},
                {"amount": -50.25, "currency": "EUR"}
            ]
        }
        
        # 100.50 - 50.25 = 50.25, which doesn't match the balance of 100.00
        is_consistent = collector.verify_account_consistency(account_data)
        self.assertFalse(is_consistent)
        
        # Test with inconsistent data and strict mode
        with self.assertRaises(BankingAPIError):
            collector.verify_account_consistency(account_data, strict=True)


class TestAsyncBankingDataCollector(unittest.IsolatedAsyncioTestCase):
    """Tests for the asynchronous BankingDataCollector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://dsp2-technical-test.iliad78.net"
        self.username = "agribard"
        self.password = "222222"
        
        # Sample response data
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
    
    async def test_data_collector_async(self):
        """Test the data collector asynchronously."""
        # Create mock client
        client = BankingAPIClient(self.base_url, self.username, self.password, use_async=True)
        
        # Mock async methods
        client.get_identity_async = AsyncMock(return_value=self.identity_data)
        client.get_accounts_async = AsyncMock(return_value=self.accounts_data)
        client.get_balances_async = AsyncMock(return_value=self.balances_data)
        client.get_transactions_async = AsyncMock(return_value=self.transactions_data)
        
        # Create collector
        collector = BankingDataCollector(client)
        data = await collector.collect_all_data_async()
        
        # Assertions
        self.assertEqual(data["identity"], self.identity_data)
        self.assertEqual(len(data["accounts"]), 2)
        self.assertEqual(data["accounts"][0]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][0]["transactions"], self.transactions_data)
        self.assertEqual(data["accounts"][1]["balances"], self.balances_data)
        self.assertEqual(data["accounts"][1]["transactions"], self.transactions_data)
        
        # Verify method calls
        client.get_identity_async.assert_called_once()
        client.get_accounts_async.assert_called_once()
        client.get_balances_async.assert_called_with("acct_012")
        client.get_transactions_async.assert_called_with("acct_012")


if __name__ == "__main__":
    unittest.main()