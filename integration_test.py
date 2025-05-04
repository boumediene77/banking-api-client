"""
Integration test for the Banking API Client.

This test will make actual API calls to the server.
"""
import asyncio
import json
import sys
import os
from banking_api_client import BankingAPIClient, BankingDataCollector


def test_sync_client():
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
            print(f"Authentication successful: {token[:10]}...")
            
            # Get identity
            identity = client.get_identity()
            # Construire le nom complet à partir des champs disponibles
            first_name = identity.get('first_name', '')
            last_name = identity.get('last_name', '')
            prefix = identity.get('prefix', '')
            full_name = f"{prefix} {first_name} {last_name}".strip()
            print(f"Identity: {full_name} ({identity.get('id')})")
            print(f"Date of birth: {identity.get('date_of_birth', 'N/A')}")
            
            # Get accounts
            accounts = client.get_accounts()
            print(f"Found {len(accounts)} accounts:")
            
            for account in accounts:
                account_id = account.get("id")
                print(f"  Account: {account.get('name')} ({account_id})")
                
                # Get balances
                balances = client.get_balances(account_id)
                # Gérer le cas où balances est une liste
                if isinstance(balances, list) and balances:
                    balance = balances[0]  # Premier élément de la liste
                    print(f"    Balance: {balance.get('amount')} {balance.get('currency')}")
                else:
                    print(f"    Balance: {balances}")
                
                # Get transactions
                transactions = client.get_transactions(account_id)
                print(f"    Transactions: {len(transactions)}")
                
                # Afficher la première transaction sans appeler get_transaction
                if transactions:
                    first_transaction = transactions[0]
                    print(f"    First transaction: {first_transaction.get('amount')} {first_transaction.get('currency')} - {first_transaction.get('label')}")
            
            print("Synchronous client test passed!")
            return True
        
        except Exception as e:
            print(f"Error during synchronous test: {e}")
            return False


async def test_async_client():
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
            print(f"Authentication successful: {token[:10]}...")
            
            # Get identity
            identity = await client.get_identity_async()
            # Construire le nom complet à partir des champs disponibles
            first_name = identity.get('first_name', '')
            last_name = identity.get('last_name', '')
            prefix = identity.get('prefix', '')
            full_name = f"{prefix} {first_name} {last_name}".strip()
            print(f"Identity: {full_name} ({identity.get('id')})")
            print(f"Date of birth: {identity.get('date_of_birth', 'N/A')}")
            
            # Get accounts
            accounts = await client.get_accounts_async()
            print(f"Found {len(accounts)} accounts:")
            
            for account in accounts:
                account_id = account.get("id")
                print(f"  Account: {account.get('name')} ({account_id})")
                
                # Get balances
                balances = await client.get_balances_async(account_id)
                # Gérer le cas où balances est une liste
                if isinstance(balances, list) and balances:
                    balance = balances[0]  # Premier élément de la liste
                    print(f"    Balance: {balance.get('amount')} {balance.get('currency')}")
                else:
                    print(f"    Balance: {balances}")
                
                # Get transactions
                transactions = await client.get_transactions_async(account_id)
                print(f"    Transactions: {len(transactions)}")
                
                # Afficher la première transaction sans appeler get_transaction_async
                if transactions:
                    first_transaction = transactions[0]
                    print(f"    First transaction: {first_transaction.get('amount')} {first_transaction.get('currency')} - {first_transaction.get('label')}")
            
            print("Asynchronous client test passed!")
            return True
        
        except Exception as e:
            print(f"Error during asynchronous test: {e}")
            return False


async def test_data_collector():
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
            
            # Save to file with proper UTF-8 handling
            with open("banking_data_sync.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Synchronous data collector test passed! Data saved to banking_data_sync.json")
            
            # Validate data structure
            assert "identity" in data
            assert "accounts" in data
            assert len(data["accounts"]) > 0
            assert "balances" in data["accounts"][0]
            assert "transactions" in data["accounts"][0]
            
        except Exception as e:
            print(f"Error during synchronous collector test: {e}")
            return False
    
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
            
            # Save to file with proper UTF-8 handling
            with open("banking_data_async.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Asynchronous data collector test passed! Data saved to banking_data_async.json")
            
            # Validate data structure
            assert "identity" in data
            assert "accounts" in data
            assert len(data["accounts"]) > 0
            assert "balances" in data["accounts"][0]
            assert "transactions" in data["accounts"][0]
            
            return True
            
        except Exception as e:
            print(f"Error during asynchronous collector test: {e}")
            return False


async def main():
    """Run all tests."""
    sync_result = test_sync_client()
    async_result = await test_async_client()
    collector_result = await test_data_collector()
    
    print("\nTest Summary:")
    print(f"Synchronous Client: {'PASS' if sync_result else 'FAIL'}")
    print(f"Asynchronous Client: {'PASS' if async_result else 'FAIL'}")
    print(f"Data Collector: {'PASS' if collector_result else 'FAIL'}")
    
    if sync_result and async_result and collector_result:
        print("\nAll tests passed!")
        return 0
    else:
        print("\nSome tests failed.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)