import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from librarian.database.database import Base
from librarian.database.models.file import HeaderModel, FooterModel, TransactionModel, Currency

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(url=TEST_DATABASE_URL, 
                           echo=True,
                           connect_args={"check_same_thread": False})
    
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, 
                                autoflush=False, 
                                bind=engine)
    session = SessionLocal()
    yield session   # pass session to tests

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def seeded_db(db_session):
    header = HeaderModel(
        name="John",
        surname="Doe",
        patronymic="A.",
        address="123 Test St"
    )
    db_session.add(header)
    db_session.flush()

    footer = FooterModel(
        total_counter=2,
        header=header
    )
    db_session.add(footer)
    db_session.flush()

    tx1 = TransactionModel(
        counter=1,
        amount=100,
        currency=Currency.USD,
        header=header,
        footer=footer
    )
    tx2 = TransactionModel(
        counter=2,
        amount=200,
        currency=Currency.EUR,
        header=header,
        footer=footer
    )
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    return db_session

