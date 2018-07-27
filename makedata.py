import pickle
import pandas as pd

def load_vocabulary(size):

    # load downloaded word dump
    file = open('data/word.txt','r')
    words = pickle.load(file)

    # create word counts
    countMap = {}
    for sub in words:
        for w in words[sub]:
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

    #sort DataFrame to preserve list correspondence
    count_table = count_table.sort_values('count',ascending=False)

    counts_sort = count_table['count']
    vocab_sort = count_table['word']

    # limit counts and vocab to size
    # TODO: exclude boring words (the, is, etc)
    counts_sized = counts_sort[0:size]
    vocab_sized = vocab_sort[0:size]

    # create final data
    final_counts = pd.Series(counts_sized,vocab_sized)

    print "word counts loaded: " + str(len(vocab_sized))

    return final_counts

load_vocabulary(100)
