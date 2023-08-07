import MySQLdb
import json


def create_table():
    try:
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
        
            query_insert = "INSERT IGNORE INTO products (product_id) VALUES (%s)"
            cursor.execute(query_insert, (product_id,))
        
        
            query = "CREATE TABLE IF NOT EXISTS `productshistory_{}`(`database_id`  int AUTO_INCREMENT NOT NULL , `product_name` varchar(255) NOT NULL ,`price` float NOT NULL ,`date_time` json NOT NULL ,`product_id` varchar(255) NOT NULL , PRIMARY KEY (`database_id`), FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`))".format(product_id)
            cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        
    except FileNotFoundError as e:
        print("Error: File not found.", e)
        
    except json.JSONDecodeError as e:
        print("Error: Unable to decode JSON from file.", e)
        
    except MySQLdb.Error as e:
        print("MySQL Error:", e)


def update_table():
    try:
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
    
    except FileNotFoundError as e:
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        print("MySQL Error:", e)
    

def get_newest_row():
    newest_row_list = []
    try:
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
            query = "SELECT product_name, price, product_id, date_time FROM ProductsHistory_{} ORDER BY database_id DESC LIMIT 1".format(product_id)
        
            cursor.execute(query)
            results = cursor.fetchone()
            newest_row_list.append(results)
        
        cursor.close()
        db.close()
        return (newest_row_list)
    
    except FileNotFoundError as e:
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        print("MySQL Error:", e)
        

def get_price_change():  # sourcery skip: for-append-to-extend, inline-variable
    price_change_arr = []
    percent_change_arr = []
    try:
        with open("product_data.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
        
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd="Adamabdul@paypal4040",
            db="price_monitor",
        )
        for key, item in data.items():
            price_change_tuple = ()
            product_id = item["ProductId"]
    
            # Cursor for the entry price query
            cursor = db.cursor()
            entry_price_query = "SELECT price, database_id FROM productshistory_{} ORDER BY database_id ASC LIMIT 1".format(product_id)
            cursor.execute(entry_price_query)
            entry_price = cursor.fetchone()[0]
        
            price_change_tuple += (entry_price,)
            cursor.close()
    
            # Cursor for the current price query
            cursor = db.cursor()
            current_price_query = "SELECT price, database_id FROM productshistory_{} ORDER BY database_id DESC LIMIT 1".format(product_id)
            cursor.execute(current_price_query)
            current_price = cursor.fetchone()[0]
        
            price_change_tuple += (current_price,)
            cursor.close()
        
            price_change_arr.append(price_change_tuple)
    
        db.close()
    
        for initial_price, final_price in price_change_arr:
            percent_change = (final_price - initial_price) / initial_price * 100
            percent_change_arr.append(round(percent_change, 2))
    
        return (percent_change_arr)
    
    
    except FileNotFoundError as e:
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        print("MySQL Error:", e)
    
def update_db_table():
    try:
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
    
        for i in range(len(newest_row)):
            product_id = newest_row[i][2]
            product_name = newest_row[i][0]
            current_price = newest_row[i][1]
            price_change = get_price_change()[i]
            date_info = newest_row[i][3]
            query = "UPDATE products SET product_name = %s, current_price = %s, price_change = %s, date_time = %s WHERE product_id = %s"
            values = (product_name, current_price, price_change, json.dumps(date_info), product_id)
            cursor.execute(query,values)
        
        db.commit()
        cursor.close()
        db.close()
    
    except FileNotFoundError as e:
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        print("MySQL Error:", e)
    
create_table() 
update_table()   
get_newest_row()
get_price_change()
update_db_table()
