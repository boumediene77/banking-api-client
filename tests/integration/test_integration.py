"""
Integration test for the Banking API Client.

This test will make actual API calls to the server.
"""
import asyncio
import json
import sys
import os
import unittest

from banking_api_client import BankingAPIClient, BankingDataCollector


class TestBankingAPIIntegration(unittest.TestCase):
    """Integration tests for the Banking API Client."""
    
    def test_sync_client(self):
        """Test the synchronous client with real API calls."""
        print("Testing synchronous client...")
        
        base_url = "https://dsp2-technical-test.iliad78.net"
        username = "mdupuis"
        password = "111111"
        
        # Use as context manager
        with BankingAPIClient(base_url, username, password) as client:
            try:
                # Authenticate
                token = client.authenticate()
                self.assertIsNotNone(token)
                print(f"Authentication successful: {token[:10]}...")
                
                # Get identity
                identity = client.get_identity()
                self.assertIsNotNone(identity)
                self.assertEqual(identity.get('first_name'), 'Maurice')
                self.assertEqual(identity.get('last_name'), 'Dupuis')
                
                # Get accounts
                accounts = client.get_accounts()
                self.assertIsNotNone(accounts)
                self.assertGreater(len(accounts), 0)
                
                for account in accounts:
                    account_id = account.get("id")
                    
                    # Get balances
                    balances = client.get_balances(account_id)
                    self.assertIsNotNone(balances)
                    
                    # Get transactions
                    transactions = client.get_transactions(account_id)
                    self.assertIsNotNone(transactions)
                
                print("Synchronous client test passed!")
                return True
            
            except Exception as e:
                print(f"Error during synchronous test: {e}")
                self.fail(f"Synchronous test failed: {e}")
    
    async def test_async_client(self):
        """Test the asynchronous client with real API calls."""
        print("\nTesting asynchronous client...")
        
        base_url = "https://dsp2-technical-test.iliad78.net"
        username = "agribard"
        password = "222222"
        
        # Use as async context manager
        async with BankingAPIClient(base_url, username, password, use_async=True) as client:
            try:
                # Authenticate
                token = await client.authenticate_async()
                self.assertIsNotNone(token)
                print(f"Authentication successful: {token[:10]}...")
                
                # Get identity
                identity = await client.get_identity_async()
                self.assertIsNotNone(identity)
                self.assertEqual(identity.get('first_name'), 'Antoinette')
                self.assertEqual(identity.get('last_name'), 'Gribard')
                
                # Get accounts
                accounts = await client.get_accounts_async()
                self.assertIsNotNone(accounts)
                self.assertGreater(len(accounts), 0)
                
                for account in accounts:
                    account_id = account.get("id")
                    
                    # Get balances
                    balances = await client.get_balances_async(account_id)
                    self.assertIsNotNone(balances)
                    
                    # Get transactions
                    transactions = await client.get_transactions_async(account_id)
                    self.assertIsNotNone(transactions)
                
                print("Asynchronous client test passed!")
                return True
            
            except Exception as e:
                print(f"Error during asynchronous test: {e}")
                self.fail(f"Asynchronous test failed: {e}")
    
    async def test_data_collector(self):
        """Test the data collector with real API calls."""
        print("\nTesting data collector...")
        
        # Test synchronous collector
        base_url = "https://dsp2-technical-test.iliad78.net"
        username = "mdupuis"
        password = "111111"
        
        # Use as context manager
        with BankingAPIClient(base_url, username, password) as client:
            try:
                # Authenticate
                client.authenticate()
                
                # Create data collector
                collector = BankingDataCollector(client)
                
                # Collect all data
                data = collector.collect_all_data()
                
                # Save data to file for inspection
                with open("banking_data_sync.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"Synchronous data collector test passed! Data saved to banking_data_sync.json")
                
                # Validate data structure
                self.assertIn("identity", data)
                self.assertIn("accounts", data)
                self.assertGreater(len(data["accounts"]), 0)
                self.assertIn("balances", data["accounts"][0])
                self.assertIn("transactions", data["accounts"][0])
                
            except Exception as e:
                print(f"Error during synchronous collector test: {e}")
                self.fail(f"Synchronous collector test failed: {e}")
        
        # Test asynchronous collector
        username = "agribard"
        password = "222222"
        
        # Use as async context manager
        async with BankingAPIClient(base_url, username, password, use_async=True) as client:
            try:
                # Authenticate
                await client.authenticate_async()
                
                # Create data collector
                collector = BankingDataCollector(client)
                
                # Collect all data
                data = await collector.collect_all_data_async()
                
                # Save data to file for inspection
                with open("banking_data_async.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"Asynchronous data collector test passed! Data saved to banking_data_async.json")
                
                # Validate data structure
                self.assertIn("identity", data)
                self.assertIn("accounts", data)
                self.assertGreater(len(data["accounts"]), 0)
                self.assertIn("balances", data["accounts"][0])
                self.assertIn("transactions", data["accounts"][0])
                
                return True
                
            except Exception as e:
                print(f"Error during asynchronous collector test: {e}")
                self.fail(f"Asynchronous collector test failed: {e}")


def run_tests():
    """Run all integration tests."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestBankingAPIIntegration('test_sync_client'))
    
    # Run async tests using the event loop
    async_test_case = TestBankingAPIIntegration('test_async_client')
    async_collector_test_case = TestBankingAPIIntegration('test_data_collector')
    
    # Run the tests
    unittest.TextTestRunner().run(test_suite)
    
    # Run async tests using asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_test_case.test_async_client())
    loop.run_until_complete(async_collector_test_case.test_data_collector())
    loop.close()


if __name__ == "__main__":
    run_tests()