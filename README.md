# Banking API Client

A Python library to consume the Banking API available at https://dsp2-technical-test.iliad78.net.

## Features

- Retrieval of all information available through the API:
  - User identity
  - Bank accounts
  - Balances
  - Transactions
- Support for both synchronous and asynchronous modes
- Context manager implementation
- Comprehensive error handling
- Modular and generic design
- Compatible with Python 3.7+ (recommended: Python 3.11+)

## Project Structure

```
banking-api-client/
├── src/
│   └── banking_api_client/
│       ├── __init__.py       # Package initialization
│       ├── client.py         # BankingAPIClient class
│       ├── collector.py      # BankingDataCollector class
│       ├── exceptions.py     # Custom exceptions
│       └── utils.py          # Utility functions
├── tests/
│   ├── unit/                 # Unit tests
│   │   ├── test_client.py    # Tests for BankingAPIClient
│   │   └── test_collector.py # Tests for BankingDataCollector
│   └── integration/
│       └── test_integration.py # Integration tests with real API calls
├── examples/
│   └── example_usage.py      # Example usage of the library
├── README.md                 # Project documentation
├── setup.py                  # Package configuration
└── requirements.txt          # Dependencies
```

## Installation

### From source

#### With pip (standard method)

```bash
# Clone the repository or extract the archive
git clone [REPO_URL] or tar -xzvf banking-api-client.tar.gz

# Navigate to the directory
cd banking-api-client

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

#### With uv (recommended, faster)

```bash
# Install uv if not already installed
pip install uv

# Clone the repository or extract the archive
git clone [REPO_URL] or tar -xzvf banking-api-client.tar.gz

# Navigate to the directory
cd banking-api-client

# Install dependencies
uv pip install -r requirements.txt

# Install the package
uv pip install .
```

### Development mode

#### With pip

```bash
pip install -e .
```

#### With uv (recommended)

```bash
uv pip install -e .
```

## Usage

### Synchronous Mode

```python
from banking_api_client import BankingAPIClient, BankingDataCollector

# Initialize the client
with BankingAPIClient("https://dsp2-technical-test.iliad78.net", "mdupuis", "111111") as client:
    # Authenticate
    client.authenticate()
    
    # Get identity
    identity = client.get_identity()
    print(f"User: {identity.get('first_name')} {identity.get('last_name')}")
    
    # Get accounts
    accounts = client.get_accounts()
    for account in accounts:
        account_id = account.get("id")
        print(f"Account: {account.get('name')} ({account_id})")
        
        # Get balances
        balances = client.get_balances(account_id)
        if isinstance(balances, list) and balances:
            balance = balances[0]
            print(f"Balance: {balance.get('amount')} {balance.get('currency')}")
        
        # Get transactions
        transactions = client.get_transactions(account_id)
        print(f"Transactions: {len(transactions)}")
```

### Asynchronous Mode

```python
import asyncio
from banking_api_client import BankingAPIClient, BankingDataCollector

async def main():
    # Initialize the client in asynchronous mode
    async with BankingAPIClient("https://dsp2-technical-test.iliad78.net", 
                               "agribard", "222222", use_async=True) as client:
        # Authenticate
        await client.authenticate_async()
        
        # Get all data with the collector
        collector = BankingDataCollector(client)
        all_data = await collector.collect_all_data_async()
        
        # Access data
        print(f"User: {all_data['identity']['first_name']} {all_data['identity']['last_name']}")
        
        for account in all_data['accounts']:
            print(f"Account: {account['name']}")
            if isinstance(account['balances'], list) and account['balances']:
                balance = account['balances'][0]
                print(f"Balance: {balance['amount']} {balance['currency']}")
            print(f"Transactions: {len(account['transactions'])}")

# Run the asynchronous function
asyncio.run(main())
```

## Using BankingDataCollector

For convenience, the library provides a `BankingDataCollector` class that allows retrieving all information in a single call:

```python
from banking_api_client import BankingAPIClient, BankingDataCollector
import json

with BankingAPIClient("https://dsp2-technical-test.iliad78.net", "mdupuis", "111111") as client:
    client.authenticate()
    
    collector = BankingDataCollector(client)
    all_data = collector.collect_all_data()
    
    # Save to file
    with open("banking_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
```

## Running the Examples

```bash
python -m examples.example_usage
```

## Tests

### Unit Tests

```bash
python -m unittest discover -s tests/unit
```

### Integration Tests

```bash
python -m tests.integration.test_integration
```

## Notes

- The data is static and subject to change
- Data consistency is not guaranteed (e.g., balance amount may not be consistent with transactions)
- The `verify_account_consistency` method in the `BankingDataCollector` class can be used to check if the balance matches the sum of transactions