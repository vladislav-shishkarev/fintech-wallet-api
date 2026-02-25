from enum import StrEnum


class WalletStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class TransactionStatus(StrEnum):
    IN_PROCESS = "in_process"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class Currency(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    CNY = "CNY"