import pandas_gbq as pdgbq
from google.oauth2 import service_account
import logging


class BigQueryUploader:
    def __init__(self, project_id: str, key_path: str, location: str):
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(
            key_path
        )
        self.location = location

    def upload(self, df, dataset_id, table_id):
        destination = f"{dataset_id}.{table_id}"
        logging.info(f"Uploading to BigQuery: {destination}")
        pdgbq.to_gbq(
            df,
            destination_table=destination,
            project_id=self.project_id,
            credentials=self.credentials,
            if_exists="replace",
            location=self.location,
        )
