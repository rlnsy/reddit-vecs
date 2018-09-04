#! /usr/bin/python

import argparse
import sys
import os
import praw
import pickle
import unicodedata
import codecs
import client
import pandas as pd
from prawcore.exceptions import ResponseException
from multiprocessing import Pool

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--subs", \
help="max number of subs to download", required=False, default=50)
parser.add_argument("-c", "--comments", \
help="max number of comments to download", required=False, default=50)
parser.add_argument("-f", "--filter_nsfw", \
help="whether or not to filter nsfw communities", required=False, default="True")
parser.add_argument("-d", "--download", \
help="whether or not to download (set false to just scan)", required=False, default="True")
parser.add_argument("-o", "--output", \
help="output directory (should be an empty folder)", required=True)

args = vars(parser.parse_args())

# set up the API client
reddit = praw.Reddit(client_id=client.id(),
                     client_secret=client.secret(),
                     password=client.pword(),
                     user_agent='sub-analysis-scraper by u/snewapp', username=client.uname())

# load subreddits and subscriber numbers data
subs_info = pd.read_csv('data/subreddits_basic.csv',usecols=[3,4],names=['name','subscribers'])

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

# convert boolean args
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

subs_limit = int(args['subs'])
comment_limit = int(args['comments'])
filter_nsfw = str2bool(args['filter_nsfw'])
download = str2bool(args['download'])
out_dir = args['output']

# process an individual subreddit and save the content
def get_subreddit(name):
    skipped = False
    content = ''
    comment_count = 0
    subreddit = reddit.subreddit(name)
    if((subreddit.over18 is False) or (filter_nsfw == 'false')):
            for comment in subreddit.comments(limit=comment_limit):
                this_content = str(unicodedata.normalize('NFKD', comment.body).encode('ascii','ignore'))
                print(this_content)
                content = content + this_content
                comment_count = comment_count + 1
            try:
                file = codecs.open(out_dir + '/' + name + '.txt', 'w', 'utf-8')
            except FileNotFoundError:
                sys.exit("aborted - please create output directory")
            file.write(content)
            file.close()


    else:
        skipped = True
    return {'name': name, 'skipped':skipped}

# look at content files downloaded and save files, name, and subsciber lists
def finish():

    print("Reading downloaded content...")

    sub_files = [] # list of files
    names_downloaded = [] # list of raw subreddit names
    subscriber_counts = [] # list of subscriber counts

    # read all files in the dir
    for file in os.listdir(out_dir):
        if file.endswith(".txt"):
            print('Found: ' + file)
            sub_files.append(out_dir + '/' + file)
            name = file[:-4]
            names_downloaded.append(name)
            subscribers = subs_info.loc[subs_info['name'] == name, 'subscribers'].iloc[0]
            subscriber_counts.append(subscribers)

    # save the reference lists
    print("Saving reference data...")
    files_store = open(out_dir + '/files.pickle','wb')
    pickle.dump(sub_files,files_store)
    files_store.close()

    names_store = open(out_dir + '/names.pickle','wb')
    pickle.dump(names_downloaded,names_store)
    files_store.close()

    subscribers_store = open(out_dir + '/subscribers.pickle','wb')
    pickle.dump(subscriber_counts, subscribers_store)
    subscribers_store.close()

    print('Done; subreddits stored: ' + str(len(names_downloaded)))

# main
try:
    #p = Pool(20) # speed things up
    #results = p.map(get_subreddit,sub_names[0:subs_limit])
    if (download):
        # download the content
        print('Downloading subreddit content...')
        for name in sub_names[0:subs_limit]:
            get_subreddit(name)
    finish()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        finish()
        sys.exit(0)
    except SystemExit:
        os._exit(0)
