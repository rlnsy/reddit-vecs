#! /usr/bin/python

import praw
import pickle
import unicodedata
import codecs
import client
import pandas as pd
from prawcore.exceptions import ResponseException

reddit = praw.Reddit(client_id=client.id(),
                     client_secret=client.secret(),
                     password=client.pword(),
                     user_agent='sub-analysis-scraper by u/snewapp', username=client.uname())

subs_info = pd.read_csv('data/subreddits_basic.csv',delimiter=',',usecols=[3,4],names=['name','subscribers'])

# convert subscriber entries to int
def convert_val(val):
    try:
        return int(val)
    except ValueError:
        return 0
subs_info['subscribers'] = subs_info['subscribers'].apply(lambda x: convert_val(x))

# sort by subscribers
subs_info = subs_info.sort_values('subscribers',ascending=False)
sub_names = subs_info['name'].values

print('Downloading subreddit content...')
sub_files = []
names_downloaded = []
for i, name in enumerate(sub_names[0:1000]):
    try:
        print('downloading r/' + name + '...')
        content = ''
        for comment in reddit.subreddit(name).comments(limit=200):
            # 200 should be enough
            content = content + str(unicodedata.normalize('NFKD', comment.body).encode('ascii','ignore'))
        print('saving to file')
        file = codecs.open('data/subs_all/' + name + '.txt', 'w', 'utf-8')
        file.write(content)
        file.close()
        # if no errors thrown in previous code
        names_downloaded.append(name)
        sub_files.append('data/subs_all/' + name +'.txt')
        print('downloaded: ' + str(len(names_downloaded)))
    except ResponseException:
        print('subreddit skipped')

files_store = open('data/sub_files_all.pickle','wb')
pickle.dump(sub_files,files_store)
files_store.close()

names_store = open('data/sub_names_all.pickle','wb')
pickle.dump(names_downloaded,names_store)
files_store.close()

print('done')
