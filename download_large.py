#! /usr/bin/python

import praw
import pickle
import unicodedata
import codecs
import client
import pandas as pd

reddit = praw.Reddit(client_id=client.id(),
                     client_secret=client.secret(),
                     password=client.pword(),
                     user_agent='sub-analysis-scraper by u/snewapp', username=client.uname())

print('Downloading subreddit content...')

subs_info = pd.read_csv('data/subreddits_basic.csv',delimiter=',',usecols=[3,4])
# first column is name, second is number of subcribers
sub_names = subs_info.iloc[:,0].values
sub_names = sub_names[0:100] #limit the number of subreddits!

sub_files = []
names_list = []
for i, name in enumerate(sub_names):
    try:
        print('downloading r/' + name + '...')
        content = ''
        for comment in reddit.subreddit(name).comments(limit=500):
            content = content + str(unicodedata.normalize('NFKD', comment.body).encode('ascii','ignore'))
        print('saving to file')
        file = codecs.open('data/subs_large/' + name + '.txt', 'w', 'utf-8')
        file.write(content)
        file.close()
        # if no errors thrown in previous code
        names_list.append(name)
        sub_files.append('data/subs_large/' + name +'.txt');
    except:
        print('subreddit skipped')
    finally:
        print('downloaded: ' + str(names_list))

files_store = open('data/sub_files_large.pickle','wb')
pickle.dump(sub_files,files_store)
files_store.close()

names_store = open('data/sub_names_large.pickle','wb')
pickle.dump(names_list,names_store)
files_store.close()

print('done')
