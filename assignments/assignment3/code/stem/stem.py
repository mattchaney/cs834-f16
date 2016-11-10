#!/usr/bin/env python

import collections
import cPickle
from nltk.stem import *


class Result(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        sa = set(words[a])
        sb = set(words[b])
        sab = sa.intersection(sb)
        na = float(len(sa))
        nb = float(len(sb))
        nab = float(len(sab))
        self.dice = nab / (na + nb)

    def getdice(self):
        return self.dice

    def __repr__(self):
        return '({},{}) Dice {}'.format(
            self.a, self.b, self.dice)


try:
    print 'loading cached word map'
    words = cPickle.load(open('words.p', 'rb'))
except IOError:
    print 'cached word map not found, building now'
    words = {line.split()[0]: line.split()[1:] for line in open('invidx.dat').readlines()}
    cPickle.dump(words, open('words.p', 'wb'))
    words = cPickle.load(open('words.p', 'rb'))
N = float(sum(len(docs) for docs in words.values()))

# skipping first 13,000 terms because they are all numeric
# so they won't meet language probability expectations
first1k = sorted(words.keys())[13000:14000]

# stem the first 1k words
stemmer = SnowballStemmer('english')
stems = {word: stemmer.stem(unicode(word, 'utf-8')) for word in first1k}

# count the stems to find duplicates
vals = collections.Counter(stems.values())

# reduce stem map to those that stemmed to the same stem
dupkeys = {key: val for key, val in stems.items() if vals[val] > 1}

# create new map that is the stem pointing to all terms that stemmed to it
dupset = {}
for pair in itertools.combinations(dupkeys.items(), 2):
    k1 = pair[0][0]
    k2 = pair[1][0]
    v1 = pair[0][1]
    v2 = pair[1][1]
    if v1 == v2:
        if not dupset.has_key(v1):
            dupset[v1] = set()
        dupset[v1].add(k1)
        dupset[v1].add(k2)

print '%d duplicate stems' % len(dupset)

# calculate Dice's coefficient for each term with the same stem
results = {}
for stem, terms in dupset.items():
    for pair in itertools.combinations(terms, 2):
        t1 = pair[0]
        t2 = pair[1]
        if not results.has_key(stem):
            results[stem] = []
        results[stem].append(Result(t1, t2))
