# http header
API_URL = 'https://www.okx.com'

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'

ACEEPT = 'Accept'
COOKIE = 'Cookie'
LOCALE = 'Locale='

APPLICATION_JSON = 'application/json'

GET = "GET"
POST = "POST"

SERVER_TIMESTAMP_URL = '/api/v5/public/time'

# account-complete-testcomplete
POSITION_RISK='/api/v5/account/account-position-risk'
ACCOUNT_INFO = '/api/v5/account/balance'
POSITION_INFO = '/api/v5/account/positions'
BILLS_DETAIL = '/api/v5/account/bills'
BILLS_ARCHIVE = '/api/v5/account/bills-archive'
ACCOUNT_CONFIG = '/api/v5/account/config'
POSITION_MODE = '/api/v5/account/set-position-mode'
SET_LEVERAGE = '/api/v5/account/set-leverage'
MAX_TRADE_SIZE = '/api/v5/account/max-size'
MAX_AVAIL_SIZE = '/api/v5/account/max-avail-size'
ADJUSTMENT_MARGIN = '/api/v5/account/position/margin-balance'
GET_LEVERAGE = '/api/v5/account/leverage-info'
MAX_LOAN = '/api/v5/account/max-loan'
FEE_RATES = '/api/v5/account/trade-fee'
INTEREST_ACCRUED = '/api/v5/account/interest-accrued'
INTEREST_RATE = '/api/v5/account/interest-rate'
SET_GREEKS = '/api/v5/account/set-greeks'
ISOLATED_MODE = '/api/v5/account/set-isolated-mode'
MAX_WITHDRAWAL = '/api/v5/account/max-withdrawal'
ACCOUNT_RISK = '/api/v5/account/risk-state' #need add
BORROW_REPAY = '/api/v5/account/borrow-repay'
BORROW_REPAY_HISTORY = '/api/v5/account/borrow-repay-history'
INTEREST_LIMITS = '/api/v5/account/interest-limits'
SIMULATED_MARGIN = '/api/v5/account/simulated_margin'
GREEKS = '/api/v5/account/greeks'
POSITIONS_HISTORY = '/api/v5/account/positions-history' #need add
GET_PM_LIMIT = '/api/v5/account/position-tiers' #need add
GET_VIP_INTEREST_ACCRUED_DATA = '/api/v5/account/vip-interest-accrued'
GET_VIP_INTEREST_DEDUCTED_DATA = '/api/v5/account/vip-interest-deducted'
GET_VIP_LOAN_ORDER_LIST= '/api/v5/account/vip-loan-order-list'
GET_VIP_LOAN_ORDER_DETAIL= '/api/v5/account/vip-loan-order-detail'
SET_RISK_OFFSET_TYPE = '/api/v5/account/set-riskOffset-type'
SET_AUTO_LOAN = '/api/v5/account/set-auto-loan'
ACTIVSTE_OPTION = '/api/v5/account/activate-option'

# funding-complete-testcomplete
DEPOSIT_ADDRESS = '/api/v5/asset/deposit-address'
GET_BALANCES = '/api/v5/asset/balances'
FUNDS_TRANSFER = '/api/v5/asset/transfer'
TRANSFER_STATE = '/api/v5/asset/transfer-state'
WITHDRAWAL_COIN = '/api/v5/asset/withdrawal'
DEPOSIT_HISTORIY = '/api/v5/asset/deposit-history'
CURRENCY_INFO = '/api/v5/asset/currencies'
PURCHASE_REDEMPT = '/api/v5/asset/purchase_redempt'
BILLS_INFO = '/api/v5/asset/bills'
DEPOSIT_LIGHTNING = '/api/v5/asset/deposit-lightning'
WITHDRAWAL_LIGHTNING = '/api/v5/asset/withdrawal-lightning'
CANCEL_WITHDRAWAL = '/api/v5/asset/cancel-withdrawal' #need add
WITHDRAWAL_HISTORIY = '/api/v5/asset/withdrawal-history'
CONVERT_DUST_ASSETS = '/api/v5/asset/convert-dust-assets' #need add
ASSET_VALUATION = '/api/v5/asset/asset-valuation' #need add
SET_LENDING_RATE = '/api/v5/asset/set-lending-rate'
LENDING_HISTORY = '/api/v5/asset/lending-history'
LENDING_RATE_HISTORY = '/api/v5/asset/lending-rate-history'
LENDING_RATE_SUMMARY = '/api/v5/asset/lending-rate-summary'
GET_SAVING_BALANCE = '/api/v5/asset/saving-balance' #need to add
GET_WITHDRAWAL_HISTORY = '/api/v5/asset/withdrawal-history'
GET_NON_TRADABLE_ASSETS = '/api/v5/asset/non-tradable-assets'
GET_DEPOSIT_WITHDrAW_STATUS = '/api/v5/asset/deposit-withdraw-status'


