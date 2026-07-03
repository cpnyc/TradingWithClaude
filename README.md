# TradingWithClaude

A lightweight Python project for bringing Schwab account and market data into Claude through a local MCP server.

## Objective

Fetch account and market data from Schwab in Python, normalize it into a compact snapshot, and expose that snapshot to Claude via an MCP tool.

## What this repo contains

- Schwab OAuth helper: [schwab_auth.py](schwab_auth.py)
- Schwab client wrapper: [services/schwab/client.py](services/schwab/client.py)
- Snapshot normalization layer: [services/schwab/data_service.py](services/schwab/data_service.py)
- MCP server entry point: [mcp_server_stdio.py](mcp_server_stdio.py)
- Unit tests: [tests/test_schwab_data.py](tests/test_schwab_data.py)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your Schwab credentials in a local `.env` file:

```bash
SCHWAB_APP_KEY=...
SCHWAB_APP_SECRET=...
SCHWAB_CALLBACK_URL=https://127.0.0.1:8182
SCHWAB_TOKEN_PATH=data/schwab_token.json
```

4. Authenticate once:

```bash
python schwab_auth.py
```

5. Start the MCP server:

```bash
python mcp_server_stdio.py
```

## Claude Desktop usage

Add a server entry such as:

```json
{
  "mcpServers": {
    "trading-with-claude": {
      "command": "/Users/cpatel/src/Projects/FinTech/TradingWithClaude/.venv/bin/python",
      "args": ["/Users/cpatel/src/Projects/FinTech/TradingWithClaude/mcp_server_stdio.py"]
    }
  }
}
```

Claude can then call the `get_schwab_snapshot` tool to retrieve current account and market data from Schwab.

## Security notes

- Keep your Schwab credentials and token file local.
- Do not commit the token file or `.env`.
