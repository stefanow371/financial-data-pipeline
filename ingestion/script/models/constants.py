from enum import Enum


class CostCenter(Enum):
    IT = "IT"
    MARKETING = "Marketing"
    SALES = "Sales"
    HR = "HR"
    OPERATIONS = "Operations"

    @classmethod
    def list_values(cls):
        return [c.value for c in cls]


class TransactionStatus(Enum):
    PAID = "Paid"
    PENDING = "Pending"
    OVERDUE = "Overdue"