# Market Data-Complete-testComplete
TICKERS_INFO = '/api/v5/market/tickers'
TICKER_INFO = '/api/v5/market/ticker'
INDEX_TICKERS = '/api/v5/market/index-tickers'
ORDER_BOOKS = '/api/v5/market/books'
MARKET_CANDLES = '/api/v5/market/candles'
HISTORY_CANDLES = '/api/v5/market/history-candles'
INDEX_CANSLES = '/api/v5/market/index-candles'
MARKPRICE_CANDLES = '/api/v5/market/mark-price-candles'
MARKET_TRADES = '/api/v5/market/trades'
VOLUMNE = '/api/v5/market/platform-24-volume'
ORACLE = '/api/v5/market/open-oracle' #need to update? if it is open oracle
INDEX_COMPONENTS = '/api/v5/market/index-components' #need to add
EXCHANGE_RATE = '/api/v5/market/exchange-rate' #need to add
HISTORY_TRADES = '/api/v5/market/history-trades' #need to add
BLOCK_TICKERS = '/api/v5/market/block-tickers' #need to add
BLOCK_TICKER = '/api/v5/market/block-ticker'#need to add
BLOCK_TRADES = '/api/v5/market/block-trades'#need to add
GET_ORDER_LITE_BOOK = '/api/v5/market/books-lite'
GET_OPTION_TRADES = '/api/v5/market/option/instrument-family-trades'

# Public Data-Complete-testComplete
INSTRUMENT_INFO = '/api/v5/public/instruments'
DELIVERY_EXERCISE = '/api/v5/public/delivery-exercise-history'
OPEN_INTEREST = '/api/v5/public/open-interest'
FUNDING_RATE = '/api/v5/public/funding-rate'
FUNDING_RATE_HISTORY = '/api/v5/public/funding-rate-history'
PRICE_LIMIT = '/api/v5/public/price-limit'
OPT_SUMMARY = '/api/v5/public/opt-summary'
ESTIMATED_PRICE = '/api/v5/public/estimated-price'
DICCOUNT_INTETEST_INFO = '/api/v5/public/discount-rate-interest-free-quota'
SYSTEM_TIME = '/api/v5/public/time'
LIQUIDATION_ORDERS = '/api/v5/public/liquidation-orders'
MARK_PRICE = '/api/v5/public/mark-price'
TIER = '/api/v5/public/position-tiers'
INTEREST_LOAN = '/api/v5/public/interest-rate-loan-quota' #need to add
UNDERLYING = '/api/v5/public/underlying' #need to add
VIP_INTEREST_RATE_LOAN_QUOTA = '/api/v5/public/vip-interest-rate-loan-quota' #need to add
INSURANCE_FUND = '/api/v5/public/insurance-fund'#need to add
CONVERT_CONTRACT_COIN = '/api/v5/public/convert-contract-coin' #need to add
GET_OPTION_TICKBANDS = '/api/v5/public/instrument-tick-bands'
GET_OPTION_TRADES = '/api/v5/public/option-trades'

