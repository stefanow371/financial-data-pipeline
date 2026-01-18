from dataclasses import dataclass
import pandas as pd


@dataclass
class Transaction:
    transaction_id: str
    transaction_date: pd.Timestamp
    amount_original: float
    currency_original: str
    amount_target: float
    currency_target: str
    cost_center: str
    vendor: str
    status: str
