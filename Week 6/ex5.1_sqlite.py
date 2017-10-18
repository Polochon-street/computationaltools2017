#!/bin/python

import sqlite3
import codecs

query_question_1 = '''
SELECT Orders.OrderID, Products.ProductID, Products.ProductName FROM Products
INNER JOIN "Order Details" ON "Order Details".ProductID=Products.ProductID
INNER JOIN Orders ON "Order Details".OrderID=Orders.OrderID WHERE Orders.CustomerID="ALFKI"
ORDER BY Orders.OrderID;
'''

# Open the Northwind database
conn = sqlite3.connect('northwind.db')
# Replace the encoding by cp1250, which is the database encoding
conn.text_factory = lambda x: str(x, 'cp1250') 
c = conn.cursor()

orders = {}

for row in c.execute(query_question_1):
    orders[row[0]] = orders.get(row[0], []) + [[row[1], row[2]]]

# Here we could simply return the "orders" dict variable, instead we print
# it so the reader can see them
print('All orders and corresponding products:')
for key in orders.keys():
    print('Order {}:'.format(key))
    for products in orders[key]:
        print('Ordered {}, product ID {}'.format(products[1], products[0]))

