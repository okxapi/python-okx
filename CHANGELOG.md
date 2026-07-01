# Changelog

All notable changes to `python-okx` are documented in this file.

## [0.4.2]

Community issue batch (GH#141 / GH#116 / GH#115) plus the v5 API sync batch. All changes are additive / opt-in and backward compatible — existing public signatures and happy-path behaviour are unchanged. New optional kwargs default to "unset" (omitted from the request); new endpoints/modules are net-new symbols.

### Added
- `okx/Account.py` `get_account_bills`: added optional `begin=''` / `end=''` time-window parameters, mirroring `get_account_bills_archive`. Empty defaults produce the exact same request as before (GH#141).
- `okx/websocket/WsPublicAsync.py` and `okx/websocket/WsPrivateAsync.py` `start()`: now return the created `consume()` task so callers can retain/await it (GH#116).
- `okx/Account.py` `set_trading_config` / `precheck_set_delta_neutral`: new methods for `POST /api/v5/account/set-trading-config` and `POST /api/v5/account/precheck-set-delta-neutral` (delta-neutral trading config, BROK-1724).
- `okx/Account.py` `get_bill_type` / `apply_bills`: new methods for `GET /api/v5/account/bill-type` and `POST /api/v5/account/bills/apply` (bill types + async bill export, BROK-1728).
- `okx/Trade.py` `get_oneclick_repay_list_new` / `oneclick_repay_new`: new methods for `GET /api/v5/trade/one-click-repay-currency-list-new` and `POST /api/v5/trade/one-click-repay-new`, mirroring the `*_v2` methods (BROK-1727).
- `okx/Finance/Earn.py` (new module) `EarnAPI`: `staking_cancel_redeem` (`POST /api/v5/earn/staking-cancel-redeem`) and `get_staking_products` (`GET /api/v5/earn/staking-products`) (BROK-1726).
- `okx/DualInvest.py` (new module) `DualInvestAPI`: 8 methods for the `/api/v5/dualinvest/*` product surface — `get_currency_pairs`, `get_product_info`, `request_quote`, `trade`, `request_redeem_quote`, `redeem`, `get_order_state`, `get_order_history` (BROK-1729).
- `okx/PublicData.py` `get_announcements`: new method for `GET /api/v5/announcement/announcements` (BROK-1730).
- `okx/consts.py`: new path constants for all endpoints above, plus 8 `DUAL_INVEST_*` constants.

### Fixed
- `okx/websocket/WsPublicAsync.py` and `okx/websocket/WsPrivateAsync.py` `consume()`: wrap the receive loop in `try/except ConnectionClosedError` — on disconnect it now logs the error, pushes an `{"event": "error", "code": "ConnClosed", ...}` message to the existing callback, and re-raises so the awaited task surfaces the failure instead of dying silently. No auto-reconnect (retry is left to the caller) (GH#116).

### Changed
- `okx/Trade.py` `cancel_algo_order`: renamed the positional argument `params` → `orders_data` and added a docstring documenting the expected `list[{'instId', 'algoId'}]`. The legacy `params=` keyword is kept as a deprecated alias, so all existing call shapes (positional and `params=`) continue to work (GH#115).
- `okx/Trade.py` `place_algo_order`: added optional `advanceOrdType=None` (trigger-order advance type, BROK-1720) and `tpTriggerRatio=None` / `slTriggerRatio=None` (BROK-1725). Unset params are omitted from the request.
- `okx/Account.py` `get_fee_rates`: added optional `groupId=None` (query fees by instrument group, BROK-1721). Unset param is omitted.
- `okx/Trade.py` `place_order`: added optional `isElpTakerAccess=None` (ELP taker access on IOC, BROK-1722) and `instIdCode=None` (BROK-1725). Unset params are omitted.
- `okx/Convert.py` `get_currency_pair` / `estimate_quote` / `convert_trade`: added optional `convertMode=None` (0=standard, 1=large-order VIP, BROK-1723). Unset param is omitted.
- `okx/Trade.py` `amend_order`: added optional `newTpTriggerRatio=None` / `newSlTriggerRatio=None` (BROK-1725). Unset params are omitted.
