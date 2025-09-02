from src.courier.core import create_courier, update_courier, delete_courier

from unittest.mock import Mock, patch


@patch("os.system")
@patch("uuid.uuid4")
def test_create_courier(mock_uuid4, mock_system):

    test_couriers = []

    mock_system.return_value = ""

    mock_uuid4.return_value = 0

    mock_input = Mock()
    mock_input.side_effect = ["John", "07111222333"]

    mock_connection = Mock()

    def mock_update(conn, sql_create_courier, values):
        pass

    mock_print = Mock()

    actual = create_courier(
        test_couriers,
        mock_input,
        mock_update,
        mock_connection,
        mock_print,
    )
    expected = [
        {"courier_id": 0, "courier_name": "John", "courier_phone": "07111222333"}
    ]
    assert actual == expected


def test_update_courier():

    mock_print_couriers = Mock()
    mock_print_couriers.return_value = [
        {"courier_id": 0, "courier_name": "Pepso", "courier_phone": 0.1}
    ]
    mock_input = Mock()
    mock_input.side_effect = [1, "John", "07111222333"]

    def mock_update(conn, sql_create_courier, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = update_courier(
        mock_print_couriers, mock_input, mock_update, mock_connection, mock_print
    )
    expected = [
        {"courier_id": 0, "courier_name": "John", "courier_phone": "07111222333"}
    ]
    assert actual == expected


def test_delete_courier():

    mock_print_couriers = Mock()
    mock_print_couriers.return_value = [
        {"courier_id": 0, "courier_name": "John", "courier_phone": "07111222333"}
    ]
    mock_input = Mock()
    mock_input.return_value = 1

    def mock_update(conn, sql_create_courier, values):
        pass

    mock_connection = Mock()
    mock_print = Mock()

    actual = delete_courier(
        mock_print_couriers, mock_input, mock_update, mock_connection, mock_print
    )
    expected = []
    assert actual == expected