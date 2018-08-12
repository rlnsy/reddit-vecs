#! /usr/bin/python

import praw
import pickle
import unicodedata
import codecs
import client

reddit = praw.Reddit(client_id=client.id(),
                     client_secret=client.secret(),
                     password=client.pword(),
                     user_agent='sub-analysis-scraper by u/snewapp', username=client.uname())
print('Downloading subreddit content...')
files = []
for subreddit in reddit.subreddits.default(limit=100):
    name = subreddit.display_name
    print('downloading r/' + name + '...')
    files.append('data/subs/' + name +'.txt');
    content = ''
    for comment in subreddit.comments(limit=500):
        content = content + str(unicodedata.normalize('NFKD', comment.body).encode('ascii','ignore'))
    print('saving to file')
    file = codecs.open('data/subs/' + name + '.txt', 'w', 'utf-8')
    file.write(content)
    file.close()

files_store = open('data/sub_files.pickle','wb')
pickle.dump(files,files_store)
files_store.close()
print('done')
