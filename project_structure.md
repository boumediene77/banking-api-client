# Project Structure

```
banking-api-client/
├── README.md               # Project documentation
├── setup.py                # Package configuration file
├── requirements.txt        # Dependencies
├── banking_api_client.py   # Main library module
├── __init__.py             # Package initialization
├── example_usage.py        # Example use of the library
├── tests.py                # Unit tests
└── integration_test.py     # Integration tests with real API calls
```

## How to use this project

### Installation

1. Clone the repository or extract the archive:
   ```
   # Option 1: Clone the repository
   git clone [REPO_URL]
   
   # Option 2: Extract the archive
   tar -xzvf banking-api-client.tar.gz
   ```

2. Navigate to the directory:
   ```
   cd banking-api-client
   ```

3. Installation with pip (standard method):
   ```
   # Install dependencies
   pip install -r requirements.txt
   
   # Install the package in development mode
   pip install -e .
   ```

4. Installation with uv (recommended in the technical test):
   ```
   # Install uv if not already installed
   pip install uv
   
   # Install dependencies
   uv pip install -r requirements.txt
   
   # Install the package in development mode
   uv pip install -e .
   ```

### Example usage

Run the example script to see the library in action:
```
python example_usage.py
```

This will authenticate both users, retrieve all data, and save it to JSON files.

### Running tests

1. Run unit tests:
   ```
   python -m unittest tests.py
   ```

2. Run integration tests:
   ```
   python integration_test.py
   ```



## Design decisions

1. **Modular architecture**: The library is designed in a modular way, with a clear separation between the API client and the data collector. This makes extension and maintenance easier.

2. **Synchronous/asynchronous support**: The library supports both synchronous and asynchronous usage, allowing users to choose the most appropriate approach for their use case.

3. **Context manager**: The client implements the context manager protocol, ensuring that resources are properly released.

4. **Error handling**: The library includes comprehensive error handling, raising appropriate exceptions when API calls fail.

5. **Type hints**: Type hints are used throughout the codebase, making it easier to understand and providing better IDE support.

6. **Documentation**: The code is well-documented with docstrings, explaining the purpose and usage of each function and class.

7. **Testing**: The library includes both unit tests and integration tests, ensuring that it works as expected.

8. **Generic and reusable**: The API client is designed to be as generic as possible, facilitating reuse and adaptation to other projects.

9. **Consistency**: A consistent approach is used for all API endpoints, making the library's usage intuitive.

10. **Python compatibility**: The library is compatible with Python 3.7+ and has been specifically tested with Python 3.11 to demonstrate the use of recent language features.

11. **Using uv**: In accordance with the technical test recommendation, the project supports installation via uv, an ultra-fast Python package installer written in Rust. This enables faster installation and better dependency resolution while maintaining compatibility with pip.
