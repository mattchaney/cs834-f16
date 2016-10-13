#!/usr/bin/python

import argparse
import os
import operator
import sys
import nltk
from os.path import isdir, isfile
from bs4 import BeautifulSoup

class WordCounter(object):
    def __init__(self, root):
        self.tokenizer = nltk.RegexpTokenizer(r'\w+')
        self.root = root
        self.wmap = {}
        self.invidx = {}
        self.bgmap = {}
        self.filelist = []
        self.visited = 0

    def getfiles(self, folder=''):
        items = os.listdir(self.root + folder)
        for item in items:
            filepath = self.root + folder + os.sep + item
            if isfile(filepath):
                self.filelist.append(filepath)
            elif isdir(filepath):
                self.getfiles(folder + os.sep + item)

    def count(self, filepath):
        sys.stdout.write("\rprocessing document #%i" % self.visited)
        sys.stdout.flush()
        with open(filepath) as infile:
            text = BeautifulSoup(infile.read(), 'html.parser').get_text()
            tokens = self.tokenizer.tokenize(text)
        for s in tokens:
            if not self.wmap.has_key(s):
                self.wmap[s] = 0
            self.wmap[s] = self.wmap[s] + 1
            if not self.invidx.has_key(s):
                self.invidx[s] = []
                self.invidx[s].append(filepath)
        for b in nltk.bigrams(tokens):
            if not self.bgmap.has_key(b):
                self.bgmap[b] = 0
            self.bgmap[b] = self.bgmap[b] + 1
        self.visited = self.visited + 1

    def writeresults(self):
        with open('wordcount', 'w') as outfile:
            for k, v in sorted(self.wmap.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(str(v) + '\t' + k.encode('utf-8') + '\n')
        with open('bigramcount', 'w') as outfile:
            for k, v in sorted(self.bgmap.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(str(v) + '\t' + k[0].encode('utf-8') + '\t' + k[1].encode('utf-8') + '\n')
        with open('invidx', 'w') as outfile:
            for k, v in sorted(self.invidx.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(str(v) + '\t')
                for page in v:
                    outfile.write(page + '\t')
                outfile.write('\n')

    def run(self):
        print 'delving into "{0}"'.format(self.root)
        self.getfiles()
        print 'found {0} documents'.format(len(self.filelist))
        map(self.count, self.filelist)
        print '\nfound {0} words'.format(len(self.wmap))
        print 'found {0} bigrams'.format(len(self.bgmap))
        self.writeresults()
        print 'wrote word counts, bigram counts and uncompressed inverted index'

if __name__ == '__main__':
    parser = argparse.ArgumentParser('word count')
    parser.add_argument('-root', '-r', help='the root directory for parsing', default='en')
    args = parser.parse_args()
    wc = WordCounter(args.root)
    wc.run()
