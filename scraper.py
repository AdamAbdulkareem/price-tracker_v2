from bs4 import BeautifulSoup
import requests
from datetime import date
from datetime import datetime


URL = "https://www.amazon.com/dp/B09MSRJ97Y"
#URL = "https://www.amazon.com/dp/B09XBS3S5J"
#URL = "https://www.amazon.com/dp/B0BDTWQ2DW"
#URL = "https://www.amazon.com/dp/B0863TXGM3"
#URL = "https://www.amazon.com/dp/B099VMT8VZ"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Upgrade-Insecure-Requests": "1",
}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")


def check_product_title():
    return soup.find("span", id="productTitle").text.strip()


def check_product_id():
    product_id_element = soup.find(
        "div", id="title_feature_div", attrs={"data-csa-c-asin": True}
    )
    return product_id_element["data-csa-c-asin"]


def check_price():
    price_string = soup.find("span", class_="a-offscreen").text.strip("$")
    return float(price_string.replace(",", ""))


def check_keywords():
    return soup.find("div", id="featurebullets_feature_div").text.strip()


def check_date():
    current_date = date.today().strftime("%a, %B %d %Y")
    current_time = datetime.now().strftime("%H:%M:%S %p")
    return current_date, current_time
