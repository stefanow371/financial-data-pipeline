import logging
import os
import random
from dataclasses import asdict, dataclass
from enum import Enum
from typing import List, Optional

import pandas as pd
import pandas_gbq as pdgbq
from dotenv import load_dotenv
from faker import Faker
from google.oauth2 import service_account

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("DataIngestor")


@dataclass
class Transaction:
    """Dataclass representing a single financial transaction."""

    transaction_id: str
    date: pd.Timestamp
    amount: float
    currency: str
    cost_center: str
    status: str
    vendor: str


class TransactionStatus(Enum):
    PAID = "Paid"
    OVERDUE = "Overdue"
    PENDING = "Pending"
    CANCELLED = "Cancelled"


class DataIngestor:
    """Generic class for generating and uploading synthetic data to BigQuery."""

    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.key_path = os.getenv("GCP_KEY_PATH")
        self.dataset_id = os.getenv("DATASET_ID", "finance_raw")
        self.table_id = os.getenv("TABLE_ID", "transactions")
        self.location = os.getenv("GCP_LOCATION", "EU")

        self.fake = Faker()

        if not self.project_id or not self.key_path:
            logger.error("Configuration error: GCP_PROJECT_ID or GCP_KEY_PATH missing.")
            raise EnvironmentError("Missing required environment variables.")

    def generate_synthetic_data(self, n_records: int = 5000) -> pd.DataFrame:
        """Generates a DataFrame with synthetic financial transactions."""

        logger.info(f"Starting generation of {n_records} synthetic records.")

        cost_centers = ["Marketing", "Sales", "IT", "Operations", "HR"]
        currencies = ["USD", "EUR", "PLN", "GBP"]

        transactions: List[Transaction] = []

        for _ in range(n_records):
            new_tx = Transaction(
                transaction_id=self.fake.uuid4(),
                date=pd.Timestamp(
                    self.fake.date_between(start_date="-1y", end_date="today")
                ),
                amount=round(random.uniform(10.0, 5000.0), 2),
                currency=random.choice(currencies),
                cost_center=random.choice(cost_centers),
                status=random.choice(list(TransactionStatus)).value,
                vendor=self.fake.company(),
            )
            transactions.append(new_tx)

        df = pd.DataFrame([asdict(tx) for tx in transactions])

        logger.info("Synthetic data generation completed.")
        return df

    def upload_to_big_query(
        self,
        df: pd.DataFrame,
        dataset: Optional[str] = None,
        table: Optional[str] = None,
    ) -> None:
        """Uploads the provided DataFrame to BigQuery using Service Account credentials."""

        # Użyj parametrów lub wartości domyślnych z inicjalizacji
        target_dataset = dataset or self.dataset_id
        target_table = table or self.table_id
        destination = f"{target_dataset}.{target_table}"

        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.key_path
            )

            logger.info(f"Uploading {len(df)} rows to BigQuery: {destination}")

            pdgbq.to_gbq(
                df,
                destination_table=destination,
                project_id=self.project_id,
                if_exists="replace",
                credentials=credentials,
                location=self.location,
            )

            logger.info("Upload to BigQuery completed successfully.")

        except Exception as e:
            logger.error(f"Critical error during BigQuery upload: {e}")
            raise


if __name__ == "__main__":
    n_to_generate = int(os.getenv("NUM_RECORDS", 5000))
    ingestor = DataIngestor()
    data_df = ingestor.generate_synthetic_data(n_to_generate)
    ingestor.upload_to_big_query(data_df)
