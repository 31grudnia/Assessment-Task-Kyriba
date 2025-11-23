from librarian.database.database import Base
from librarian.database.models.currency import Currency

from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import mapped_column, relationship, Mapped

from typing import List

class HeaderModel(Base):
    __tablename__ = "header"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(28))
    surname: Mapped[str] = mapped_column(String(30))
    patronymic: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(30))

    footer: Mapped["FooterModel"] = relationship(back_populates="header",
                                                 cascade="all, delete-orphan")
    
    transactions: Mapped[List["TransactionModel"]] = relationship(back_populates="header",
                                                                  cascade="all, delete-orphan")
    

class TransactionModel(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    counter: Mapped[int] = mapped_column()
    amount: Mapped[int] = mapped_column()
    currency: Mapped[Currency] = mapped_column(Enum(Currency))

    header_id: Mapped[int] = mapped_column(ForeignKey("header.id"))
    header: Mapped["HeaderModel"] = relationship(back_populates="transactions")

    footer_id: Mapped[int] = mapped_column(ForeignKey("footer.id"))
    footer: Mapped["FooterModel"] = relationship(back_populates="transactions")


class FooterModel(Base):
    __tablename__ = "footer"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_counter: Mapped[int] = mapped_column() 

    header_id: Mapped[int] = mapped_column(ForeignKey("header.id"))
    header: Mapped["HeaderModel"] = relationship(back_populates="footer", 
                                                 single_parent=True)
    
    transactions: Mapped[List["TransactionModel"]] = relationship(back_populates="footer",
                                                                  cascade="all, delete-orphan") 
