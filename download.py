#! /usr/bin/python

import praw
import pickle
import client
import unicodedata

reddit = praw.Reddit(client_id=client.id(),
                     client_secret=client.secret(),
                     password=client.pword(),
                     user_agent='sub-recommender-scraper by u/snewapp',
                     username=client.uname())

data = {};

front_page = reddit.front.top(time_filter='week');

subs_done = 0;
for subreddit in reddit.subreddits.default(limit=100):
    sub_name = subreddit.display_name;
    print "downloading subreddit r/" + sub_name
    data[sub_name] = ""
    coms_done = 0;
    for comment in subreddit.comments(limit=100):
        content = unicodedata.normalize('NFKD', comment.body).encode('ascii','ignore')
        data[sub_name] = data[sub_name] + ' ' + str(content)
        coms_done = coms_done + 1
    print "comments downloaded in last sub: " + str(coms_done)
    subs_done = subs_done + 1
    print "subreddits downloaded: " + str(subs_done)


file = open('data.txt','wb')
pickle.dump(data,file)
file.close()
