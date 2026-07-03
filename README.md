# TradingWithClaude

This project lets you connect your Schwab account data to Claude through a local MCP server. In simple terms, it helps Claude read your account and market information from your own computer.

If you are new to coding, do not worry. The setup below uses plain steps and copy-paste commands.

## What this project does

This repo contains a small Python app that:

- connects to Schwab,
- fetches account and market data,
- formats that data into a simple snapshot,
- and exposes it to Claude through a local tool called `get_schwab_snapshot`.

## What you need before you begin

Make sure you have:

- a computer with Python installed,
- a Schwab brokerage account,
- a Schwab developer account and API app,
- Claude Desktop or Antigravity Desktop installed if you want to use it with those apps.

## Architecture (simple data flow)

```text
Schwab login / token file
        |
        v
Schwab API
        |
        v
Python app
        |
        v
Simple snapshot format
        |
        v
Local MCP server
        |
        v
Claude Desktop / Antigravity Desktop
```

## Step-by-step setup

### 1. Download this repository to your computer

If you are using Git:

```bash
git clone https://github.com/cpnyc/TradingWithClaude.git
cd TradingWithClaude
```

If you do not use Git, you can download the project as a ZIP file from GitHub, then unzip it and open the folder in a terminal.

### 2. Open the project folder in a terminal

After downloading the repo, open a terminal and go into the project folder:

```bash
cd TradingWithClaude
```

### 3. Install Python

If Python is not already installed:

- download Python from https://www.python.org/downloads/
- install it and make sure to check the option to add Python to your PATH

You can verify it by opening a terminal and running:

```bash
python --version
```

If that does not work, try:

```bash
python3 --version
```

### 2. Open the project folder

In your terminal, go to the folder where you cloned or downloaded this repository.

Example:

```bash
cd /path/to/TradingWithClaude
```

### 3. Create a virtual environment

A virtual environment keeps this project isolated from other Python projects.

```bash
python -m venv .venv
```

Then activate it.

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install the required Python packages

Run:

```bash
pip install -r requirements.txt
```

### 5. Create your local environment file

Create a file named `.env` in the project folder. You can copy the example file first:

```bash
cp .env.example .env
```

Then open `.env` in a text editor and fill in your values.

Example:

```bash
SCHWAB_APP_KEY=your_app_key_here
SCHWAB_APP_SECRET=your_app_secret_here
SCHWAB_CALLBACK_URL=https://127.0.0.1:8182
SCHWAB_TOKEN_PATH=data/schwab_token.json
```

### 6. Get your Schwab credentials

To use this project, you need a Schwab API app.

1. Sign in to the Schwab developer portal at https://developer.schwab.com.
2. Create or open an API application.
3. Set the redirect URL to the same value you used in `.env`:

```bash
SCHWAB_CALLBACK_URL=https://127.0.0.1:8182
```

4. Copy the generated app key and app secret into your `.env` file.
5. Complete any approval or onboarding steps required by Schwab.

If your account is not approved for API access, the authentication flow will not work until that is completed.

### 7. Authenticate once with Schwab

Run:

```bash
python schwab_auth.py
```

This starts the one-time login flow and creates a token file at the path you set in `.env`.

### 8. Start the local MCP server

Run:

```bash
python mcp_server_stdio.py
```

If it starts successfully, the server is ready to be used by a desktop app.

## Connect it to desktop apps

The MCP server runs locally on your computer. You can connect it to apps that support MCP.

### Claude Desktop

Open the config file for Claude Desktop:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add a server entry like this:

```json
{
  "mcpServers": {
    "trading-with-claude": {
      "command": "/absolute/path/to/your/project/.venv/bin/python",
      "args": ["/absolute/path/to/your/project/mcp_server_stdio.py"]
    }
  }
}
```

Replace the paths with the actual location of your project on your computer.

Then restart Claude Desktop.

### Antigravity Desktop

Open the MCP or integrations settings in Antigravity Desktop and add a server named `trading-with-claude` with the same command and arguments.

Example:

```json
{
  "command": "/absolute/path/to/your/project/.venv/bin/python",
  "args": ["/absolute/path/to/your/project/mcp_server_stdio.py"]
}
```

Save the settings and restart the app.

## Troubleshooting

If something does not work, try these checks:

- Make sure Python is installed.
- Make sure the virtual environment is activated.
- Make sure `.env` contains the correct Schwab values.
- Make sure the server starts with:

```bash
python mcp_server_stdio.py
```

- If the desktop app does not see the server, restart the app after changing its config.

## License

This project is licensed under the MIT License. Copyright (c) 2026 Atrii, LLC.

## Security notes

- Keep your Schwab credentials and token file local.
- Do not commit your `.env` file or token file to Git.
- If you are unsure about a setting, keep the default values unless you know they should be changed.