# TRADING DATA-COMPLETE
SUPPORT_COIN = '/api/v5/rubik/stat/trading-data/support-coin'
TAKER_VOLUME = '/api/v5/rubik/stat/taker-volume'
MARGIN_LENDING_RATIO = '/api/v5/rubik/stat/margin/loan-ratio'
LONG_SHORT_RATIO = '/api/v5/rubik/stat/contracts/long-short-account-ratio'
CONTRACTS_INTEREST_VOLUME = '/api/v5/rubik/stat/contracts/open-interest-volume'
OPTIONS_INTEREST_VOLUME = '/api/v5/rubik/stat/option/open-interest-volume'
PUT_CALL_RATIO = '/api/v5/rubik/stat/option/open-interest-volume-ratio'
OPEN_INTEREST_VOLUME_EXPIRY = '/api/v5/rubik/stat/option/open-interest-volume-expiry'
INTEREST_VOLUME_STRIKE = '/api/v5/rubik/stat/option/open-interest-volume-strike'
TAKER_FLOW = '/api/v5/rubik/stat/option/taker-block-volume'

# TRADE-Complete
PLACR_ORDER = '/api/v5/trade/order'
BATCH_ORDERS = '/api/v5/trade/batch-orders'
CANAEL_ORDER = '/api/v5/trade/cancel-order'
CANAEL_BATCH_ORDERS = '/api/v5/trade/cancel-batch-orders'
AMEND_ORDER = '/api/v5/trade/amend-order'
AMEND_BATCH_ORDER = '/api/v5/trade/amend-batch-orders'
CLOSE_POSITION = '/api/v5/trade/close-position'
ORDER_INFO = '/api/v5/trade/order'
ORDERS_PENDING = '/api/v5/trade/orders-pending'
ORDERS_HISTORY = '/api/v5/trade/orders-history'
ORDERS_HISTORY_ARCHIVE = '/api/v5/trade/orders-history-archive'
ORDER_FILLS = '/api/v5/trade/fills'
ORDERS_FILLS_HISTORY = '/api/v5/trade/fills-history'
PLACE_ALGO_ORDER = '/api/v5/trade/order-algo'
CANCEL_ALGOS = '/api/v5/trade/cancel-algos'
Cancel_Advance_Algos = '/api/v5/trade/cancel-advance-algos'
ORDERS_ALGO_OENDING = '/api/v5/trade/orders-algo-pending'
ORDERS_ALGO_HISTORY = '/api/v5/trade/orders-algo-history'
GET_ALGO_ORDER_DETAILS = '/api/v5/trade/order-algo'
AMEND_ALGO_ORDER = '/api/v5/trade/amend-algos'

EASY_CONVERT_CURRENCY_LIST = '/api/v5/trade/easy-convert-currency-list'
EASY_CONVERT = '/api/v5/trade/easy-convert'
CONVERT_EASY_HISTORY = '/api/v5/trade/easy-convert-history'
ONE_CLICK_REPAY_SUPPORT = '/api/v5/trade/one-click-repay-currency-list'
ONE_CLICK_REPAY = '/api/v5/trade/one-click-repay'
ONE_CLICK_REPAY_HISTORY = '/api/v5/trade/one-click-repay-history'


# SubAccount-complete-testwriteComplete
BALANCE = '/api/v5/account/subaccount/balances'
BILLs = '/api/v5/asset/subaccount/bills'
RESET = '/api/v5/users/subaccount/modify-apikey'
VIEW_LIST = '/api/v5/users/subaccount/list'
SUBACCOUNT_TRANSFER = '/api/v5/asset/subaccount/transfer'
ENTRUST_SUBACCOUNT_LIST = '/api/v5/users/entrust-subaccount-list' #need to add
SET_TRSNSFER_OUT = '/api/v5/users/subaccount/set-transfer-out' #need to add
GET_ASSET_SUBACCOUNT_BALANCE = '/api/v5/asset/subaccount/balances' #need to add
GET_THE_USER_AFFILIATE_REBATE = '/api/v5/users/partner/if-rebate'
SET_SUB_ACCOUNTS_VIP_LOAN = '/api/v5/account/subaccount/set-loan-allocation'
GET_SUB_ACCOUNT_BORROW_INTEREST_AND_LIMIT = '/api/v5/account/subaccount/interest-limits'

