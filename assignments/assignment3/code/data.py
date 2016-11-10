import cPickle

try:
    print 'loading cached word map'
    words = cPickle.load(open('wordcount.p', 'rb'))
except IOError:
    words = {line.split()[0]: line.split()[1:] for line in open('invidx.dat').readlines()}
    cPickle.dump(words, open('wordcount.p', 'wb'))
    words = cPickle.load(open('wordcount.p', 'rb'))
N = float(sum(len(docs) for docs in words.values()))
