#!/bin/python

import helpers
import itertools
import sqlite3
import shelve
import sys

query = "SELECT author_id, GROUP_CONCAT(DISTINCT subreddit_id) from comments author_id GROUP BY author_id having count(distinct subreddit_id) >= 2;"

# Connect to the database and do SQL-related stuff
conn = sqlite3.connect('reddit.db')
c = conn.cursor()
c.execute(query)

# Argument handling
if len(sys.argv) > 2:
    print(
        'Usage: run "./assignment1.py <file>" to avoid consumming RAM and '
        'store the dict to the hard drive. Otherwise RAM will be used.'
    )
    exit() 

if len(sys.argv) == 1:
    # Use a simple dict in RAM
    authors_sub = {}
else:
    # Open a shelve (=hard-drive dict)
    authors_sub = shelve.open(sys.argv[1])

# For each user that authored a comment
for row in c:
    # Skip '[deleted]' user (which corresponds to deleted account
    # and is not relevant to our question
    if row[0] == '3':
        continue
    # Get the list of subreddits on which the user posted
    subreddits = row[1].split(',')
    # Make a list of all corresponding subreddit pairs
    subreddit_pairs = itertools.combinations(subreddits, 2)
    # For each pair, create a corresponding string hash and increment the
    # precise pair count
    for sub1, sub2 in (subreddit_pairs):
        hash_string = '{}/{}'.format(sub1,sub2)
        # Increment the pair count (if the pair doesn't exist in the dict,
        # put the default value 0)
        authors_sub[hash_string] = authors_sub.get(hash_string, 0) + 1

# Sort all subreddit pairs by count in reverse order and get the 10 first
top_ten = sorted(authors_sub, key=authors_sub.get, reverse=True)[:10]
# Get the count values for these 10 first subreddit pairs
values_top_ten = [authors_sub[key] for key in top_ten]
# Make a usable pair list (like [['sub1', 'sub2'], ['sub3', 'sub4']])
top_ten_iterable = [string.split('/') for string in top_ten]

# Get all subreddit pair real names
top_ten_human_readable = list(map(helpers.subreddit_names, top_ten_iterable))

print('Top ten:')

# Display the subreddit names along with the count of common authors
for subs_name, subs_id, values in zip(top_ten_human_readable, top_ten_iterable, values_top_ten):
    print(
        'The subs {} (ID {}) and {} (ID {}) have {} common authors.'
        .format(subs_name[0], subs_id[0], subs_name[1], subs_id[1], values)
    )

if len(sys.argv) == 2:
# Close the shelve
    authors_sub.close()
