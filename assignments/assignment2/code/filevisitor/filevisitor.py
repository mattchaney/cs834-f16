#!/usr/bin/python

import argparse
import os
import operator
import sys
import nltk
from os.path import isdir, isfile
from bs4 import BeautifulSoup

class NullCounter(object):
    def count(self, filepath, rawtext):
        pass
    def results(self):
        pass

class FileVisitor(object):
    def __init__(self, root, counters=[NullCounter()]):
        self.root = root
        self.counters = counters
        self.visited = 0

    def visit(self, folder=''):
        items = os.listdir(self.root + folder)
        for item in items:
            # if self.visited == 101:
            #     return
            filepath = self.root + folder + os.sep + item
            if isfile(filepath):
                sys.stdout.write("\rprocessing doc #%i" % self.visited)
                sys.stdout.flush()
                with open(filepath) as infile:
                    soup = BeautifulSoup(infile.read(), 'html.parser')
                    for counter in self.counters:
                        counter.count(filepath, soup)  
                self.visited = self.visited + 1
            elif isdir(filepath):
                self.visit(folder + os.sep + item)

    def run(self):
        print 'delving into "{0}"'.format(self.root)
        self.visit()
        print
        for counter in self.counters:
            counter.results()    
        print 'done'

class WordCounter(object):
    def __init__(self):
        self.tokenizer = nltk.RegexpTokenizer(r'\w+')
        self.wmap = {}
        self.invidx = {}
        self.bgmap = {}

    def count(self, filepath, soup):
        plaintext = soup.get_text()
        tokens = self.tokenizer.tokenize(plaintext)
        for s in tokens:
            if not self.wmap.has_key(s):
                self.wmap[s] = 0
            self.wmap[s] = self.wmap[s] + 1
            if not self.invidx.has_key(s):
                self.invidx[s] = set()
            self.invidx[s].add(filepath)
        for b in nltk.bigrams(tokens):
            if not self.bgmap.has_key(b):
                self.bgmap[b] = 0
            self.bgmap[b] = self.bgmap[b] + 1

    def results(self):
        print 'found {0} words'.format(len(self.wmap))
        print 'found {0} bigrams'.format(len(self.bgmap))
        with open('wordcount', 'w') as outfile:
            for k, v in sorted(self.wmap.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(str(v) + '\t' + k.encode('utf-8') + '\n')
        with open('bigramcount', 'w') as outfile:
            for k, v in sorted(self.bgmap.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(str(v) + '\t' + k[0].encode('utf-8') + '\t' + k[1].encode('utf-8') + '\n')
        with open('invidx', 'w') as outfile:
            for k, v in sorted(self.invidx.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(k.encode('utf-8') + '\t')
                for page in v:
                    outfile.write(page + '\t')
                outfile.write('\n')

class InlinkCounter(object):
    def __init__(self):
        self.inlinks = {}

    def filter(self, href):
        if '../' not in href:
            return True

    def count(self, filepath, soup):
        links = soup.find_all('a')
        for link in links:
            if link.has_attr('href'):
                href = link['href']
                if self.filter(href):
                    continue
                href = href.replace('../', '')
                if not self.inlinks.has_key(href):
                    self.inlinks[href] = 0
                self.inlinks[href] = self.inlinks[href] + 1

    def results(self):
        with open('inlinks', 'w') as outfile:
            for k, v in sorted(self.inlinks.items(), key=operator.itemgetter(1), reverse=True):
                outfile.write(str(v) + '\t' + k.encode('utf-8') + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('word count')
    parser.add_argument('-root', '-r', help='the root directory for parsing', default='en')
    args = parser.parse_args()
    visitor = FileVisitor(args.root, [WordCounter(), InlinkCounter()])
    visitor.run()