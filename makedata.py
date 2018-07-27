import pandas as pd

# read content and return vocabulary of top
# words and corresponding counts
def load_vocabulary(content, size):

    # create word counts
    countMap = {}
    for sub in content:
        for w in content[sub]:
            if w in countMap:
                countMap[w] = countMap[w] + 1
            else:
                countMap[w] = 1

    # create corresponding count and word lists
    counts = []
    vocab = []
    for word in countMap:
        counts.append(countMap[word])
        vocab.append(word)

    # create a DataFrame
    count_data = {'count': counts, 'word': vocab}
    count_table = pd.DataFrame(count_data,columns=['count','word'])

    # sort DataFrame to preserve list correspondence
    count_table = count_table.sort_values('count',ascending=False)

    counts_sort = list(count_table['count'])
    vocab_sort = list(count_table['word'])

    # limit counts and vocab to size
    counts_sized = counts_sort[0:size]
    vocab_sized = vocab_sort[0:size]

    # create final data
    final_counts = pd.Series(counts_sized,vocab_sized)

    return {'counts': counts_sized, 'vocab': vocab_sized}

def vocab_intersect(words, vocab):
    count = [0] * len(vocab)
    for w in words:
        try:
            select = vocab.index(w)
            count[select] = count[select] + 1
        except ValueError:
            True

    return count

# count words in vocab accross subreddits and create
# count vectors
def load_feature_set(content, vocab):
    data = {}
    labels = []
    for sub in content:
        count = vocab_intersect(content[sub],vocab)
        data[sub] = count
        labels.append(sub)
    feature_set = pd.DataFrame(data,columns=labels)
    return feature_set

def save_to_excel(df,name):
    from pandas import ExcelWriter
    writer = ExcelWriter(name)
    df.to_excel(writer,'Sheet1')
    writer.save()

print "generating dataset from content..."

import pickle

# load downloaded words
file = open('data/word.txt','r')
all_words = pickle.load(file)

vocab_data = load_vocabulary(all_words, 1000)

data = load_feature_set(all_words,vocab_data['vocab'])

save_to_excel(data,'data/data.xlsx')

print "done"
