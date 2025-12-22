### Overview
This is an unofficial Python wrapper for the [OKX exchange v5 API](https://www.okx.com/okx-api)

If you came here looking to purchase cryptocurrencies from the OKX exchange, please go [here](https://www.okx.com/).

#### Source code
https://github.com/okxapi/python-okx
#### API trading tutorials
- Spot trading: https://www.okx.com/help/how-can-i-do-spot-trading-with-the-jupyter-notebook
- Derivative trading: https://www.okx.com/help/how-can-i-do-derivatives-trading-with-the-jupyter-notebook

Make sure you update often and check the [Changelog](https://www.okx.com/docs-v5/log_en/) for new features and bug fixes.

### Features
- Implementation of all Rest API endpoints.
- Private and Public Websocket implementation
- Testnet support 
- Websocket handling with reconnection and multiplexed connections

### Quick start
#### Prerequisites

`python version：>=3.7`

#### Step 1: Register an account on OKX and apply for an API key
- Register for an account: https://www.okx.com/account/register
- Apply for an API key: https://www.okx.com/account/users/myApi

#### Step 2: Install python-okx

```bash
pip install python-okx
```

### API Credentials

#### Option 1: Hardcoded credentials

```python
from okx import Account

account = Account.AccountAPI(
    api_key="your-api-key-here",
    api_secret_key="your-api-secret-here",
    passphrase="your-passphrase-here",
    flag="1",  # 0 = live trading, 1 = demo trading
    debug=False
)
```

#### Option 2: Using `.env` file (recommended)

Create a `.env` file in your project root:

```bash
OKX_API_KEY=your-api-key-here
OKX_API_SECRET=your-api-secret-here
OKX_PASSPHRASE=your-passphrase-here
OKX_FLAG=1
```

Then load it in your code:

```python
import os
from dotenv import load_dotenv
from okx import Account

load_dotenv()

account = Account.AccountAPI(
    api_key=os.getenv('OKX_API_KEY'),
    api_secret_key=os.getenv('OKX_API_SECRET'),
    passphrase=os.getenv('OKX_PASSPHRASE'),
    flag=os.getenv('OKX_FLAG', '1'),
    debug=False
)
```

### Development Setup

For contributors or local development:

```bash
# Clone the repository
git clone https://github.com/okxapi/python-okx.git
cd python-okx

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest test/unit/ -v
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
