#!/bin/python

import helpers
import sqlite3

query = '''
SELECT subreddit_id,AVG(level) FROM (  
    WITH RECURSIVE fulltree(subreddit_id,id,parent_id,level) AS (
        SELECT subreddit_id, id, parent_id, 0 as level from comments where parent_id like 't3_%'
UNION ALL
    SELECT t.subreddit_id,t.id, t.parent_id, ft.level+1 as level from comments t, fulltree ft where t.parent_id = ft.id
)
SELECT * from fulltree order by id) WHERE
    id not in (SELECT parent_id FROM comments) GROUP BY subreddit_id;
'''

# Connect to the database and do SQL-related stuff
conn = sqlite3.connect('reddit.db')

c = conn.cursor()
c.execute(query)

# Fetch the results
subs_average = c.fetchall()
# Sort all subreddits by average thread depth
top_ten = sorted(subs_average, key=lambda x: x[1], reverse=True)[:10]
# Get all real subreddit names
top_ten_human_readable = helpers.subreddit_names(top_ten) 

for (sub_id, value), name in zip(subreddit_id, top_ten_human_readable)
    print(
        'Subreddit {} (ID {}) has an average comment thread depth of {}.'
        .format(sub_id, value, name)
    )

# Compute the average subreddit thread depth value
avg = 0
for sub_av in subs_average:
    avg += sub_av[1]
avg /= len(subs_average)

print('Average subreddit thread depth length is {}.'.format(avg))
