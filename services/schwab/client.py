"""
services/schwab/client.py

Singleton Schwab API client built from persisted OAuth token.
Token is auto-refreshed by schwab-py on every call — no manual refresh needed.

Usage:
    from services.schwab.client import get_schwab_client
    client = get_schwab_client()   # returns None if not configured
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger("trading.schwab.client")

_client = None
_initialized: bool = False

PROJECT_ROOT = Path(__file__).parent.parent.parent


def get_schwab_client():
    """
    Returns a configured schwab-py client, or None if Schwab is not configured.
    Initializes once and caches the instance — token refresh is handled by schwab-py.
    """
    global _client, _initialized
    if _initialized:
        return _client

    _initialized = True
    try:
        import schwab
        from config import settings

        if not settings.SCHWAB_APP_KEY or not settings.SCHWAB_APP_SECRET:
            logger.info("Schwab not configured — SCHWAB_APP_KEY/SECRET missing")
            return None

        token_path = Path(settings.SCHWAB_TOKEN_PATH)
        if not token_path.is_absolute():
            token_path = (PROJECT_ROOT / settings.SCHWAB_TOKEN_PATH).resolve()

        if not token_path.exists():
            logger.warning("Schwab token not found at %s — run: python schwab_auth.py", token_path)
            return None

        _client = schwab.auth.client_from_token_file(
            token_path=str(token_path),
            api_key=settings.SCHWAB_APP_KEY,
            app_secret=settings.SCHWAB_APP_SECRET,
        )
        logger.info("Schwab client initialized from token file")
        return _client

    except Exception as e:
        logger.error("Schwab client init failed: %s", e, exc_info=True)
        return None


def is_schwab_available() -> bool:
    return get_schwab_client() is not None
