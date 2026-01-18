import os
import logging
from functools import cached_property

logger = logging.getLogger("Config")


class Settings:
    """Configuration class fetching settings from environment variables."""

    def _get_env(self, var_name: str, mandatory: bool = True) -> str:
        """Helper to get environment variables with optional mandatory check."""
        value = os.getenv(var_name)
        if mandatory and not value:
            logger.error(f"Missing mandatory environment variable: {var_name}")
            raise EnvironmentError(f"Mandatory variable {var_name} not set.")
        return value or ""

    @cached_property
    def gcp_project_id(self) -> str:
        return self._get_env("GCP_PROJECT_ID")

    @cached_property
    def gcp_key_path(self) -> str:
        return self._get_env("GCP_KEY_PATH")

    @property
    def target_currency(self) -> str:
        curr = self._get_env("TARGET_CURRENCY", mandatory=False) or "USD"
        return curr.upper()

    @property
    def exchange_api_url(self) -> str:
        return (
            self._get_env("EXCHANGE_API_URL", mandatory=False)
            or "https://api.frankfurter.app"
        )

    @property
    def num_records(self) -> int:
        val = self._get_env("NUM_RECORDS", mandatory=False) or "50000"
        return int(val)

    @property
    def dataset_id(self) -> str:
        return self._get_env("DATASET_ID", mandatory=False) or "finance_raw"

    @property
    def table_id(self) -> str:
        return self._get_env("TABLE_ID", mandatory=False) or "transactions"

    @property
    def location(self) -> str:
        return self._get_env("GCP_LOCATION", mandatory=False) or "EU"


settings = Settings()
