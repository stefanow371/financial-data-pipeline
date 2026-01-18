import requests
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class FXConverter:
    def __init__(self, api_url: str, target_currency: str):
        self.api_url = api_url
        self.target = target_currency

    def get_rates(self) -> Dict[str, float]:
        """Fetches FX rates relative to the target currency."""
        try:
            url = f"{self.api_url}{self.target}"
            logger.info(f"Fetching FX rates relative to {self.target}...")

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            rates = {curr: round(1 / rate, 6) for curr, rate in data["rates"].items()}
            rates[self.target] = 1.0

            return rates
        except Exception as e:
            logger.error(f"FX API Error: {e}. Check connectivity.")
            raise
