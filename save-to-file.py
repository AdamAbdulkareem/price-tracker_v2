import json
from scraper import check_product_title
from scraper import check_product_id
from scraper import check_price
from scraper import check_date


def save_to_file():
    product_title = check_product_title()
    product_id = check_product_id()
    price = check_price()
    date_info = check_date()
    product_data = {
        "ProductName": product_title,
        "ProductId": product_id,
        "Price": price,
        "Date_Time": date_info,
    }
    try:
        with open("product_data.json", mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[product_id] = product_data

    with open("product_data.json", mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file)


save_to_file()
