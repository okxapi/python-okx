# Changelog

All notable changes to `python-okx` are documented in this file.

## [0.4.3]

Packaging hygiene plus one additive ETH Staking endpoint. All changes are backward compatible — existing public signatures and happy-path behaviour are unchanged.

### Fixed
- Packaging split: dev/release-only tooling no longer leaks into end-user installs. `requirements.txt` now lists only the 5 runtime dependencies (`httpx[http2]`, `requests`, `websockets`, `certifi`, `loguru`), so `setup.py`'s `parse_requirements()` yields a runtime-only `install_requires`. The dev/test/release packages (`python-dotenv`, `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `build`, `twine`) moved to a new `dev_requirements.txt` (starts with `-r requirements.txt`). `setup.py` is unchanged. Contributors should now run `pip install -r dev_requirements.txt`. Consumers who relied on `python-okx` transitively installing `pytest`/`python-dotenv` etc. must install those themselves.

### Added
- `okx/Finance/EthStaking.py` `eth_cancel_redeem(ordId='')`: new method for `POST /api/v5/finance/staking-defi/eth/cancel-redeem`, bringing the ETH Staking module to full 7/7 endpoint coverage. Mirrors `eth_purchase` / `eth_redeem`.
- `okx/consts.py`: new `STACK_ETH_CANCEL_REDEEM` path constant.

## [0.4.2]

Community issue batch (GH#141 / GH#116 / GH#115) plus the v5 API sync batch. All changes are additive / opt-in and backward compatible — existing public signatures and happy-path behaviour are unchanged. New optional kwargs default to "unset" (omitted from the request); new endpoints/modules are net-new symbols.

### Added
- `okx/Account.py` `get_account_bills`: added optional `begin=''` / `end=''` time-window parameters, mirroring `get_account_bills_archive`. Empty defaults produce the exact same request as before (GH#141).
- `okx/websocket/WsPublicAsync.py` and `okx/websocket/WsPrivateAsync.py` `start()`: now return the created `consume()` task so callers can retain/await it (GH#116).
- `okx/Account.py` `set_trading_config`: new method for `POST /api/v5/account/set-trading-config` (params `type` (required), `stgyType` (optional; 0=general, 1=delta neutral, applies when type=stgyType)); `precheck_set_delta_neutral`: new method for `GET /api/v5/account/precheck-set-delta-neutral` (param `stgyType`) (delta-neutral trading config).
- `okx/Account.py` `get_bill_type` / `apply_bills`: new methods for `GET /api/v5/account/subtypes` (optional `type`) and `POST /api/v5/account/bills-history-archive` (params `year`, `quarter`, optional `type`) (bill subtypes + async bill history archive).
- `okx/DualInvest.py` (new module) `DualInvestAPI`: 8 methods for the `/api/v5/finance/sfp/dcd/*` dual-currency (DCD) product surface — `get_currency_pairs`, `get_product_info`, `request_quote`, `trade`, `request_redeem_quote`, `redeem`, `get_order_state`, `get_order_history`.
- `okx/PublicData.py` `get_announcements`: new method for `GET /api/v5/announcement/announcements`.
- `okx/consts.py`: new path constants for all endpoints above, plus 8 `DUAL_INVEST_*` constants.

### Fixed
- `okx/websocket/WsPublicAsync.py` and `okx/websocket/WsPrivateAsync.py` `consume()`: wrap the receive loop in `try/except ConnectionClosedError` — on disconnect it now logs the error, pushes an `{"event": "error", "code": "ConnClosed", ...}` message to the existing callback, and re-raises so the awaited task surfaces the failure instead of dying silently. No auto-reconnect (retry is left to the caller) (GH#116).

### Changed
- `okx/Trade.py` `cancel_algo_order`: renamed the positional argument `params` → `orders_data` and added a docstring documenting the expected `list[{'instId', 'algoId'}]`. The legacy `params=` keyword is kept as a deprecated alias, so all existing call shapes (positional and `params=`) continue to work (GH#115).
- `okx/Trade.py` `place_algo_order`: added optional `advanceOrdType=None` (trigger-order advance type) and `tpTriggerRatio=None` / `slTriggerRatio=None`. Unset params are omitted from the request.
- `okx/Account.py` `get_fee_rates`: added optional `groupId=None` (query fees by instrument group). Unset param is omitted.
- `okx/Trade.py` `place_order`: added optional `isElpTakerAccess=None` (ELP taker access on IOC) and `instIdCode=None`. Unset params are omitted.
- `okx/Convert.py` `get_currency_pair` / `estimate_quote` / `convert_trade`: added optional `convertMode=None` (0=standard, 1=large-order VIP). Unset param is omitted.
- `okx/Trade.py` `amend_order`: added optional `newTpTriggerRatio=None` / `newSlTriggerRatio=None`. Unset params are omitted.
