#!/usr/bin/python

import argparse
import re
import requests
import xmltodict
from bs4 import BeautifulSoup
from pprint import pprint as pp


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--qnum', type=int, default=10, help='the query number to use')
    parser.add_argument('-n', type=int, default=10, help='the number of results to retrieve')
    return parser.parse_args()


args = parseargs()


def buildrel():
    rel = {}
    for line in open('cacm.rel').readlines():
        q, _, doc, _ = line.split()
        if q not in rel:
            rel[q] = []
        rel[q].append(int(doc.split('-')[1]))
    return rel


def buildqueries():
    with open('cacm.query.xml') as fd:
        return xmltodict.parse(fd.read())


REL = buildrel()
QUERIES = buildqueries()
RE = re.compile('/home/mchaney/workspace/edu/cs834-f16/assignments/assignment4/code/cacm/docs/CACM-([\d]+).html')
ID = {'id':'result'}
URL = 'http://0.0.0.0:{0}/search'
QUERY1 = 'what articles exist which deal with tss time sharing system an operating system for ibm computers'
QUERY10 = 'parallel languages languages for parallel computation'
PDICT = {'q': QUERY1, 'start': 0, 'n': args.n}

def query(qstr, port=54312):
    PDICT['q'] = qstr
    PDICT['n'] = args.n
    res = requests.get(URL.format(port), params=PDICT)
    if not res.ok:
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    return [int(RE.match(href.text).groups()[0]) for href in soup.select("#result a")]

# precision is the proportion of retrieved documents that are relevant
# recall is the proportion of relevant documents that are retrieved

def recall(rel, retr):
    relset = set(rel)
    retrset = set(retr)
    return float(len(relset.intersection(retrset))) / len(relset)


def precision(rel, retr):
    relset = set(rel)
    retrset = set(retr)
    return float(len(relset.intersection(retrset))) / len(retrset)


def run(rel, retr, func):
    rr = []
    for i in range(1, len(retr)+1):
        rr.append(func(rel, retr[:i]))
    return rr


def avg(rel, retr, func):
    prun = run(rel, retr, precision)
    res = []
    for i in range(len(retr)):
        if retr[i] in rel:
            res.append(prun[i])
    return float(sum(res))/len(res)


def getquery(qnum):
    return QUERIES['parameters']['query'][qnum-1]['text']


def process(qnum):
    qstr = getquery(qnum)
    retr = query(qstr)
    rel = REL[str(qnum)]
    prun = run(rel, retr, precision)
    prec = precision(rel, retr)
    rec = recall(rel, retr)
    avgprec = avg(rel, retr, precision)
    return qnum, qstr, retr, rel, prun, prec, rec, avgprec


def printresults(qnum, qstr, retr, rel, prun, prec, rec, avgprec):
    print 'using query', qnum
    print 'query:', qstr
    print 'precision:', prec
    print 'recall:', rec
    print 'average precision:', avgprec
    if args.n == 10:
        print 'relevant:', rel
        print 'retrieved:', retr
        print 'p-run:', prun


if __name__ == '__main__':
    printresults(*process(args.qnum))
