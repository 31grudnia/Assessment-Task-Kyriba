import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logger.logger import setup_logger
from librarian.config import DATABASE_URL
from librarian.database.database import Base
from librarian.database.models.file import HeaderModel, FooterModel, TransactionModel, Currency


logger = setup_logger("database_init")

def init_db():
    logger.info("Starting database initialization")
    
    engine = create_engine(DATABASE_URL)
    
    logger.info("Resetting database schema (Drop/Create)")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    users = [
        ("John", "Doe", "A."),
        ("Alice", "Smith", "B."),
        ("Bob", "Jones", "C.")
    ]

    logger.info(f"Preparing to seed {len(users)} users")

    for name, surname, pat in users:
        logger.info(f"Seeding data for user: {name} {surname}")
        
        header = HeaderModel(
            name=name,
            surname=surname,
            patronymic=pat,
            address="123 Main St"
        )
        session.add(header)
        session.flush()

        footer = FooterModel(
            total_counter=3,
            header=header
        )
        session.add(footer)
        session.flush()

        for i in range(1, 4):
            tx = TransactionModel(
                counter=i,
                amount=random.randint(1000, 9999),
                currency=Currency.USD,
                header=header,
                footer=footer
            )
            session.add(tx)

    session.commit()
    session.close()
    logger.info("Database seeded successfully")

if __name__ == "__main__":
    init_db()