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

## Connecting desktop apps to the MCP server

The MCP server runs locally and can be exposed to desktop apps that support MCP. Use the same command and arguments for each app.

### 1. Claude Desktop

Add an MCP server entry to Claude Desktop's config file at:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Example:

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

Then restart Claude Desktop. After that, Claude can call the `get_schwab_snapshot` tool to retrieve current account and market data from Schwab.

### 2. Antigravity Desktop

If you use Antigravity Desktop, open its MCP or integrations settings and add a new server named `trading-with-claude` with the same local command and arguments:

```json
{
  "command": "/Users/cpatel/src/Projects/FinTech/TradingWithClaude/.venv/bin/python",
  "args": ["/Users/cpatel/src/Projects/FinTech/TradingWithClaude/mcp_server_stdio.py"]
}
```

If the app expects a full config object, place it under an `mcpServers` section using the same name and settings shown above. Save the config and restart Antigravity Desktop.

### 3. Troubleshooting

- Make sure the virtual environment path is correct.
- Confirm the server starts successfully with:

```bash
python mcp_server_stdio.py
```

- If the app does not detect the server, restart the app after changing its config.

## Security notes

- Keep your Schwab credentials and token file local.
- Do not commit the token file or `.env`.
