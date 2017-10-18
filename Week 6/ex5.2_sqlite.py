#!/bin/python

import sqlite3
import codecs

query_question_2 = '''
SELECT sub.OrderID, Products.ProductID, Products.ProductName
FROM (
    SELECT Orders.OrderID FROM Products
    INNER JOIN "Order Details" ON "Order Details".ProductID=Products.ProductID
    INNER JOIN Orders ON "Order Details".OrderID=Orders.OrderID WHERE Orders.CustomerID="ALFKI"
    GROUP BY Orders.OrderID
    HAVING COUNT(DISTINCT Products.ProductID) >= 2
) sub
JOIN Products
INNER JOIN "Order Details" ON "Order Details".ProductID=Products.ProductID
WHERE "Order Details".OrderID=sub.OrderID
ORDER BY sub.OrderID;
'''

# Open the Northwind database
conn = sqlite3.connect('northwind.db')
# Replace the encoding by cp1250, which is the database encoding
conn.text_factory = lambda x: str(x, 'cp1250') 
c = conn.cursor()

orders = {}

print('Orders that contain at least 2 different product types:')
for row in c.execute(query_question_2):
    orders[row[0]] = orders.get(row[0], []) + [[row[1], row[2]]]

for key in orders.keys():
    print('Order {}:'.format(key))
    for products in orders[key]:
        print('Ordered {}, product ID {}'.format(products[1], products[0]))
