"""Collector module for gathering all data from the Banking API."""
from typing import Dict, Any

from .client import BankingAPIClient


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
            
        Raises:
            AuthenticationError: If authentication error occurs
            ResourceNotFoundError: If a resource is not found
            BankingAPIError: For other API errors
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
            
        Raises:
            AuthenticationError: If authentication error occurs
            ResourceNotFoundError: If a resource is not found
            BankingAPIError: For other API errors
        """
        if not self.client.use_async:
            raise RuntimeError("Use collect_all_data for sync mode")
        
        # Get identity
        identity = await self.client.get_identity_async()
        
        # Get accounts
        accounts = await self.client.get_accounts_async()
        
        for account in accounts:
            account_id = account.get("id")
            # Get balances and transactions sequentially for each account
            account["balances"] = await self.client.get_balances_async(account_id)
            account["transactions"] = await self.client.get_transactions_async(account_id)
        
        return {
            "identity": identity,
            "accounts": accounts
        }
    
    def verify_account_consistency(self, account_data, strict=False):
        """
        Verifies consistency between an account's balance and its transactions.
        
        Args:
            account_data: Account data including balances and transactions
            strict: If True, raises an exception in case of inconsistency; otherwise, returns False
        
        Returns:
            bool: True if the data is consistent, False otherwise
        """
        from .exceptions import BankingAPIError
        
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
            raise BankingAPIError(
                f"Inconsistency detected: Official balance {official_balance} ≠ "
                f"Sum of transactions {calculated_balance}"
            )
        
        return is_consistent