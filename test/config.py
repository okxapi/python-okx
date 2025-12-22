"""
Test configuration module - loads API credentials from environment variables.

Usage:
    from test.config import get_api_credentials
    
    api_key, api_secret, passphrase, flag = get_api_credentials()
"""
import os
from pathlib import Path

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, rely on system environment variables


def get_api_credentials():
    """
    Get API credentials from environment variables.
    
    Returns:
        tuple: (api_key, api_secret, passphrase, flag)
    """
    api_key = os.getenv('OKX_API_KEY', '')
    api_secret = os.getenv('OKX_API_SECRET', '')
    passphrase = os.getenv('OKX_PASSPHRASE', '')
    flag = os.getenv('OKX_FLAG', '1')  # Default to demo trading
    
    return api_key, api_secret, passphrase, flag

