#!/bin/python

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from collections import Counter
import json
import re
import numpy as np

articles = []

# Make a huge "article" list
for i in range(0, 22):
    with open('reuters-{:03d}.json'.format(i)) as f:
        local_articles = json.load(f)
        for article in local_articles:
            # Only pick articles that have a body and topic(s)
            if 'body' in article and 'topics' in article:
                articles.append(article)

# Concatenate all article bodies
all_text = [''.join(ch for ch in x['body'].lower()) for x in articles]
# Make a list of unique words - not stripping punctuation to have the same 
# results as exercise description
unique_words = list(set(re.split(' |\n', ' '.join(all_text))))

# For each article, flag it if it has "earn" in its topic
earn_not_earn = []
for article in articles:
    if 'earn' in article['topics']:
        earn_not_earn.append(1)
    else:
        earn_not_earn.append(0)
earn_not_earn = np.array(earn_not_earn, dtype=int)

# Prepare the bag of words matrix
bag_of_words = np.zeros((len(articles), len(unique_words)), dtype=int)

# Fill the bag of words correctly
for i,field in enumerate(articles):
    # Lower and split the words from the body
    text = field['body'].lower()
    words = re.split(' |\n', ' '.join(text))
    # Count each word
    counter = Counter(words)
    # Create the row in unique_words order
    row = np.array([counter.get(w, 0) for w in unique_words], dtype=int)
    # Put replace the dummy zeros-row with the article's actual word count row
    bag_of_words[i] = row

print(
    'The bag of words is of size {}x{}'.format(
        len(bag_of_words),
        len(bag_of_words[0]),
    )
)

# Split the bag of words / results between training (80%) / test set (20%)
X_train, X_test, y_train, y_test = train_test_split(
    bag_of_words, earn_not_earn, test_size=0.2)

# Create the classifier
clf = RandomForestClassifier(n_estimators=50)
# Train the classifier
clf.fit(X_train, y_train)
# Test the classifier against the test set
score = clf.score(X_test, y_test)
print('Score on the test set: {:2.1f}%'.format(score*100))
