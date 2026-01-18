import logging
import sys
from .config import settings
from .fx_converter import FXConverter
from .fake_data_generator import DataGenerator
from .uploader import BigQueryUploader

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PipelineOrchestrator")


def main():
    """Main function orchestrating the data pipeline steps."""
    try:
        logger.info(f"Pipeline started for Target Currency: {settings.target_currency}")

        fx = FXConverter(
            api_url=settings.exchange_api_url, target_currency=settings.target_currency
        )

        gen = DataGenerator()

        up = BigQueryUploader(
            project_id=settings.gcp_project_id,
            key_path=settings.gcp_key_path,
            location=settings.location,
        )

        rates = fx.get_rates()
        logger.info(f"Successfully retrieved rates for {len(rates)} currencies.")

        data = gen.generate_batch(
            n=settings.num_records, rates=rates, target_curr=settings.target_currency
        )
        logger.info(
            f"Generated {len(data)} synthetic records with explicit data types."
        )

        up.upload(df=data, dataset_id=settings.dataset_id, table_id=settings.table_id)

        logger.info("Pipeline execution completed successfully.")

    except EnvironmentError as ee:
        logger.error(f"Configuration error: {ee}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Critical pipeline failure: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
