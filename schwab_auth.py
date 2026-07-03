"""
schwab_auth.py — One-time Schwab OAuth flow using schwab-py.

Run once interactively to generate data/schwab_token.json.
After that, fetch_market_data.py auto-refreshes the token on every run.

Usage:
    python schwab_auth.py
"""
import schwab
from config import settings


def main() -> None:
    token_path = settings.token_path
    token_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting Schwab OAuth flow...")
    print(f"Token will be saved to: {token_path}")
    print(f"A browser window will open. Log in and approve access.\n")

    schwab.auth.client_from_login_flow(
        api_key=settings.SCHWAB_APP_KEY,
        app_secret=settings.SCHWAB_APP_SECRET,
        callback_url=settings.SCHWAB_CALLBACK_URL,
        token_path=str(token_path),
        interactive=False,
    )
    print(f"\nToken saved to {token_path}")
    print("You can now run: python mcp_server_stdio.py")


if __name__ == "__main__":
    main()
