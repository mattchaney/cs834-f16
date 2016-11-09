import cPickle

def cachewords():
    global words
    try:
        words = cPickle.load(open('words.p', 'rb'))
    except IOError:
        words = [line.split()[1] for line in open('wordcount.dat').readlines() if not line.split()[1].isdigit()]
        words = sorted(words)
        cPickle.dump(words, open('words.p', 'wb'))
        words = cPickle.load(open('words.p', 'rb'))


cachewords()

