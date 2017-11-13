#!/bin/python

import helpers
import shelve
import sqlite3
from string import punctuation
import sys

query = "SELECT subreddit_id, GROUP_CONCAT(body, ' ') from comments GROUP BY subreddit_id;"

# Connect to the database and do SQL-related stuff
conn = sqlite3.connect('reddit.db')
c = conn.cursor()
c.execute(query)

# Use an efficient translate table to replace all punctuation
# chars by spaces (using punctuation characters in string module)
translate = str.maketrans(punctuation, ' '*len(punctuation))

# Argument handling
if len(sys.argv) > 2:
    print(
        'Usage: run "./assignment1.py <file>" to avoid consumming RAM and '
        'store the dict to the hard drive. Otherwise RAM will be used.'
    )
    exit() 

if len(sys.argv) == 1:       
    count = {}
else:
    count = shelve.open(sys.argv[1])

# Each row represents (a subreddit, all concatenated comments in the subreddit)
for row in c:
    subreddit = row[0]
    # Delete all punctuation chars in the comments
    comments = row[1].translate(translate)
    # Put all the comments in lowercase
    comments = comments.lower()
    # Count all individual words by making a set of all words - set() will
    # return only unique words.
    word_count = len(set(comments.split()))
    # Add the word count to the global dict
    count[row[0]] = word_count

# Sort all subreddits by word count in reverse order and get the 10 first
top_ten = sorted(count, key=count.get, reverse=True)[:10]
# Get all corresponding subreddit names 
human_readable_top_ten = helpers.subreddit_names(top_ten)
# Show proper output
human_readable_top_ten = [(count[x], x, human_readable_top_ten[i]) for i,x in enumerate(top_ten)]

if len(sys.argv == 2):
    count = shelve.close()
print(human_readable_top_ten)
