import MySQLdb
import json


def create_table():
    with open("product_data.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        port=3306,
        passwd="Adamabdul@paypal4040",
        db="price_monitor",
    )
    cursor = db.cursor()
    for key, item in data.items():
        product_id = item["ProductId"]
        
        query_insert = "INSERT INTO products (product_id) VALUES (%s)"
        cursor.execute(query_insert, (product_id,))
        
        
        query = "CREATE TABLE `productshistory_{}`(`database_id`  int AUTO_INCREMENT NOT NULL , `product_name` varchar(255) NOT NULL ,`price` float NOT NULL ,`date_time` json NOT NULL ,`product_id` varchar(255) NOT NULL , PRIMARY KEY (`database_id`), FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`))".format(product_id)
        cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

def update_table():
    with open("product_data.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        port=3306,
        passwd="Adamabdul@paypal4040",
        db="price_monitor",
    )
    cursor = db.cursor()
    for key, item in data.items():
        product_name = item["ProductName"]
        product_id = item["ProductId"]
        price = item["Price"]
        date_info = item["Date_Time"]

        query = "INSERT INTO productshistory_{}(product_name, price, product_id, date_time) VALUES (%s, %s, %s, %s);".format(product_id)
        values = (product_name, price, product_id, json.dumps(date_info))
        cursor.execute(query,values)
        
    db.commit()
    cursor.close()
    db.close()
    


def get_newest_row():
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        port=3306,
        passwd="Adamabdul@paypal4040",
        db="price_monitor",
    )
    cursor = db.cursor()
    query = "SELECT product_name, price, product_id, date_time FROM ProductsHistory_b09msrj97y ORDER BY database_id DESC LIMIT 1"
    
    cursor.execute(query)
    results = cursor.fetchone()
    cursor.close()
    db.close()
    return results

def update_db_table():
    with open("product_data.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        port=3306,
        passwd="Adamabdul@paypal4040",
        db="price_monitor",
    )
    cursor = db.cursor()
    
    newest_row = get_newest_row()
    product_id = newest_row[2]
    product_name = newest_row[0]
    current_price = newest_row[1]
    date_info = newest_row[3]
    
    query = "UPDATE products SET product_name = %s, current_price = %s, date_time = %s WHERE product_id = %s"
    values = (product_name, current_price, json.dumps(date_info), product_id)
    cursor.execute(query,values)
        
    db.commit()
    cursor.close()
    db.close()
    
#create_table() 
#update_table()   
#get_newest_row()
#update_db_table()
