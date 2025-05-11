"""Exceptions for the Banking API Client."""

class BankingAPIError(Exception):
    """Base exception for Banking API errors."""
    pass


class AuthenticationError(BankingAPIError):
    """Raised when authentication fails."""
    pass


class ResourceNotFoundError(BankingAPIError):
    """Raised when a resource is not found."""
    pass