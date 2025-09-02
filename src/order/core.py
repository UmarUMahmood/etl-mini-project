import os
import uuid
from src.product.core import print_products
from src.courier.core import print_couriers
from src.db.core import (
    connection,
    update,
    load_orders,
    load_couriers,
    load_basket,
    export_orders,
)


menu = """
=-=-= ORDER MENU =-=-=
0 - RETURN TO MAIN MENU
1 - PRINT ORDERS
2 - ADD NEW ORDER
3 - UPDATE ORDER STATUS
4 - UPDATE ORDER
5 - DELETE ORDER
6 - EXPORT ORDERS TO CSV
=-=-=-=-=-=-=-=-=-=-=-=-=
"""

statuses = ["preparing", "ready", "out for delivery", "delivered"]

# NB: the order table in SQL is named transaction due to a order being a reserved term in SQL.
sql_create_order = "INSERT INTO transaction (transaction_id, customer_name, customer_address, customer_phone, courier_id, status) VALUES (%s, %s, %s, %s, %s, %s)"
sql_add_to_basket = (
    "INSERT INTO basket (basket_id, transaction_id, product_id) VALUES (%s, %s, %s)"
)
sql_update_order_status = "UPDATE transaction SET status = %s WHERE transaction_id = %s"
sql_update_customer_name = (
    "UPDATE transaction SET customer_name = %s WHERE transaction_id = %s"
)
sql_update_customer_address = (
    "UPDATE transaction SET customer_address = %s WHERE transaction_id = %s"
)
sql_update_customer_phone = (
    "UPDATE transaction SET customer_phone = %s WHERE transaction_id = %s"
)
sql_delete_order = "DELETE FROM transaction WHERE transaction_id = %s"


def order_menu(orders, couriers, products):
    os.system("clear")
    while True:
        print(menu)
        order_menu_option = int(
            input("Enter the number of the menu option you wish to use: ")
        )

        if order_menu_option == 0:
            break

        if order_menu_option == 1:
            # print out orders to screen
            print_orders()

        if order_menu_option == 2:
            # create new order
            create_order(
                orders,
                couriers,
                products,
                input,
                print_couriers,
                select_products,
                update,
                connection,
                print,
            )

        if order_menu_option == 3:
            # update order status
            update_order_status(print_orders, input, update, connection, print)

        if order_menu_option == 4:
            # update order
            update_order(print_orders, input, update, connection, print)

        if order_menu_option == 5:
            # delete order
            delete_order(print_orders, input, update, connection, print)

        if order_menu_option == 6:
            # export orders and basket
            export_orders(connection())


def print_orders():
    # print orders
    os.system("clear")
    orders = load_orders(connection())
    basket = load_basket(connection())
    index = 1

    for order in orders:

        print(f"\nORDER {index}")

        print(
            f"CUSTOMER: {order['customer_name']} - {order['customer_address']} - {order['customer_phone']}"
        )

        # use index from 'courier' in order to get that courier's row
        # courier = couriers[(order["courier_id"]]
        print(f"COURIER: {order['courier_name']}")

        print(f"STATUS: {order['status']}")

        # get the total cost of an order
        cost_of_order = 0
        for item in basket:
            if order["transaction_id"] == item["transaction_id"]:
                cost_of_order += item["product_price"]

        print(f"ITEMS: total cost: £{cost_of_order}")

        for item in basket:
            if order["transaction_id"] == item["transaction_id"]:
                print(f"- {item['product_name']}, £{item['product_price']}")

        index += 1
    return orders


