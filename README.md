### Overview
This is an unofficial Python wrapper for the [OKX exchange v5 API](https://www.okx.com/okx-api)

If you came here looking to purchase cryptocurrencies from the OKX exchange, please go [here](https://www.okx.com/).

#### Source code
https://github.com/okxapi/python-okx
#### OKX API Telegram
https://t.me/OKXAPI
#### API trading tutorials
- Spot trading: https://www.okx.com/learn/spot-trading-with-jupyter-notebook
- Derivative trading: https://www.okx.com/learn/derivatives-trading-with-jupyter-notebook

Make sure you update often and check the [Changelog](https://www.okx.com/docs-v5/log_en/) for new features and bug fixes.

### Features
- Implementation of all Rest API endpoints.
- Private and Public Websocket implementation
- Testnet support 
- Websocket handling with reconnection and multiplexed connections

### Quick start
#### Prerequisites

`python version：>=3.9`

`WebSocketAPI： websockets package advise version 6.0`

#### Step 1: register an account on OKX and apply for an API key
- Register for an account: https://www.okx.com/account/register
- Apply for an API key: https://www.okx.com/account/users/myApi

#### Step 2: install python-okx

```python
pip install python-okx
```

#### Step 3: Run examples

- Fill in API credentials in the corresponding examples
```python 
api_key = ""
secret_key = ""
passphrase = ""
```
- RestAPI
  - For spot trading: run example/get_started_en.ipynb
  - For derivative trading: run example/trade_derivatives_en.ipynb
  - Tweak the value of the parameter `flag` (live trading: 0, demo trading: 1
) to switch between live and demo trading environment
- WebSocketAPI
  - Run test/WsPrivateTest.py for private websocket channels
  - Run test/WsPublicTest.py for public websocket channels
  - Use different URLs for different environment
      - Live trading URLs: https://www.okx.com/docs-v5/en/#overview-production-trading-services
      - Demo trading URLs: https://www.okx.com/docs-v5/en/#overview-demo-trading-services

Note 

- To learn more about OKX API, visit official [OKX API documentation](https://www.okx.com/docs-v5/en/)

- If you face any questions when using `WebSocketAPI`,you can consult the following links

  - `asyncio`、`websockets` document/`github`：

    ```python 
    https://docs.python.org/3/library/asyncio-dev.html
    https://websockets.readthedocs.io/en/stable/intro.html
    https://github.com/aaugustin/websockets
    ```

  - About `code=1006`：

    ```python 
    https://github.com/Rapptz/discord.py/issues/1996
    https://github.com/aaugustin/websockets/issues/587
    ```
