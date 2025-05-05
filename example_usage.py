"""
Example usage of the Banking API Client with proper UTF-8 handling.
"""
import asyncio
import json
from banking_api_client import BankingAPIClient, BankingDataCollector


def sync_example():
    """Example of using the client in synchronous mode."""
    base_url = "https://dsp2-technical-test.iliad78.net"
    username = "mdupuis"
    password = "111111"
    
    # Use as context manager
    with BankingAPIClient(base_url, username, password) as client:
        # Authenticate
        client.authenticate()
        
        # Create data collector
        collector = BankingDataCollector(client)
        
        # Collect all data
        data = collector.collect_all_data()
        
        # Pretty print the data with proper UTF-8 handling
        print(json.dumps(data, indent=2, ensure_ascii=False)) 
        
        # Save to file with proper UTF-8 handling
        with open("banking_data_sync.json", "w", encoding="utf-8") as f:  
            json.dump(data, f, indent=2, ensure_ascii=False) 
        
        print("Data saved to banking_data_sync.json")


async def async_example():
    """Example of using the client in asynchronous mode."""
    base_url = "https://dsp2-technical-test.iliad78.net"
    username = "mdupuis"
    password = "111111"
    
    # Use as async context manager
    async with BankingAPIClient(base_url, username, password, use_async=True) as client:
        # Authenticate
        await client.authenticate_async()
        
        # Create data collector
        collector = BankingDataCollector(client)
        
        # Collect all data
        data = await collector.collect_all_data_async()
        
        # Pretty print the data with proper UTF-8 handling
        print(json.dumps(data, indent=2, ensure_ascii=False)) 
        
        # Save to file with proper UTF-8 handling
        with open("banking_data_async.json", "w", encoding="utf-8") as f:  
            json.dump(data, f, indent=2, ensure_ascii=False) 
        
        print("Data saved to banking_data_async.json")


def main():
    """Main function to run examples."""
    print("Running synchronous example:")
    sync_example()
    
    print("\nRunning asynchronous example:")
    asyncio.run(async_example())


if __name__ == "__main__":
    main()