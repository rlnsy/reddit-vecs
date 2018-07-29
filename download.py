#! /usr/bin/python

# Scraper for subreddit content
# Downloads words from comments across subs and
# and stores as a file-encoded dictionary

# Options [#subreddits, #comments]

import sys
import praw
import pickle
import client
import unicodedata
import re
from stemming.porter2 import stem

reddit = praw.Reddit(client_id=client.id(),
                     client_secret=client.secret(),
                     password=client.pword(),
                     user_agent='sub-recommender-scraper by u/snewapp',
                     username=client.uname())

# returns words from content greater than length 1,
# in all lower case and stemmed
def clean(content):
    format = re.compile('[a-z]+',re.IGNORECASE) # single word format
    wds = format.findall(content)
    wds = filter(lambda w: len(w) >= 2, wds)
    wds = list(map(lambda w: w.lower(), wds))
    wds = list(map(lambda w: stem(w), wds))
    return wds

data = {};

front_page = reddit.front.top(time_filter='week');

subs_done = 0;
# todo: run over all subs
for subreddit in reddit.subreddits.default(limit=int(sys.argv[1])):
    sub_name = subreddit.display_name;
    print ('downloading subreddit r/' + sub_name)
    data[sub_name] = []
    coms_done = 0;
    for comment in subreddit.comments(limit=int(sys.argv[2])):
        content = unicodedata.normalize('NFKD', comment.body).encode('ascii','ignore')
        words = clean(str(content))
        data[sub_name] = data[sub_name] + words
        coms_done = coms_done + 1
    print ('comments downloaded in last sub: ' + str(coms_done))
    subs_done = subs_done + 1
    print ('subreddits downloaded: ' + str(subs_done))

# write data to file
file = open('data/word.txt','wb')
pickle.dump(data,file)
file.close()
