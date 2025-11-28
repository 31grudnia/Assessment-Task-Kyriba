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
    header1 = HeaderModel(name="John",
                          surname="Doe",
                          patronymic="A.",
                          address="123 Test St")
    db_session.add(header1)
    db_session.flush()

    footer1 = FooterModel(total_counter=2, 
                          control_sum=300, 
                          header=header1)
    db_session.add(footer1)

    tx1_1 = TransactionModel(counter=1, 
                             amount=100, 
                             currency=Currency.USD, 
                             header=header1, 
                             footer=footer1)
    tx1_2 = TransactionModel(counter=2, 
                             amount=200, 
                             currency=Currency.EUR, 
                             header=header1, 
                             footer=footer1)
    db_session.add_all([tx1_1, tx1_2])

    header2 = HeaderModel(name="Alice", 
                          surname="Wonder", 
                          patronymic="B.", 
                          address="456 Land")
    db_session.add(header2)
    db_session.flush()

    footer2 = FooterModel(total_counter=1, 
                          control_sum=500, 
                          header=header2)
    db_session.add(footer2)

    tx2_1 = TransactionModel(counter=1, 
                             amount=500, 
                             currency=Currency.USD, 
                             header=header2, 
                             footer=footer2)
    db_session.add(tx2_1)
    
    db_session.commit()
    return db_session