# Broker-all need to implmented-completed
BROKER_INFO = '/api/v5/broker/nd/info'
CREATE_SUBACCOUNT = '/api/v5/broker/nd/create-subaccount'
DELETE_SUBACCOUNT = '/api/v5/broker/nd/delete-subaccount'
SUBACCOUNT_INFO = '/api/v5/broker/nd/subaccount-info'
SET_SUBACCOUNT_LEVEL = '/api/v5/broker/nd/set-subaccount-level'
SET_SUBACCOUNT_FEE_REAT = '/api/v5/broker/nd/set-subaccount-fee-rate'
SUBACCOUNT_DEPOSIT_ADDRESS = '/api/v5/asset/broker/nd/subaccount-deposit-address'
SUBACCOUNT_DEPOSIT_HISTORY = '/api/v5/asset/broker/nd/subaccount-deposit-history'
REBATE_DAILY = '/api/v5/broker/nd/rebate-daily'
ND_CREAET_APIKEY = '/api/v5/broker/nd/subaccount/apikey'
ND_SELECT_APIKEY = '/api/v5/broker/nd/subaccount/apikey'
ND_MODIFY_APIKEY = '/api/v5/broker/nd/subaccount/modify-apikey'
ND_DELETE_APIKEY = '/api/v5/broker/nd/subaccount/delete-apikey'
GET_REBATE_PER_ORDERS = '/api/v5/broker/nd/rebate-per-orders'
REBATE_PER_ORDERS = '/api/v5/broker/nd/rebate-per-orders'
MODIFY_SUBACCOUNT_DEPOSIT_ADDRESS = '/api/v5/asset/broker/nd/modify-subaccount-deposit-address'
GET_SUBACCOUNT_DEPOSIT='/api/v5/asset/broker/nd/subaccount-deposit-address'

# Convert-Complete
GET_CURRENCIES = '/api/v5/asset/convert/currencies'
GET_CURRENCY_PAIR = '/api/v5/asset/convert/currency-pair'
ESTIMATE_QUOTE = '/api/v5/asset/convert/estimate-quote'
CONVERT_TRADE = '/api/v5/asset/convert/trade'
CONVERT_HISTORY = '/api/v5/asset/convert/history'

# FDBroker -completed
FD_GET_REBATE_PER_ORDERS = '/api/v5/broker/fd/rebate-per-orders'
FD_REBATE_PER_ORDERS = '/api/v5/broker/fd/rebate-per-orders'

# Rfq/BlcokTrading-completed
COUNTERPARTIES = '/api/v5/rfq/counterparties'
CREATE_RFQ = '/api/v5/rfq/create-rfq'
CANCEL_RFQ = '/api/v5/rfq/cancel-rfq'
CANCEL_BATCH_RFQS = '/api/v5/rfq/cancel-batch-rfqs'
CANCEL_ALL_RSQS = '/api/v5/rfq/cancel-all-rfqs'
EXECUTE_QUOTE = '/api/v5/rfq/execute-quote'
CREATE_QUOTE = '/api/v5/rfq/create-quote'
CANCEL_QUOTE = '/api/v5/rfq/cancel-quote'
CANCEL_BATCH_QUOTES = '/api/v5/rfq/cancel-batch-quotes'
CANCEL_ALL_QUOTES = '/api/v5/rfq/cancel-all-quotes'
GET_RFQS = '/api/v5/rfq/rfqs'
GET_QUOTES = '/api/v5/rfq/quotes'
GET_RFQ_TRADES = '/api/v5/rfq/trades'
GET_PUBLIC_TRADES = '/api/v5/rfq/public-trades'
MMP_RESET = '/api/v5/rfq/mmp-reset'
MARKER_INSTRUMENT_SETTING = '/api/v5/rfq/maker-instrument-settings'


