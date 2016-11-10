#!/usr/bin/env python

import re
import sys
import cPickle
from collections import Counter


def get_words():
    try:
        return cPickle.load(open('words.p', 'rb'))
    except IOError:
        wordmap = Counter(re.findall(r'\w+', open('big.txt').read().lower()))
        cPickle.dump(wordmap, open('words.p', 'wb'))
        return cPickle.load(open('words.p', 'rb'))


words = get_words()
N = sum(words.values())


def exists(wordset):
    return set([word for word in wordset if word in words])


def prob(word):
    return float(words[word]) / float(N)


def edit1(w):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    deletes    = [w[:i]+w[i+1:]             for i in range(len(w))]
    transposes = [w[:i]+w[i+1]+w[i]+w[i+2:] for i in range(len(w)-1)]
    replaces   = [w[:i]+l+w[i+1:]           for i in range(len(w)) for l in letters]
    inserts    = [w[:i]+l+w[i:]             for i in range(len(w)+1) for l in letters]
    return set(deletes + transposes + replaces + inserts)


def edit2(word):
    e2 = [edit1(w) for w in edit1(word)]
    return [item for sublist in e2 for item in sublist]


def parse(word):
    return exists([word]) or exists(edit1(word)) or exists(edit2(word)) or [word]


def correct(word):
    return max(parse(word), key=prob)


if __name__ == '__main__':
    print correct(sys.argv[1])