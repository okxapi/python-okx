# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python SDK for OKX exchange v5 API. An unofficial wrapper providing synchronous REST API clients and asynchronous WebSocket implementations for trading, account management, market data, and more.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run unit tests
pytest test/unit/ -v

# Run tests with coverage
pytest test/unit/ -v --cov=okx --cov-report=term-missing

# Run specific test file
pytest test/unit/okx/test_account.py -v

# Lint with ruff
ruff check okx/ --ignore=E501

# Build package
python -m build --no-isolation

# Verify package
twine check dist/*
```

## Architecture

### Core Structure

- **okx/okxclient.py** - Base `OkxClient` class extending `httpx.Client` with HTTP/2 support. Handles authentication, request signing, and common request logic.
- **okx/consts.py** - API endpoint constants and HTTP headers. All REST endpoints defined here.
- **okx/utils.py** - Cryptographic signing (HMAC-SHA256), timestamp generation, header construction.

### API Modules (Pattern: `class XAPI(OkxClient)`)

Each module inherits from `OkxClient` and implements specific endpoint methods:

- **Account.py** - Account balance, positions, leverage, margin, bills
- **Trade.py** - Order placement, cancellation, amendments, fills
- **Funding.py** - Deposits, withdrawals, transfers, asset management
- **MarketData.py** - Tickers, order books, candles, trades
- **PublicData.py** - Instrument info, funding rates, open interest
- **SubAccount.py** - Sub-account management and transfers
- **Grid.py** - Trading bot grid strategies
- **WebSocket modules** - `WsPublicAsync.py`, `WsPrivateAsync.py` for real-time data

### Request Pattern

All API calls follow this pattern:
```python
# GET with params
return self._request_with_params(GET, ENDPOINT_CONSTANT, params)

# POST with params
return self._request_with_params(POST, ENDPOINT_CONSTANT, params)

# GET without params
return self._request_without_params(GET, ENDPOINT_CONSTANT)
```

### Testing

- **test/unit/** - Unit tests for API modules
- **test/test_*.py** - Integration tests (require API credentials)
- **test/config.py** - Loads credentials from `.env` via `get_api_credentials()`

## Environment Setup

Create `.env` file (do not commit):
```bash
OKX_API_KEY=your_api_key_here
OKX_API_SECRET=your_api_secret_here
OKX_PASSPHRASE=your_passphrase_here
OKX_FLAG=1  # 0=live, 1=demo
```

## Key Conventions

- **flag parameter**: `'0'` for live trading, `'1'` for demo/simulated trading
- **All API modules** accept credentials in constructor and pass to parent `OkxClient`
- **httpx** is used for HTTP client (not requests) for REST calls
- **websockets** library for WebSocket connections
- **loguru** for logging
- Methods use `GET`/`POST` constants from `consts.py`, not string literals

## Additional Architecture Details

### Exception Handling
Three custom exceptions in `okx/exceptions.py`:
- **OkxAPIException** - Raised for API errors with code and message from response
- **OkxRequestException** - General request errors
- **OkxParamsException** - Invalid parameters

### WebSocket Architecture
- **WsPublicAsync.py** - Public channels (market data), async-only
- **WsPrivateAsync.py** - Private channels (account/order updates), requires authentication
- **WebSocketFactory.py** - Manages WebSocket connections with reconnection logic
- **WsUtils.py** - Authentication signing for private channels

### Finance Submodule
Nested package `okx/Finance/` with specialized staking/DeFi endpoints:
- `EthStaking.py`, `SolStaking.py` - Cryptocurrency staking
- `Savings.py` - Savings products
- `StakingDefi.py` - General DeFi staking
- `FlexibleLoan.py` - Flexible loan products

### Package Structure
- Main package exports version via `okx/__init__.py`
- All API modules follow naming: `<Feature>.py` (e.g., `Account.py`, `Trade.py`)
- Constants in `consts.py` use UPPER_CASE with endpoint paths
