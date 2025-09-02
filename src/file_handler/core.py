import csv

def read_data(filepath):
    data = []
    with open(filepath) as file:
        product_file = csv.DictReader(file)
        for products in product_file:
            data.append(products)
    return data

def save_data(filepath, data):
    keys = data[0].keys()
    with open(filepath, mode="w", newline="") as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(data)
