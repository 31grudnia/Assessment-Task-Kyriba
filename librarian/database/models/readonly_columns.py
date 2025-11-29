from librarian.database.database import Base

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import CheckConstraint



class ReadonlyColumns(Base):
    __tablename__ = "readonly_columns"
    
    __table_args__ = (
        CheckConstraint('id = 1', name='check_single_row'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    
    name: Mapped[bool] = mapped_column(default=False)
    surname: Mapped[bool] = mapped_column(default=False)
    patronymic: Mapped[bool] = mapped_column(default=False)
    address: Mapped[bool] = mapped_column(default=False)
    
    counter: Mapped[bool] = mapped_column(default=True)
    amount: Mapped[bool] = mapped_column(default=False)
    currency: Mapped[bool] = mapped_column(default=False)

    total_counter: Mapped[bool] = mapped_column(default=True)
    control_sum: Mapped[bool] = mapped_column(default=True)