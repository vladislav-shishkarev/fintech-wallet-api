from decimal import Decimal

from pydantic import EmailStr

from app.enums import Currency, WalletStatus


class UserNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"User not found: ID {self.id}")


class WalletNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Wallet not found: ID {self.id}")


class TransactionNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Transaction not found: ID {self.id}")


class PhoneAlreadyExistsError(Exception):
    def __init__(self, phone: str):
        self.phone = phone
        super().__init__(f"Phone already exists: {self.phone}")


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: EmailStr):
        self.email = email
        super().__init__(f"Email already exists: {self.email}")


class NotEnoughMoneyError(Exception):
    def __init__(self, wallet_id: int, transaction_amount: Decimal):
        self.wallet_id = wallet_id
        self.transaction_amount = transaction_amount
        super().__init__(
            f"Not enough money for transaction: wallet ID {self.wallet_id}, transaction amount {self.transaction_amount}"
        )


class DifferentCurrencyError(Exception):
    def __init__(self, sender_currency: Currency, receiver_currency: Currency):
        self.sender_currency = sender_currency
        self.receiver_currency = receiver_currency
        super().__init__(
            f"Currency mismatch: sender wallet {self.sender_currency}, receiver wallet {self.receiver_currency}"
        )


class WalletNotActiveError(Exception):
    def __init__(self, id: int, status: WalletStatus):
        self.id = id
        self.status = status
        super().__init__(f"Wallet is not active: ID {self.id}, status {self.status}")


class WalletOverlapError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Sender and receiver wallet overlap: ID {self.id}")


class BalanceOverflowError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Balance limit exceeded: ID {self.id}")
