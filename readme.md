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

## Available Functions

The `banking_api_client.py` module provides two main classes:

### BankingAPIClient

The `BankingAPIClient` class provides both synchronous and asynchronous methods to interact with the Banking API:

#### Synchronous Methods
- `authenticate()`: Authenticate with the API and retrieve a token
- `get_identity()`: Get user identity information
- `get_accounts()`: Get all accounts
- `get_account(account_id)`: Get a specific account by ID
- `get_balances(account_id)`: Get balances for an account
- `get_transactions(account_id)`: Get transactions for an account

#### Asynchronous Methods
- `authenticate_async()`: Authenticate with the API asynchronously
- `get_identity_async()`: Get user identity information asynchronously
- `get_accounts_async()`: Get all accounts asynchronously
- `get_account_async(account_id)`: Get a specific account by ID asynchronously
- `get_balances_async(account_id)`: Get balances for an account asynchronously
- `get_transactions_async(account_id)`: Get transactions for an account asynchronously

### BankingDataCollector

The `BankingDataCollector` class provides methods to collect all data in a single operation:

- `collect_all_data()`: Collect all data synchronously
- `collect_all_data_async()`: Collect all data asynchronously

Both classes support the context manager protocol for proper resource management.

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


## Running the Example

```bash
python example_usage.py
```

## Tests

### Unit Tests

```bash
python -m unittest tests.py
```

### Integration Tests

```bash
python integration_test.py
```



## Notes

- The data is static and subject to change
- Data consistency is not guaranteed (e.g., balance amount may not be consistent with transactions)

- The question of verifying whether the balance matches the sum of transactions is very pertinent and deserves consideration.

- An ideal implementation might look like this:

```python
def verify_account_consistency(self, account_data, strict=False):
    """
    Verifies consistency between an account's balance and its transactions.
    
    Args:
        account_data: Account data including balances and transactions
        strict: If True, raises an exception in case of inconsistency; otherwise, returns False
    
    Returns:
        bool: True if the data is consistent, False otherwise
    """
    balances = account_data.get("balances", {})
    transactions = account_data.get("transactions", [])
    
    # Handle the case where balances is a list
    if isinstance(balances, list) and balances:
        balance_data = balances[0]
        official_balance = balance_data.get("amount", 0)
    else:
        official_balance = balances.get("amount", 0)
    
    calculated_balance = sum(tx.get("amount", 0) for tx in transactions)
    
    # Tolerance for rounding errors
    is_consistent = abs(official_balance - calculated_balance) < 0.01
    
    if not is_consistent and strict:
        raise ValueError(
            f"Inconsistency detected: Official balance {official_balance} ≠ "
            f"Sum of transactions {calculated_balance}"
        )
    
    return is_consistent
```

- This function could be added to the `BankingDataCollector` class and used optionally:

```python
# Example usage
collector = BankingDataCollector(client)
data = collector.collect_all_data()

# Optional consistency check
for account in data["accounts"]:
    is_consistent = collector.verify_account_consistency(account)
    if not is_consistent:
        print(f"Warning: Inconsistency detected for account {account.get('id')}")
```


