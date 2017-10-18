#!/bin/python
from pymongo import MongoClient

# Connect to the mongo database
client = MongoClient()
# Choose the 'Northwind' database 
db = client['Northwind']

pipeline_more_than_two = [
    {
        "$match": { "CustomerID": "ALFKI" },
    },
    {
        "$lookup": {
            "from": "order-details",
            "localField": "OrderID",
            "foreignField": "OrderID",
            "as": "orders",
        }
    },
    {
        "$unwind": "$orders",
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "orders.ProductID",
            "foreignField": "ProductID",
            "as": "product",
        }
    },
    {
        "$project": {
            "OrderID": True,
            "product.ProductID": True,
            "product.ProductName": True,
        }
    },
    {
        "$unwind": "$product",
    },
    {
        "$group": {
            "_id": { "OrderID": "$OrderID" },
            "products": { "$addToSet": "$product" },
            "count": { "$sum": 0.125 },
        },
    },
    {
        "$match": { "count": { "$gte": 2 } }, 
    },
    # Facultative step; return only useful variables
    # and drop the temporary variable "count".
    {
        "$project": {
            "OrderID": True,
            "products": True,
        }
    },
    {
        "$sort": { "_id": 1 },
    }
]

# Format the output to have a "clean" output variable.
# Because our output from mongo is actually cleaner than SQL, this
# step is facultative.
results = list(db.orders.aggregate(pipeline_more_than_two))
orders = {}

for order in results:
    OrderID = order['_id']['OrderID']
    orders[OrderID] = []
    for product in order['products']:
        orders[OrderID] = orders[OrderID] + [[product['ProductID'], product['ProductName']]]

# Here we could simply return the "orders" dict variable, instead we print
# it so the reader can see them
print('Orders that contain at least 2 different product types:')
for key in orders.keys():
    print('Order {}:'.format(key))
    for products in orders[key]:
        print('Ordered {}, product ID {}'.format(products[1], products[0]))
