"""
WEEK 4 Assignment

Code up two version of tf-idf:

1. Version 1: what I've been calling "traditional" (in your function implementation below when "smoothed" is False).
In scikit-learn this would be: TfidfVectorizer(norm=None, smooth_idf=False)

2. Version 2: what I've been calling "smoothed" (in your function implementation below when "smoothed" is True).
In scikit-learn this would be: TfidfVectorizer(norm=None)

Don't worry about implementing normalization for this assignment.

The output of the function should match the output of the scikit-learn version. So in particular, if we have
the following corpus:

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first USU document?',
]

Then your version should equal the scikit-learn implementation (should be helpful for testing):

tf_idf(corpus) = TfidfVectorizer(norm=None, smooth_idf=False).fit_transform(corpus).toarray()

and

tf_idf(corpus, smoothed=True) = TfidfVectorizer(norm=None).fit_transform(corpus).toarray()
"""

import numpy as np
import string

def tf_idf(corpus: list[str], smoothed: bool = False) -> np.array:
    finalList = []
    allWords = {}
    for document in corpus:
        words = document.translate(str.maketrans('', '', string.punctuation)).lower().split()
        for w in words:
            if w not in allWords:
                allWords[w] = 0

    for document in corpus:
        docWords = allWords.copy()
        words = document.translate(str.maketrans('', '', string.punctuation)).lower().split()
        tf = {}
        for w in words:
            if w in tf:
                tf[w] += 1
            else:
                tf[w] = 1

        idf = {}
        for w in allWords:
            if w in tf:
                if smoothed:
                    idf[w] = np.log((len(corpus) + 1) / (1 + sum(1 for doc in corpus if w in doc.translate(str.maketrans('', '', string.punctuation)).lower().split())))
                else:
                    idf[w] = np.log(len(corpus) / sum(1 for doc in corpus if w in doc.translate(str.maketrans('', '', string.punctuation)).lower().split())) + 1
            else:
                idf[w] = 0
            docWords[w] = tf.get(w, 0) * idf[w]
        finalList.append(list(docWords.values()))
    return np.array(finalList, dtype=float)

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first USU document?',
]

print(tf_idf(corpus))

# The order of the dictionary is different from that created by TfidfVectorizer, but the values are the same