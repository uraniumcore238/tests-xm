from xm.models.order_models import OrderResponse


def validate_orders_response_schema(response):
    try:
        orders = response.json()
        for order in orders:
            try:
                OrderResponse(**order)
            except Exception:
                return False
        return True
    except Exception:
        return False