#!/usr/bin/python

import argparse
import re
import requests
import xmltodict
from math import log
from bs4 import BeautifulSoup


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


def getrel(rel, retr, i):
    return 1 if retr[i] in rel else 0


def DCG(rel, retr, p):
    sum = 0
    for i in range(2, p+1):
        sum += float(getrel(rel, retr, i-1)) / log(i, 2)
    return getrel(rel, retr, 0) + sum

def IDCG(p):
    sum = 0
    for i in range(2, p+1):
        sum += 1 / log(i, 2)
    return 1 + sum


def NDCG(rel, retr, p):
    dcg = DCG(rel, retr, p)
    idcg = IDCG(p)
    return dcg / idcg


def reciprank(rel, retr):
    for i in range(1, len(retr)+1):
        if retr[i-1] in rel:
            return 1.0 / i
    return 0.0


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
    ndcg5 = NDCG(rel, retr, 5)
    ndcg10 = NDCG(rel, retr, 10)
    recip = reciprank(rel, retr)
    return qnum, qstr, retr, rel, prun, prec, rec, ndcg5, ndcg10, avgprec, recip


def printresults(qnum, qstr, retr, rel, prun, prec, rec, ndcg5, ndcg10, avgprec, recip):
    print 'query {0}'.format(qnum)
    print 'query: {0}'.format(qstr)
    if args.n == 10:
        print 'relevant: {0}'.format(rel)
        print 'retrieved: {0}'.format(retr)
        print 'p-run: {0}'.format(prun)
    print 'precision: {0}'.format(prec)
    print 'recall: {0}'.format(rec)
    print 'precision @10: {0}'.format(prun[9])
    print 'NDCG @5: {0}'.format(ndcg5)
    print 'NDCG @10: {0}'.format(ndcg10)
    print 'avg precision: {0}'.format(avgprec)
    print 'reciprocal rank: {0}'.format(recip)


TABLE = """\\begin{{table}}[h!]
\\centering
\\begin{{tabular}}{{ | c | c | c | c | c | c | }}
\\hline
Query \# & Avg. Prec. & NDCG @5 & NDCG @10 & Prec. @10 & Recip. Rank \\\\
\\hline
{0} & {1} & {2} & {3} & {4} & {5} \\\\
\\hline
\\end{{tabular}}
\\caption{{Calculations for CACM query {6} from top {7} retrieved documents.}}
\\label{{tab:query20}}
\\end{{table}}
"""

def printtab(qnum, qstr, retr, rel, prun, prec, rec, ndcg5, ndcg10, avgprec, recip):
    fname = 'query{0}.tab'.format(qnum)
    with open(fname, 'w') as fd:
        fd.write(TABLE.format(qnum, avgprec, ndcg5, ndcg10, prun[9], recip, qnum, args.n))


results = process(args.qnum)
printresults(*results)
printtab(*results)    
