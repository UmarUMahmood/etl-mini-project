import os

from src.product.core import product_menu
from src.courier.core import courier_menu
from src.order.core import order_menu
from src.file_handler.core import read_data, save_data
from src.db.core import (
    connection,
    load_products,
    load_couriers,
    load_orders,
    export_products,
    export_couriers,
    export_orders,
)

menu = """
=-=-= MAIN MENU =-=-=
0 - EXIT APP
1 - SHOW PRODUCT MENU
2 - SHOW COURIER MENU
3 - SHOW ORDER MENU
4 - EXPORT DATA
=-=-=-=-=-=-=-=-=-=-=
"""

conn = connection()

def main_menu(products, couriers, orders):

    while True:
        os.system("clear")
        print(menu)
        main_menu_option = int(
            input("Enter the number of the menu option you wish to use: ")
        )

        if main_menu_option == 0:
            break

        if main_menu_option == 1:
            product_menu(products)  # load product menu

        if main_menu_option == 2:
            courier_menu(couriers)  # load courier menu

        if main_menu_option == 3:
            order_menu(orders, couriers, products)  # load order menu

        if main_menu_option == 4:
            export_products(conn)
            export_couriers(conn)
            export_orders(conn)


if __name__ == "__main__":
    products = list(load_products(conn))
    couriers = list(load_couriers(conn))
    orders = list(load_orders(conn))

    # show list of options to user and accept numerical input
    main_menu(products, couriers, orders)
