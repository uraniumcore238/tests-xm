from typing import List

import pytest

from pydantic import ValidationError
from tests.conftest import client
from xm.models.order_models import OrderCreate, OrderResponse
from xm.models.validate_response_schema import validate_orders_response_schema


def test__create_order__product_name_and_quantity_should_be_correct(create_order):
    assert create_order.product_name == 'Test Product'
    assert create_order.quantity == 10


def test__create_order__if_product_name_is_integer_should_rase_error():
    with pytest.raises(ValidationError):
        order_data = OrderCreate(product_name=1)
        response = client.post("/orders/", json=order_data.dict())
        assert response.status_code == 200
        order = OrderResponse(**response.json())
        assert order.product_name == 1


def test__read_order__order_id_should_be_correct(create_order):
    order_id = create_order.id
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test__update_order__product_name_and_quantity_should_correct(create_order):
    order_id = create_order.id
    update_data = {"product_name": "Updated Product", "quantity": 20}
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["product_name"] == "Updated Product"
    assert response.json()["quantity"] == 20


def test__delete_order__order_should_be_deleted(create_order):
    order_id = create_order.id
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404


def test_get_orders_should_has_correct_schema():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert validate_orders_response_schema(response) is True
