from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
 
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
 
initial_data = [
    {"product_name": "Product A", "quantity": 10},
    {"product_name": "Product B", "quantity": 5},
    {"product_name": "Product C", "quantity": 20}
]


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    quantity = Column(Integer)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_initial_data(db: Session):
    for data in initial_data:
        db_order = Order(**data)
        db.add(db_order)
    db.commit()
