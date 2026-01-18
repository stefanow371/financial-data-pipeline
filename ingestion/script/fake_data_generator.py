import random
from typing import List
from faker import Faker
from .models.constants import CostCenter, TransactionStatus
from .models.transaction import Transaction
import pandas as pd
import logging
from typing import Dict
from dataclasses import asdict


class DataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.cost_centers = CostCenter.list_values()
        self.logger = logging.getLogger(__name__)

    def generate_batch(
        self, n: int, rates: Dict[str, float], target_curr: str
    ) -> pd.DataFrame:
        logger = logging.getLogger("Generator")
        logger.info(f"Generating data with target currency: {target_curr}")

        transactions: List[Transaction] = []
        available_currencies = list(rates.keys())

        for _ in range(n):
            curr = random.choice(available_currencies)
            amt = round(random.uniform(10.0, 10000.0), 2)

            tx = Transaction(
                transaction_id=self.fake.uuid4(),
                transaction_date=pd.Timestamp(self.fake.date_between(start_date="-1y")),
                amount_original=amt,
                currency_original=curr,
                amount_target=round(amt * rates[curr], 2),
                currency_target=target_curr,
                cost_center=random.choice(self.cost_centers),
                vendor=self.fake.company(),
                status=random.choice(list(TransactionStatus)).value,
            )
            transactions.append(tx)

        return pd.DataFrame([asdict(t) for t in transactions])
