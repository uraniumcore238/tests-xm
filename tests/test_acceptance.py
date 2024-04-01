import os

import allure
import httpx
import pytest
from dotenv import load_dotenv
from pydantic import ValidationError
from xm.models.order_models import OrderCreate, OrderResponse, OrderUpdate

load_dotenv()
main_app_url = os.getenv('BASE_DOMAIN')


@allure.tag('ID 1')
@allure.severity(severity_level='critical')
@allure.story('Order creation')
@allure.suite('Product name')
@allure.title('Response should be correct if product name is a string')
@pytest.mark.parametrize('product_name', [
    'Test Product',
    'T',
    '',
    ' ',
    'Product#$%',
    '!@#$%^&*()_+~`=-0987654321/.,;[]',
    '1',
    'test@test.com',
    '<script>alert</script>'
])
def test_response_should_be_correct_on_order_creation_if_product_name_is_str(product_name):
    payload = OrderCreate(product_name=product_name, quantity=10)
    response = httpx.Client().post(f'{main_app_url}/orders', json=payload.dict(), follow_redirects=True)
    assert response.status_code == 200
    assert response.json()['product_name'] == product_name


@allure.tag('ID 2')
@allure.severity(severity_level='critical')
@allure.story('Order creation')
@allure.suite('Quantity')
@allure.title('Response should be correct if quantity is integer')
@pytest.mark.parametrize('quantity', [
    1,
    0,
    10,
    10000000,
    -1,
    1.0
])
def test_response_should_be_correct_on_order_creation_if_quantity_is_digit(quantity):
    payload = OrderCreate(product_name='Test Product', quantity=quantity)
    response = httpx.Client().post(f"{main_app_url}/orders", json=payload.dict(), follow_redirects=True)
    assert response.status_code == 200
    assert response.json()['quantity'] == quantity


@allure.tag('ID 3')
@allure.severity(severity_level='critical')
@allure.story('Order creation')
@allure.suite('Quantity')
@allure.title('Response should return ValidationError if quantity is a fractional number')
@pytest.mark.parametrize('quantity', [
    0.1,
    10.1,
    -0.1,
    00.01,
    '1.1'
])
def test_response_should_return_validation_error_if_quantity_is_fractional_number(quantity):
    with pytest.raises(ValidationError):
        payload = OrderCreate(product_name='Test Product', quantity=quantity)
        response = httpx.Client().post(f"{main_app_url}/orders", json=payload.dict(), follow_redirects=True)
        assert response.status_code == 200
        assert response.json()['quantity'] == quantity


@allure.tag('ID 4')
@allure.severity(severity_level='critical')
@allure.story('Order creation')
@allure.suite('Product name')
@allure.title('Response should return ValidationError if product name is not a string')
@pytest.mark.parametrize('order_name', [
    1,
    1.0,
    100.9,
    ['Test'],
    {'test': 'test'},
    ('Test')
])
def test_response_should_return_validation_error_if_order_name_is_not_a_string(order_name):
    with pytest.raises(ValidationError):
        payload = OrderCreate(product_name=order_name, quantity=10)
        response = httpx.Client().post(f"{main_app_url}/orders", json=payload.dict(), follow_redirects=True)
        assert response.status_code == 200
        assert response.json()['product_name'] == order_name


@allure.tag('ID 5')
@allure.severity(severity_level='critical')
@allure.story('Order reading')
@allure.suite('Product name')
@allure.title('Response should be correct if product name is correct')
def test_response_should_return_order_with_correct_schema():
    response = httpx.Client().get(f"{main_app_url}/orders/1", follow_redirects=True)
    assert response.status_code == 200
    OrderResponse(**response.json())


@allure.tag('ID 6')
@allure.severity(severity_level='critical')
@allure.story('Order updating')
@allure.suite('Product name')
@allure.title('Response should return correct product_name and quantity on updating order')
def test_response_should_return_correct_product_name_and_quantity():
    product_name = 'Change name'
    quantity = 99
    payload = OrderUpdate(product_name=product_name, quantity=quantity)
    response = httpx.Client().put(f"{main_app_url}/orders/2", json=payload.dict(), follow_redirects=True)
    assert response.status_code == 200
    assert response.json()['product_name'] == product_name
    assert response.json()['quantity'] == quantity


@allure.tag('ID 7')
@allure.severity(severity_level='critical')
@allure.story('Order updating')
@allure.suite('Product id')
@allure.title('Response should return 404 error if there is no such order to update')
def test_response_should_return_404_error_if_there_is_no_such_order_to_update():
    product_name = 'Change name'
    quantity = 99
    payload = OrderUpdate(product_name=product_name, quantity=quantity)
    response = httpx.Client().put(f"{main_app_url}/orders/1000", json=payload.dict(), follow_redirects=True)
    assert response.status_code == 404


@allure.tag('ID 8')
@allure.severity(severity_level='critical')
@allure.story('Order reading')
@allure.suite('Product id')
@allure.title('Response should return 404 error if there is no such order to read')
def test_response_should_return_404_error_if_there_is_no_such_order_to_read():
    response = httpx.Client().get(f"{main_app_url}/orders/1000", follow_redirects=True)
    assert response.status_code == 404


@allure.tag('ID 9')
@allure.severity(severity_level='critical')
@allure.story('Order reading')
@allure.suite('Product id')
@allure.title('Response should return 404 error if there is no such order to read')
def test_get_response_should_return_404_error_if_new_order_was_deleted_successfully():
    payload = OrderCreate()
    response = httpx.Client().post(f"{main_app_url}/orders", json=payload.dict(), follow_redirects=True)
    assert response.status_code == 200
    product_id = response.json()['id']
    response = httpx.Client().delete(f"{main_app_url}/orders/{product_id}", follow_redirects=True)
    assert response.status_code == 200
    response = httpx.Client().get(f"{main_app_url}/orders/{product_id}", follow_redirects=True)
    assert response.status_code == 404


@allure.tag('ID 9')
@allure.severity(severity_level='critical')
@allure.story('Orders reading')
@allure.suite('Product id')
@allure.title('Response should return correct schema on get all orders')
def test_response_should_return_correct_schema_on_get_all_orders():
    response = httpx.Client().get(f"{main_app_url}/orders/", follow_redirects=True)
    assert response.status_code == 200
    # OrderResponse(**response.json()
