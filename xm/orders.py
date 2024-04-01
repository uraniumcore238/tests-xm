from typing import List
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from xm.database.database_creation import Base, engine, SessionLocal, Order, insert_initial_data, get_db
from xm.models.order_models import OrderResponse, OrderCreate, OrderUpdate

Base.metadata.create_all(bind=engine)
app = FastAPI()


# CRUD operations
@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    for var, value in vars(order).items():
        setattr(db_order, var, value) if value is not None else None
    db.commit()
    db.refresh(db_order)
    return db_order


@app.delete("/orders/{order_id}", response_model=OrderResponse)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(order)
    db.commit()
    return order


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    insert_initial_data(db)
    db.close()
