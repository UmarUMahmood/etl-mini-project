import os
import pymysql.cursors
import csv
from dotenv import load_dotenv
import time

load_dotenv()

HOST = os.environ.get("MYSQL_HOST")
PORT = os.environ.get("MYSQL_PORT")
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB = os.environ.get("MYSQL_DB")

export_path = "data/"


def connection():
    return pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB,
        cursorclass=pymysql.cursors.DictCursor,
    )


conn = connection
# print(conn)  # <pymysql.connections.Connection object at <MEMORY_ALLOCATION>>


def query(conn, sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def update(conn, sql, values, should_commit=True):
    with conn.cursor() as cursor:
        cursor.execute(sql, values)
        if should_commit:  # atomicity - ensure the update completes/fails entirely
            conn.commit()


def load_products(conn):
    select_all_products = "SELECT * FROM product"
    products = query(conn, select_all_products)
    return products


def load_couriers(conn):
    select_all_couriers = "SELECT * FROM courier"
    couriers = query(conn, select_all_couriers)
    return couriers


def load_orders(conn):
    select_all_orders = "SELECT * FROM transaction NATURAL JOIN courier"
    orders = query(conn, select_all_orders)
    return orders


def load_basket(conn):
    select_all_basket = (
        "SELECT * FROM basket NATURAL JOIN transaction NATURAL JOIN product"
    )
    baskets = query(conn, select_all_basket)
    return baskets


def export_query(conn, sql, filename):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        
        with open(filename, "w", newline="\n") as file:
            writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(headers)
            for result in results:
                writer.writerow(result.values())


def export_products(conn):
    filename = (
        export_path + "products_" + str(time.strftime("%Y-%m-%d_%H-%M-%S")) + ".csv"
    )
    get_products = "SELECT * FROM product"

    export_query(conn, get_products, filename)


def export_couriers(conn):
    filename = (
        export_path + "couriers_" + str(time.strftime("%Y-%m-%d_%H-%M-%S")) + ".csv"
    )
    get_couriers = "SELECT * FROM courier"

    export_query(conn, get_couriers, filename)


def export_orders(conn):
    filename = (
        export_path + "orders_" + str(time.strftime("%Y-%m-%d_%H-%M-%S")) + ".csv"
    )
    get_orders = """
    SELECT * 
    FROM basket 
    NATURAL JOIN transaction 
    NATURAL JOIN product 
    ORDER BY transaction_id
    """

    export_query(conn, get_orders, filename)