def create_order(
    orders,
    couriers,
    products,
    input,
    print_couriers,
    select_products,
    update,
    connection,
    print,
):
    # ask user for the name of the customer
    # ask user for the address of the customer
    # ask user for the phone of the customer
    # (week 4) ask user to select from the product list until 0 to cancel
    # (week 4) set order products to be a list of product indexes
    # ask user to select a courier from the list
    # set order courier to be a courier index
    # set the default order status to be preparing
    # append the new to the list of orders

    os.system("clear")

    new_id = uuid.uuid4()
    new_customer_name = input("Enter the name of the customer: ")
    new_customer_address = input("Enter the address of the customer: ")
    new_customer_phone = input("Enter the phone number of the customer: ")

    couriers = print_couriers()
    courier_index = int(input("Please select a courier: ")) - 1
    courier_id = couriers[int(courier_index)]["courier_id"]

    selected_products = select_products(products)

    status = "preparing"

    new_order = {
        "order_id": new_id,
        "customer_name": new_customer_name,
        "customer_address": new_customer_address,
        "customer_phone": new_customer_phone,
        "courier_id": courier_id,
        "status": status,
    }

    orders.append(new_order)

    update(
        connection(),
        sql_create_order,
        (
            new_id,
            new_customer_name,
            new_customer_address,
            new_customer_phone,
            courier_id,
            status,
        ),
    )

    for selected_product in selected_products:
        basket_id = uuid.uuid4()
        update(connection(), sql_add_to_basket, (basket_id, new_id, selected_product))

    print("Order Added.")

    return orders


def select_products(products):
    # ask user to select from the product list until 0 to cancel
    # set order products to be a list of product ids

    # because product_ids use uuid, showing the user what indexes they selected is better than showing them the ids
    selected_indexes = []
    selected_products = []

    while True:
        os.system("clear")

        products = print_products()

        print(f"Selected Products: {selected_indexes}")

        selected_index = int(
            input("\nSelect a product or enter 0 to stop adding products: ")
        )
        selected_indexes.append(selected_index)

        if selected_index == 0:
            break
        else:
            product_id = products[int(selected_index - 1)]["product_id"]

            selected_products.append(product_id)

    return selected_products


def update_order_status(print_orders, input, update, connection, print):
    # ask user to select an order to update or 0 to cancel
    # ask user to select a new status from a list of statuses

    orders = print_orders()

    index = int(
        input(
            "Please enter the order you wish to update the status of, or enter 0 to cancel: "
        )
    )

    if index == 0:
        return orders
    else:
        index -= 1

        s_index = 1
        for status in statuses:
            print(f"{s_index} - {status}")
            s_index += 1

        new_status_index = int(input("Please choose the new status: "))
        new_status_index -= 1

        new_status = statuses[new_status_index]

        orders[index]["status"] = new_status

        order_id = orders[int(index)]["transaction_id"]
        update(
            connection(),
            sql_update_order_status,
            (new_status, [order_id]),
        )

        print("Status Updated.")

    return orders


def update_order(print_orders, input, update, connection, print):
    # ask user to select an order to update or 0 to cancel
    # for each order property:
    #   ask user for update data or leave blank to skip
    #   update the order if property not blank

    orders = print_orders()
    index = int(input("Select an order to update or enter 0 to cancel: "))

    if index == 0:
        return orders
    else:
        index -= 1

        protected = [
            "transaction_id",
            "courier_id",
            "courier_name",
            "courier_phone",
            "status",
        ]

        for key in orders[index].keys():
            if key not in protected:
                update_value = (
                    input(f"Enter a new {key} or leave blank to keep the same: ")
                    or None
                )
                if update_value is not None:
                    if key == "customer_name":
                        orders[index][key] = update_value
                        order_id = orders[int(index)]["transaction_id"]
                        update(
                            connection(),
                            sql_update_customer_name,
                            (update_value, [order_id]),
                        )
                    if key == "customer_address":
                        orders[index][key] = update_value
                        order_id = orders[int(index)]["transaction_id"]
                        update(
                            connection(),
                            sql_update_customer_address,
                            (update_value, [order_id]),
                        )
                    if key == "customer_phone":
                        orders[index][key] = update_value
                        order_id = orders[int(index)]["transaction_id"]
                        update(
                            connection(),
                            sql_update_customer_phone,
                            (update_value, [order_id]),
                        )

    print("Order Updated.")

    return orders


def delete_order(print_orders, input, update, connection, print):
    # ask user to select an order to delete or 0 to cancel
    # remove this item from the orders list

    orders = print_orders()
    index = int(input("Select an order to delete or enter 0 to cancel: "))

    if index == 0:
        return orders
    else:
        order_id = orders[int(index - 1)]["transaction_id"]
        update(connection(), sql_delete_order, [order_id])
        orders.pop(index - 1)

    print("Order Deleted.")

    return orders