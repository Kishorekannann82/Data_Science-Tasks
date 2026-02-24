import mysql.connector
from mysql.connector import Error

try:
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='ecommerce'
    )
    if connection.is_connected():
        print('Connected to MySQL database')

        cursor=connection.cursor()

        query ="Select * from customers where customer_id=52"

        cursor.execute(query)
        rows=cursor.fetchall()
        for row in rows:
            print(row)
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")