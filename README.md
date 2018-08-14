# Content-Based Community Discovery and Recommendation on Reddit

## Running
The python scripts for this project can be used to download and vectorize subreddit data. They require the standard numerical computing libraries in the Anaconda environment as well as a handful of other packages for content processing. The code has been tested on python 3.6. Note that the downloader makes use of a pre-made dataset for subreddit lists which can be downloaded [here](https://www.reddit.com/r/datasets/comments/8isnek/list_of_every_subreddit_on_reddit/).

Files: 
* [download_all.py](../master/download_all.py): Subreddit content scraper (See file for details)
* [make_vecs.py](../master/make_vecs.py): Content vectorizer (See file for details)

## Progress
### Experimentation
I try to keep records of all the experiments I perform in the following files. Each notebook usually encompasses analysis or creation of a single data file, so the journal is fairly modular in structure. The notebooks link to the external site plot.ly, which I use to save interactive visualizations of the data.

1. [TFIDF Vectorization and t-SNE Dimensionality Reduction](../master/tSNE.ipynb)
2. [Representation Analysis and Basic Clustering](../master/vecs_analysis.ipynb)

### Deliverables
User-ready functionality is limited as of yet to the scripts mentioned in the 'running' section. However, I hope to deploy the models created here at app-scale once a useful model and front-end are both complete

## Origins
Seeing how many newsfeed and content-suggestion systems work nowadays, I was inspired to use machine learning to construct models for discovering new sources for news, entertainment etc.

## Why Reddit?
Reddit has for a long time been my go-to platform for aggregated web content. Recently, in an effort to break free of the closed circle of communities (subreddits) I had found myself in, I started to make new accounts just so I could go through the process of re-subscribing to new subs that I thought might be interesting. One of my hopes for this project is to automate and enhance this process by training a content-based recommendation system (that hopefully incorporates an element of deviation from current sources)

## Contribution
Right now this repo is mostly me just tinkering around from time to time, but feel free to contribute or give feedback!
