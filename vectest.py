from sklearn.feature_extraction.text import TfidfVectorizer
import os
import time
import pickle

def vectorize(files):
    vectorizer = TfidfVectorizer(input='filename',stop_words='english',lowercase=True,\
            strip_accents='unicode',smooth_idf=True,sublinear_tf=False,\
            use_idf=True, ngram_range=(1,2),min_df=2)

    vecs = vectorizer.fit_transform(files).todense()

    print(vecs)

if __name__ == '__main__':
    content_dir = 'review_polarity/txt_sentoken/pos/'
    file_names = os.listdir(content_dir)
    files = list(map(lambda name: content_dir + name, file_names))
    doc_counts = []
    times = []
    for num in range(2,len(files)):
        print(num)
        doc_counts.append(num)
        t0 = time.time()
        vectorize(files[0:num])
        t = time.time()
        t_delta = t - t0
        times.append(t_delta)
    print (doc_counts)
    print (times)
    pickle.dump(doc_counts, open( "nums.p", "wb" ))
    pickle.dump(times, open( "times.p", "wb" ))
