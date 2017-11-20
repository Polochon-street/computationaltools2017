#!/bin/python

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json
import re
import numpy as np

articles = []
N = 1000


def hash_func(string):
    """Hash a string very naively.

    Returns the summed ascii value of all the characters of
    the given string modulo the bucket size N
    """

    return sum(map(ord, string)) % N 


# Make a huge "article" list
for i in range(0, 22):
    with open('reuters-{:03d}.json'.format(i)) as f:
        local_articles = json.load(f)
        for article in local_articles:
            # Only pick articles that have a body and topic(s)
            if 'body' in article and 'topics' in article:
                articles.append(article)

# For each article, flag it if it has "earn" in its topic
earn_not_earn = []
for article in articles:
    if 'earn' in article['topics']:
        earn_not_earn.append(1)
    else:
        earn_not_earn.append(0)
earn_not_earn = np.array(earn_not_earn, dtype=int)

# Prepare the bucket articles matrix
buckets = np.zeros((len(articles), N), dtype=int)

# Fill the bucket articles matrix correctly
for i,field in enumerate(articles):
    # Lower and split the words from the body
    text_without_punct = [''.join(ch for ch in field['body'].lower())]
    words = re.split(' |\n', ' '.join(text_without_punct))
    row = np.zeros(N)
    # Hash the words and put them in the right place 
    for word in words:
        row[hash_func(word)] += 1
    # Add the row to the bucket matrix
    buckets[i] = row

print(
    'The final matrix is of size {}x{}'.format(
        len(buckets),
        len(buckets[0]),
    )
)


# Split the bucket articles matrix / results between training (80%)
# / test set (20%)
X_train, X_test, y_train, y_test = train_test_split(
    buckets, earn_not_earn, test_size=0.2)

# Create the classifier
clf = RandomForestClassifier(n_estimators=50)
# Train the classifier
clf.fit(X_train, y_train)
# Test the classifier against the test set
score = clf.score(X_test, y_test)
print('Score on the test set: {:2.1f}%'.format(score*100))
