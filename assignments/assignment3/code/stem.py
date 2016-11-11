#!/usr/bin/env python

import collections
import itertools
from data import words
from nltk.stem import *

class Result(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.sa = set(words[a])
        self.sb = set(words[b])
        self.sab = self.sa.intersection(self.sb)
        self.na = float(len(self.sa))
        self.nb = float(len(self.sb))
        self.nab = float(len(self.sab))
        self.dice = self.nab / (self.na + self.nb)

    def getdice(self):
        return self.dice

    def __repr__(self):
        return '({},{}) Dice {}'.format(self.a, self.b, self.dice)


def getstems(wordlist):
    # stem the first 1k words
    stemmer = SnowballStemmer('english')
    stems = {word: stemmer.stem(unicode(word, 'utf-8')) for word in wordlist}

    # count the stems to find duplicates
    vals = collections.Counter(stems.values())

    # reduce stem map to those that stemmed to the same stem
    dupkeys = {key: val for key, val in stems.items() if vals[val] > 1}

    # create new map that is the stem pointing to all terms that stemmed to it
    classes = {}
    for pair in itertools.combinations(dupkeys.items(), 2):
        k1 = pair[0][0]
        k2 = pair[1][0]
        v1 = pair[0][1]
        v2 = pair[1][1]
        if v1 == v2:
            if not classes.has_key(v1):
                classes[v1] = set()
            classes[v1].add(k1)
            classes[v1].add(k2)
    print '%d duplicate stems' % len(classes)

    # calculate Dice's coefficient for each term with the same stem
    results = {}
    for stem, terms in classes.items():
        for pair in itertools.combinations(terms, 2):
            t1 = pair[0]
            t2 = pair[1]
            if not results.has_key(stem):
                results[stem] = set()
            results[stem].add(Result(t1, t2))
    return classes, results


def convert(filtered):
    converted = {}
    for stem, fres in filtered.items():
        if len(fres) > 0:
            res = set()
            for result in fres:
                res.add(result.a)
                res.add(result.b)
            converted[stem] = res
    return converted


def printtables(fname, resultset, mode='w'):
    head = '\\begin{table}[h!]\n\\centering\n\\begin{tabular}{ | c | c | }\n'
    foot = '\\hline\n\\end{tabular}\n\\caption{``%s\'\' stems}\n\\label{tab:%s}\n\\end{table}\n'
    print 'writing tables'
    with open(fname, mode) as outfile:
        outfile.write('\n\n\n\\noindent\n')
        for stemclass in resultset.items():
            outfile.write(stemclass[0])
            outfile.write(': ')
            outfile.write(', '.join(stemclass[1]))
            outfile.write('\\\\\n')
