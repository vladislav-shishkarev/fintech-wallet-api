from datetime import datetime
from decimal import Decimal
from typing import List
from sqlalchemy import String, DateTime, ForeignKey, DECIMAL, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from main.app.db import Base
from main.app.schemas import WalletStatus, TransactionStatus, Currency


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(),
                                                 nullable=False)
    wallets: Mapped[List["Wallet"]] = relationship("Wallet", back_populates="owner", cascade="all, delete")


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Ссылка на таблицу users
    status: Mapped[WalletStatus] = mapped_column(SAEnum(WalletStatus, native_enum=False), nullable=False)
    currency: Mapped[Currency] = mapped_column(SAEnum(Currency, native_enum=False), nullable=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(11, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(),
                                                 nullable=False)
    name: Mapped[str] = mapped_column(String(100))

    owner: Mapped["User"] = relationship("User", back_populates="wallets")
    sent_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_wallet_id",
        back_populates="sender_wallet"
    )
    received_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_wallet_id",
        back_populates="receiver_wallet"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    receiver_wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    status: Mapped[TransactionStatus] = mapped_column(SAEnum(TransactionStatus, native_enum=False), nullable=False)
    currency: Mapped[Currency] = mapped_column(SAEnum(Currency, native_enum=False), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(11, 2), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(),
                                                nullable=False)
    comment: Mapped[str] = mapped_column(String(256), nullable=True)
    sender_wallet: Mapped["Wallet"] = relationship(
        "Wallet",
        foreign_keys=sender_wallet_id,
        back_populates="sent_transactions"
    )
    receiver_wallet: Mapped["Wallet"] = relationship(
        "Wallet",
        foreign_keys=receiver_wallet_id,
        back_populates="received_transactions"
    )