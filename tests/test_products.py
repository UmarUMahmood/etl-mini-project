from src.product.core import create_product, update_product, delete_product

from unittest.mock import Mock, patch


@patch("os.system")
@patch("uuid.uuid4")
def test_create_product(mock_uuid4, mock_system):

    test_products = []

    mock_system.return_value = ""

    mock_uuid4.return_value = 0

    mock_input = Mock()
    mock_input.side_effect = ["Pepsi", 0.8]

    mock_connection = Mock()

    def mock_update(conn, sql_create_product, values):
        pass

    mock_print = Mock()

    actual = create_product(
        test_products,
        mock_input,
        mock_update,
        mock_connection,
        mock_print,
    )
    expected = [{"product_id": 0, "product_name": "Pepsi", "product_price": 0.8}]
    assert actual == expected


def test_update_product():

    mock_print_products = Mock()
    mock_print_products.return_value = [
        {"product_id": 0, "product_name": "Pepso", "product_price": 0.1}
    ]
    mock_input = Mock()
    mock_input.side_effect = [1, "Pepsi", 0.8]

    def mock_update(conn, sql_create_product, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = update_product(
        mock_print_products, mock_input, mock_update, mock_connection, mock_print
    )
    expected = [{"product_id": 0, "product_name": "Pepsi", "product_price": 0.8}]
    assert actual == expected


def test_delete_product():

    mock_print_products = Mock()
    mock_print_products.return_value = [
        {"product_id": 0, "product_name": "Pepsi", "product_price": 0.8}
    ]
    mock_input = Mock()
    mock_input.return_value = 1

    def mock_update(conn, sql_create_product, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = delete_product(
        mock_print_products, mock_input, mock_update, mock_connection, mock_print
    )
    expected = []
    assert actual == expected