# TradingWithClaude PRD

## Version
- 2.1
- 2026-07-03

## Objective
Build a local Python service that connects to Schwab, retrieves account and market data, normalizes it into a compact snapshot, and exposes that snapshot to Claude through a local MCP server.

## Problem Statement
The repository no longer needs the older dashboard, portfolio, or event-tracking workflow. The current product focus is narrower: give Claude direct access to live Schwab account and market context so it can reason over real trading data.

## Goals
- Retrieve Schwab account data in Python.
- Retrieve Schwab market/quote data in Python.
- Normalize the data into a simple structure for Claude.
- Expose the data through an MCP tool named `get_schwab_snapshot`.
- Keep the solution local, simple, and dependency-light.

## Non-Goals
- Building a web dashboard
- Maintaining portfolio UI files
- Supporting charting or historical analytics
- Fetching non-Schwab data sources
- Placing trades or managing orders

## Scope

### In scope
- Schwab OAuth authentication
- Schwab account retrieval
- Schwab quote retrieval
- Snapshot normalization for Claude consumption
- Local MCP server integration
- Basic unit tests for the normalization layer

### Out of scope
- Order execution
- Portfolio management workflows
- Advanced options analytics
- Cloud deployment

## Architecture

```text
Schwab API -> Python service -> normalized snapshot -> MCP tool -> Claude
```

### Components
- [schwab_auth.py](../schwab_auth.py): one-time OAuth flow for Schwab token creation
- [services/schwab/client.py](../services/schwab/client.py): Schwab client wrapper
- [services/schwab/data_service.py](../services/schwab/data_service.py): normalization and snapshot formatting
- [mcp_server_stdio.py](../mcp_server_stdio.py): MCP server exposing `get_schwab_snapshot`

## Data Contract

The MCP tool returns a JSON object with this shape:

```json
{
  "account": {
    "accounts": [
      {
        "account_number": "123456",
        "account_type": "INDIVIDUAL",
        "cash_balance": 1250.5,
        "long_market_value": 5000.0,
        "short_market_value": 0.0,
        "total_value": 6250.5
      }
    ]
  },
  "market": {
    "symbols": {
      "AAPL": {
        "price": 201.25,
        "change_pct": 0.63,
        "previous_close": 200.0,
        "raw": {}
      }
    }
  },
  "generated_at": null
}
```

## User Flow
1. Configure Schwab credentials and authenticate once.
2. Start the MCP server locally.
3. Connect Claude Desktop to the server.
4. Ask Claude to call `get_schwab_snapshot`.
5. Claude receives a compact account and market snapshot from Schwab.

## Success Criteria
- The repo contains only the code needed for Schwab data retrieval and MCP exposure.
- Claude can retrieve a snapshot from Schwab using the MCP tool.
- The normalization layer is covered by tests.

## Implementation Notes
- Keep the service local and simple.
- Prefer compact JSON over large dashboard-style structures.
- Avoid introducing unrelated data sources or UI code.

