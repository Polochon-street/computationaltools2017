#!/bin/python3

for iteration in range(500):
    a = 0
    for x in range(1,10001):
        a += 1/(x**2)

print(a)
