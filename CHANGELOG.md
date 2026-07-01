# Changelog

All notable changes to `python-okx` are documented in this file.

## [0.4.2]

Community issue batch (GH#141 / GH#116 / GH#115) — all changes are additive / opt-in and backward compatible; public signatures and happy-path behaviour are unchanged.

### Added
- `okx/Account.py` `get_account_bills`: added optional `begin=''` / `end=''` time-window parameters, mirroring `get_account_bills_archive`. Empty defaults produce the exact same request as before (GH#141).
- `okx/websocket/WsPublicAsync.py` and `okx/websocket/WsPrivateAsync.py` `start()`: now return the created `consume()` task so callers can retain/await it (GH#116).

### Fixed
- `okx/websocket/WsPublicAsync.py` and `okx/websocket/WsPrivateAsync.py` `consume()`: wrap the receive loop in `try/except ConnectionClosedError` — on disconnect it now logs the error, pushes an `{"event": "error", "code": "ConnClosed", ...}` message to the existing callback, and re-raises so the awaited task surfaces the failure instead of dying silently. No auto-reconnect (retry is left to the caller) (GH#116).

### Changed
- `okx/Trade.py` `cancel_algo_order`: renamed the positional argument `params` → `orders_data` and added a docstring documenting the expected `list[{'instId', 'algoId'}]`. The legacy `params=` keyword is kept as a deprecated alias, so all existing call shapes (positional and `params=`) continue to work (GH#115).
