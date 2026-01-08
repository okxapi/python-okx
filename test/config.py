"""
Test configuration module - loads API credentials from environment variables.

Usage:
    from test.config import get_api_credentials
    
    api_key, api_secret, passphrase, flag = get_api_credentials()
"""
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Flag to ensure .env is loaded only once
_env_loaded = False


def _load_env_once():
    """Load .env file only once, log any exceptions."""
    global _env_loaded
    if _env_loaded:
        return
    
    _env_loaded = True
    env_path = Path(__file__).parent.parent / '.env'
    
    try:
        from dotenv import load_dotenv
        if env_path.exists():
            load_dotenv(env_path)
            logger.debug(f"Loaded .env file from: {env_path}")
        else:
            logger.warning(f".env file not found at: {env_path}")
    except ImportError:
        logger.warning("python-dotenv not installed, relying on system environment variables")
    except Exception as e:
        logger.error(f"Failed to load .env file: {e}")


# Load .env when module is imported
_load_env_once()


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

