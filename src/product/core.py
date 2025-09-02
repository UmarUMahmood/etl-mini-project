import os
import uuid
from src.db.core import connection, update, load_products, export_products


menu = """
=-=-= PRODUCT MENU =-=-=
0 - RETURN TO MAIN MENU
1 - PRINT PRODUCTS
2 - ADD NEW PRODUCT
3 - UPDATE EXISTING PRODUCT
4 - DELETE PRODUCT
5 - EXPORT PRODUCTS TO CSV
=-=-=-=-=-=-=-=-=-=-=-=-=
"""

# sql queries used on product table in database
sql_create_product = (
    "INSERT INTO product (product_id, product_name, product_price) VALUES ( %s, %s, %s)"
)
sql_update_product_name = "UPDATE product SET product_name = %s WHERE product_id = %s"
sql_update_product_price = "UPDATE product SET product_price = %s WHERE product_id = %s"
sql_delete_product = "DELETE FROM product WHERE product_id = %s"


def product_menu(products):
    os.system("clear")
    while True:
        print(menu)
        product_menu_option = int(
            input("Enter the number of the menu option you wish to use: ")
        )

        if product_menu_option == 0:
            break

        if product_menu_option == 1:
            # print out products to screen
            print_products()

        if product_menu_option == 2:
            # create new product
            create_product(products, input, update, connection, print)

        if product_menu_option == 3:
            # update product
            update_product(print_products, input, update, connection, print)

        if product_menu_option == 4:
            # delete product
            delete_product(print_products, input, update, connection, print)

        if product_menu_option == 5:
            # export products
            export_products(connection())


def print_products():
    # print products
    os.system("clear")
    products = load_products(connection())
    index = 1  # from a user pov, starting a list at 1 makes more sense
    for product in products:
        print(f"{index} - {product['product_name']} - £{product['product_price']}")
        index += 1
    return products


def create_product(products, input, update, connection, print):
    # ask user for the name of the product
    # ask user for the price of the product
    # append to products list

    os.system("clear")

    new_id = uuid.uuid4()
    new_name = input("Enter the name of the new product: ")
    new_price = float(input("Enter the price of the new product: "))

    new_product = {
        "product_id": new_id,
        "product_name": new_name,
        "product_price": new_price,
    }

    products.append(new_product)

    update(connection(), sql_create_product, (new_id, new_name, new_price))

    print("Product Added.")

    return products


def update_product(print_products, input, update, connection, print):
    # ask user to select a product or 0 to cancel -- Note: index 0 is first item in the list, so leave blank to cancel?
    # for each product property:
    #   ask user for updated data or leave blank to skip
    #   update the product property if not blank

    products = print_products()
    index = int(input("\nSelect a product to update or enter 0 to cancel: "))

    if index == 0:
        return products  # cancel by ending the function
    else:
        index -= 1  # decrement index because print index starts at 1
        for key in products[index].keys():
            if key != "product_id":
                update_value = (
                    input(f"Enter a new {key} or leave blank to keep the same: ")
                    or None
                )
                # only save input at the given index if the user entered a value to update for that key
                if update_value is not None:
                    if key == "product_name":
                        products[index][key] = update_value
                        product_id = products[int(index)]["product_id"]
                        update(
                            connection(),
                            sql_update_product_name,
                            (update_value, [product_id]),
                        )
                    if key == "product_price":
                        products[index][key] = update_value
                        product_id = products[int(index)]["product_id"]
                        update(
                            connection(),
                            sql_update_product_price,
                            (update_value, [product_id]),
                        )

    print("Product Updated.")

    return products


def delete_product(print_products, input, update, connection, print):
    # ask user to select a product to delete or 0 to cancel
    # remove this item from the products list

    products = print_products()
    index = int(input("\nSelect a product to delete or enter 0 to cancel: "))

    if index == 0:
        return products  # cancel by ending the function
    else:
        product_id = products[int(index - 1)][
            "product_id"
        ]  # decrement index because print index starts at 1
        update(connection(), sql_delete_product, [product_id])
        products.pop(index - 1)

    print("Product Deleted.")

    return products