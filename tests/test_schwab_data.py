import unittest

from services.schwab.data_service import build_schwab_snapshot, normalize_account_payload, normalize_quotes_payload


class SchwabDataServiceTests(unittest.TestCase):
    def test_normalize_account_payload_flattens_common_fields(self) -> None:
        payload = {
            "accounts": [
                {
                    "accountNumber": "123456",
                    "type": "INDIVIDUAL",
                    "currentBalances": {"cashBalance": 1250.5, "longMarketValue": 5000.0},
                }
            ]
        }

        result = normalize_account_payload(payload)

        self.assertEqual(result["accounts"][0]["account_number"], "123456")
        self.assertEqual(result["accounts"][0]["account_type"], "INDIVIDUAL")
        self.assertEqual(result["accounts"][0]["cash_balance"], 1250.5)
        self.assertEqual(result["accounts"][0]["long_market_value"], 5000.0)

    def test_normalize_quotes_payload_converts_schwab_response(self) -> None:
        payload = {
            "AAPL": {
                "quote": {
                    "lastPrice": 201.25,
                    "mark": 201.25,
                    "closePrice": 200.0,
                }
            }
        }

        result = normalize_quotes_payload(payload)

        self.assertEqual(result["AAPL"]["price"], 201.25)
        self.assertEqual(result["AAPL"]["change_pct"], 0.63)
        self.assertEqual(result["AAPL"]["previous_close"], 200.0)

    def test_build_schwab_snapshot_merges_account_and_market(self) -> None:
        account_payload = {"accounts": [{"accountNumber": "1", "type": "INDIVIDUAL", "currentBalances": {"cashBalance": 100.0}}]}
        market_payload = {"AAPL": {"quote": {"lastPrice": 100.0, "closePrice": 99.0}}}

        snapshot = build_schwab_snapshot(account_payload, market_payload)

        self.assertEqual(snapshot["account"]["accounts"][0]["account_number"], "1")
        self.assertEqual(snapshot["market"]["symbols"]["AAPL"]["price"], 100.0)
        self.assertEqual(snapshot["market"]["symbols"]["AAPL"]["change_pct"], 1.01)


if __name__ == "__main__":
    unittest.main()
