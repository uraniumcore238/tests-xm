import os
import pytest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from xm.orders import app
from xm.models.order_models import OrderCreate, OrderResponse

client = TestClient(app)
BASE_URL = os.getenv('BASE_DOMAIN')
load_dotenv()


@pytest.fixture
def create_order():
    order_data = OrderCreate(product_name="Test Product", quantity=10)
    response = client.post("/orders/", json=order_data.dict())
    order = OrderResponse(**response.json())
    yield order
    client.delete(f"/orders/{order.id}")


