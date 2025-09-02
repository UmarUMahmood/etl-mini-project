import os
import uuid
from src.db.core import connection, update, load_couriers, export_couriers

menu = """
=-=-= COURIER MENU =-=-=
0 - RETURN TO MAIN MENU
1 - PRINT COURIERS
2 - ADD NEW COURIER
3 - UPDATE EXISTING COURIER
4 - DELETE COURIER
5 - EXPORT COURIERS TO CSV
=-=-=-=-=-=-=-=-=-=-=-=-=
"""

sql_create_courier = (
    "INSERT INTO courier (courier_id, courier_name, courier_phone) VALUES ( %s, %s, %s)"
)
sql_update_courier_name = "UPDATE courier SET courier_name = %s WHERE courier_id = %s"
sql_update_courier_phone = "UPDATE courier SET courier_phone = %s WHERE courier_id = %s"
sql_delete_courier = "DELETE FROM courier WHERE courier_id = %s"


def courier_menu(couriers):
    os.system("clear")
    while True:
        print(menu)
        courier_menu_option = int(
            input("Enter the number of the menu option you wish to use: ")
        )

        if courier_menu_option == 0:
            break

        if courier_menu_option == 1:
            # print out couriers to screen
            print_couriers()

        if courier_menu_option == 2:
            # create new courier
            create_courier(couriers, input, update, connection, print)

        if courier_menu_option == 3:
            # update courier
            update_courier(print_couriers, input, update, connection, print)

        if courier_menu_option == 4:
            # delete courier
            delete_courier(print_couriers, input, update, connection, print)

        if courier_menu_option == 5:
            # export couriers
            export_couriers(connection())


def print_couriers():
    # print couriers
    os.system("clear")
    couriers = load_couriers(connection())
    index = 1
    for courier in couriers:
        print(f"{index} - {courier['courier_name']} - {courier['courier_phone']}")
        index += 1
    return couriers


def create_courier(couriers, input, update, connection, print):
    # ask user for the name of the courier
    # ask user for the phone of the courier
    # append to couriers list

    os.system("clear")

    new_id = uuid.uuid4()
    new_name = input("Enter the name of the new courier: ")
    new_phone = input("Enter the phone of the new courier: ")

    new_courier = {
        "courier_id": new_id,
        "courier_name": new_name,
        "courier_phone": new_phone,
    }

    couriers.append(new_courier)

    update(connection(), sql_create_courier, (new_id, new_name, new_phone))

    print("Courier Added.")

    return couriers


def update_courier(print_couriers, input, update, connection, print):
    # ask user to select a courier or 0 to cancel -- Note: index 0 is first item in the list, so leave blank to cancel?
    # for each courier property:
    #   ask user for updated data or leave blank to skip
    #   update the courier property if not blank

    couriers = print_couriers()
    index = int(input("\nSelect a courier to update or enter 0 to cancel: "))

    if index == 0:
        return couriers  # cancel by ending the function
    else:
        index -= 1  # decrement index because print index starts at 1
        for key in couriers[index].keys():
            if key != "courier_id":
                update_value = (
                    input(f"Enter a new {key} or leave blank to keep the same: ")
                    or None
                )
                # only saves input at the given index if the user entered a value to update for that key
                if update_value is not None:
                    if key == "courier_name":
                        couriers[index][key] = update_value
                        courier_id = couriers[int(index)]["courier_id"]
                        update(
                            connection(),
                            sql_update_courier_name,
                            (update_value, [courier_id]),
                        )
                    if key == "courier_phone":
                        couriers[index][key] = update_value
                        courier_id = couriers[int(index)]["courier_id"]
                        update(
                            connection(),
                            sql_update_courier_phone,
                            (update_value, [courier_id]),
                        )

    print("Courier Updated.")

    return couriers


def delete_courier(print_couriers, input, update, connection, print):
    # ask user to select a courier to delete or 0 to cancel
    # remove this item from the couriers list

    couriers = print_couriers()
    index = int(input("\nSelect a courier to update or enter 0 to cancel: "))

    if index == 0:
        return couriers  # cancel by ending the function
    else:
        courier_id = couriers[int(index - 1)][
            "courier_id"
        ]  # decrement index because print index starts at 1
        update(connection(), sql_delete_courier, [courier_id])
        couriers.pop(index - 1)

    print("Courier Deleted.")

    return couriers