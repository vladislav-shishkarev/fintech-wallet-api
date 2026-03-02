from pydantic import EmailStr


class UserNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f'User not found: ID {self.id}')


class WalletNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f'Wallet not found: ID {self.id}')


class PhoneAlreadyExistsError(Exception):
    def __init__(self, phone: str):
        self.phone = phone
        super().__init__(f'Phone already exists: {self.phone}')


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: EmailStr):
        self.email = email
        super().__init__(f'Email already exists: {self.email}')