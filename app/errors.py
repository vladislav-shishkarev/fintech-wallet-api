class UserNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f'User not found: ID {self.id}')


class WalletNotFoundError(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f'Wallet not found: ID {self.id}')