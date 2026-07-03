from __future__ import annotations

import json
from typing import Any


def normalize_account_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Convert Schwab account payload into a simple structure for Claude."""
    accounts = payload.get("accounts", []) or []
    normalized_accounts: list[dict[str, Any]] = []

    for account in accounts:
        balances = account.get("currentBalances", {}) or {}
        normalized_accounts.append(
            {
                "account_number": account.get("accountNumber"),
                "account_type": account.get("type"),
                "cash_balance": balances.get("cashBalance"),
                "long_market_value": balances.get("longMarketValue"),
                "short_market_value": balances.get("shortMarketValue"),
                "total_value": balances.get("totalValue"),
            }
        )

    return {"accounts": normalized_accounts}


def normalize_quotes_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Convert Schwab quotes payload into a compact quote map."""
    quotes: dict[str, Any] = {}
    for symbol, response in payload.items():
        quote = (response or {}).get("quote", {}) or {}
        last_price = quote.get("lastPrice") or quote.get("mark") or 0.0
        previous_close = quote.get("closePrice") or last_price
        change_pct = 0.0
        if previous_close:
            change_pct = round(((float(last_price) - float(previous_close)) / float(previous_close)) * 100 + 1e-9, 2)

        quotes[symbol] = {
            "price": float(last_price),
            "change_pct": change_pct,
            "previous_close": float(previous_close),
            "raw": quote,
        }

    return quotes


def build_schwab_snapshot(account_payload: dict[str, Any], market_payload: dict[str, Any]) -> dict[str, Any]:
    """Create a single snapshot structure for Claude/MCP use."""
    return {
        "account": normalize_account_payload(account_payload),
        "market": {"symbols": normalize_quotes_payload(market_payload)},
        "generated_at": None,
    }


def format_schwab_snapshot(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2, default=str)