# tradingBot-Grid-complete-testcomplete
GRID_ORDER_ALGO = '/api/v5/tradingBot/grid/order-algo'
GRID_AMEND_ORDER_ALGO = '/api/v5/tradingBot/grid/amend-order-algo'
GRID_STOP_ORDER_ALGO = '/api/v5/tradingBot/grid/stop-order-algo'
GRID_ORDERS_ALGO_PENDING = '/api/v5/tradingBot/grid/orders-algo-pending'
GRID_ORDERS_ALGO_HISTORY = '/api/v5/tradingBot/grid/orders-algo-history'
GRID_ORDERS_ALGO_DETAILS = '/api/v5/tradingBot/grid/orders-algo-details'
GRID_SUB_ORDERS = '/api/v5/tradingBot/grid/sub-orders'
GRID_POSITIONS = '/api/v5/tradingBot/grid/positions'
GRID_WITHDRAW_INCOME = '/api/v5/tradingBot/grid/withdraw-income'
#--------need to add:
GRID_COMPUTE_MARIGIN_BALANCE = '/api/v5/tradingBot/grid/compute-margin-balance'
GRID_MARGIN_BALANCE = '/api/v5/tradingBot/grid/margin-balance'
GRID_AI_PARAM = '/api/v5/tradingBot/grid/ai-param'
PLACE_RECURRING_BUY_ORDER = '/api/v5/tradingBot/recurring/order-algo'
AMEND_RECURRING_BUY_ORDER = '/api/v5/tradingBot/recurring/amend-order-algo'
STOP_RECURRING_BUY_ORDER = '/api/v5/tradingBot/recurring/stop-order-algo'
GET_RECURRING_BUY_ORDER_LIST = '/api/v5/tradingBot/recurring/orders-algo-pending'
GET_RECURRING_BUY_ORDER_HISTORY = '/api/v5/tradingBot/recurring/orders-algo-history'
GET_RECURRING_BUY_ORDER_DETAILS = '/api/v5/tradingBot/recurring/orders-algo-details'
GET_RECURRING_BUY_SUB_ORDERS = '/api/v5/tradingBot/recurring/sub-orders'

#stacking - all need to implement-testcomplete
STACK_DEFI_OFFERS = '/api/v5/finance/staking-defi/offers'
STACK_DEFI_PURCHASE = '/api/v5/finance/staking-defi/purchase'
STACK_DEFI_REDEEM = '/api/v5/finance/staking-defi/redeem'
STACK_DEFI_CANCEL = '/api/v5/finance/staking-defi/cancel'
STACK_DEFI_ORDERS_ACTIVITY = '/api/v5/finance/staking-defi/orders-active'
STACK_DEFI_ORDERS_HISTORY = '/api/v5/finance/staking-defi/orders-history'
GET_SAVING_BALANCE = '/api/v5/finance/savings/balance'
SAVING_PURCHASE_REDEMPTION = '/api/v5/finance/savings/purchase-redempt'
SET_LENDING_RATE = '/api/v5/finance/savings/set-lending-rate'
GET_LENDING_HISTORY = '/api/v5/finance/savings/lending-history'
GET_PUBLIC_BORROW_INFO = '/api/v5/finance/savings/lending-rate-summary'
GET_PUBLIC_BORROW_HISTORY = '/api/v5/finance/savings/lending-rate-history'

# status-complete
STATUS = '/api/v5/system/status'

#Copy Trading
GET_EXISTING_LEADING_POSITIONS = '/api/v5/copytrading/current-subpositions'
GET_LEADING_POSITIONS_HISTORY = '/api/v5/copytrading/subpositions-history'
PLACE_LEADING_STOP_ORDER = '/api/v5/copytrading/algo-order'
CLOSE_LEADING_POSITIONS = '/api/v5/copytrading/close-subposition'
GET_LEADING_POSITIONS = '/api/v5/copytrading/instruments'
AMEND_EXISTING_LEADING_POSITIONS = '/api/v5/copytrading/set-instruments'
GET_PROFIT_SHARING_DETAILS = '/api/v5/copytrading/profit-sharing-details'
GET_TOTAL_PROFIT_SHARING = '/api/v5/copytrading/total-profit-sharing'
GET_UNREALIZED_PROFIT_SHARING_DETAILS = '/api/v5/copytrading/unrealized-profit-sharing-details'

