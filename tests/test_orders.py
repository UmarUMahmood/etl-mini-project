from src.order.core import create_order, update_order_status, update_order, delete_order

from unittest.mock import Mock, patch


@patch("os.system")
@patch("uuid.uuid4")
def test_create_order(mock_uuid4, mock_system):

    test_orders = []
    test_couriers = [
        {"courier_id": 0, "courier_name": "John", "courier_phone": "07111222333"}
    ]
    test_products = []

    mock_system.return_value = ""

    mock_uuid4.return_value = 0

    mock_input = Mock()
    mock_input.side_effect = ["Test Customer", "Test Address", "07111222333", 1]

    mock_print_couriers = Mock()
    mock_print_couriers.return_value = test_couriers

    def mock_select_products(test_products):
        return []

    def mock_update(conn, sql_create_product, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = create_order(
        test_orders,
        test_couriers,
        test_products,
        mock_input,
        mock_print_couriers,
        mock_select_products,
        mock_update,
        mock_connection,
        mock_print,
    )
    expected = [
        {
            "order_id": 0,
            "customer_name": "Test Customer",
            "customer_address": "Test Address",
            "customer_phone": "07111222333",
            "courier_id": 0,
            "status": "preparing",
        }
    ]
    assert actual == expected


def test_update_order_status():

    mock_print_orders = Mock()
    mock_print_orders.return_value = [
        {
            "transaction_id": 0,
            "customer_name": "Test Customer",
            "customer_address": "Test Address",
            "customer_phone": "07111222333",
            "courier_id": 0,
            "status": "preparing",
        }
    ]

    mock_input = Mock()
    mock_input.side_effect = [1, 2]

    def mock_update(conn, sql_create_product, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = update_order_status(
        mock_print_orders, mock_input, mock_update, mock_connection, mock_print
    )
    expected = [
        {
            "transaction_id": 0,
            "customer_name": "Test Customer",
            "customer_address": "Test Address",
            "customer_phone": "07111222333",
            "courier_id": 0,
            "status": "ready",
        }
    ]
    assert actual == expected


def test_update_order():

    mock_print_orders = Mock()
    mock_print_orders.return_value = [
        {
            "transaction_id": 0,
            "customer_name": "Test Customer",
            "customer_address": "Test Address",
            "customer_phone": "07111222333",
            "courier_id": 0,
            "status": "preparing",
        }
    ]

    mock_input = Mock()
    mock_input.side_effect = [1, "Updated Customer", "Updated Address", "07333222111"]

    def mock_update(conn, sql_create_product, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = update_order(
        mock_print_orders, mock_input, mock_update, mock_connection, mock_print
    )
    expected = [
        {
            "transaction_id": 0,
            "customer_name": "Updated Customer",
            "customer_address": "Updated Address",
            "customer_phone": "07333222111",
            "courier_id": 0,
            "status": "preparing",
        }
    ]
    assert actual == expected


def test_delete_order():

    mock_print_orders = Mock()
    mock_print_orders.return_value = [
        {
            "transaction_id": 0,
            "customer_name": "Test Customer",
            "customer_address": "Test Address",
            "customer_phone": "07111222333",
            "courier_id": 0,
            "status": "preparing",
        }
    ]

    mock_input = Mock()
    mock_input.side_effect = [1]

    def mock_update(conn, sql_create_product, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = delete_order(
        mock_print_orders, mock_input, mock_update, mock_connection, mock_print
    )
    expected = []
    assert actual == expected