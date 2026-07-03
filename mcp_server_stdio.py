from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from services.schwab.client import get_schwab_client
from services.schwab.data_service import build_schwab_snapshot, format_schwab_snapshot

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

mcp = FastMCP("trading-with-claude")


async def fetch_schwab_snapshot(symbols: list[str] | None = None) -> dict[str, Any]:
    client = get_schwab_client()
    if client is None:
        return {
            "account": {"accounts": []},
            "market": {"symbols": {}},
            "generated_at": None,
            "error": "Schwab client unavailable. Run schwab_auth.py first.",
        }

    symbols = symbols or ["SPY", "QQQ", "NVDA", "AAPL", "MSFT"]

    account_payload = {}
    try:
        raw_accounts = client.get_accounts(fields=["positions", "balances"])
        account_payload = raw_accounts.json() if hasattr(raw_accounts, "json") else raw_accounts
    except Exception as exc:
        log.warning("Unable to fetch Schwab accounts: %s", exc)

    market_payload = {}
    try:
        raw_quotes = client.get_quotes(symbols)
        market_payload = raw_quotes.json() if hasattr(raw_quotes, "json") else raw_quotes
    except Exception as exc:
        log.warning("Unable to fetch Schwab quotes: %s", exc)

    snapshot = build_schwab_snapshot(account_payload, market_payload)
    snapshot["generated_at"] = asyncio.get_running_loop().time()
    return snapshot


@mcp.tool()
def get_schwab_snapshot(symbols: list[str] | None = None) -> str:
    """Return a compact account and market snapshot from Schwab for Claude."""
    snapshot = asyncio.run(fetch_schwab_snapshot(symbols=symbols))
    return format_schwab_snapshot(snapshot)


if __name__ == "__main__":
    mcp.run(transport="stdio")
