import cPickle
import math


class Result(object):
    def __init__(self, a, b):
        """calculate MIM, EMIM, Chi-square, and Dice's coefficient for words a and b.
        mim  = nab / (na * nb)
        emim = nab * log [ N * nab / ( na * nb ) ]
        x2   = ( nab - ( 1 / N ) * na * nb )^2 / ( na * nb )
        dice = nab / ( na + nb )"""
        self.a = a
        self.b = b
        sa = set(words[a])
        sb = set(words[b])
        sab = sa.intersection(sb)
        na = float(len(sa))
        nb = float(len(sb))
        nab = float(len(sab))
        self.mim = nab / (na * nb)
        try:
            self.emim = nab * math.log(N * nab / (na * nb))
        except Exception as e:
            self.emim = 0.0
        self.x2 = (nab - (1/N) * na * nb)**2 / (na * nb)
        self.dice = nab / (na + nb)

    def getmim(self):
        return self.mim

    def getemim(self):
        return self.emim

    def getx2(self):
        return self.x2

    def getdice(self):
        return self.dice

    def __repr__(self):
        return '({},{})\n  MIM  {}\n  EMIM {}\n  X2   {}\n  Dice {}'.format(
            self.a, self.b, self.mim, self.emim, self.x2, self.dice)


def init():
    global words
    try:
        print 'loading cached word map'
        words = cPickle.load(open('words.p', 'rb'))
    except IOError:
        print 'cached word map not found, building now'
        words = {line.split()[0]: line.split()[1:] for line in open('invidx.dat').readlines()}
        cPickle.dump(words, open('words.p', 'wb'))
        words = cPickle.load(open('words.p', 'rb'))
    global N
    N = float(sum(len(docs) for docs in words.values()))


def calc(choices):
    print 'calculating...'
    return {choice: [Result(choice, word) for word in words.keys() if choice != word] for choice in choices}


def gethighest(results, choice, keyfunc):
    return sorted(results[choice], key=keyfunc, reverse=True)[:10]


def printresults(results, choices):
    print 'writing tables.tex'
    with open('tables.tex', 'wb') as outfile:
        for choice in choices:
            mim  = [res.b for res in gethighest(results, choice, Result.getmim)]
            emim = [res.b for res in gethighest(results, choice, Result.getmim)]
            x2   = [res.b for res in gethighest(results, choice, Result.getx2)]
            dice = [res.b for res in gethighest(results, choice, Result.getdice)]
            printtab(outfile, choice, mim, emim, x2, dice)


head = """\\begin{table}[h!]
\centering
\\begin{tabular}{ l | c | c | c }
\hline
"""

foot = '\\hline\n\\end{tabular}\n\\caption{Calculated values for ``%s\'\'}\n\\label{tab:words}\n\\end{table}\n'

def printtab(outfile, choice, mim, emim, x2, dice):
    outfile.write(head)
    outfile.write('\\multicolumn{4}{c}{'
        + choice + '}\\\\\n\\hline\n\\textit{MIM} & \\textit{EMIM} & \\textit{\(\chi^2\)} & \\textit{Dice}\\\\\n\\hline\n')
    for i in range(10):
        outfile.write(row(i, mim, emim, x2, dice))
    outfile.write(foot % choice)

def row(r, mim, emim, x2, dice):
    return mim[r] + ' & ' + emim[r] + ' & ' + x2[r] + ' & ' + dice[r] + '\\\\\n'



init()
choices = [
    'running',
    'calculation',
    'color',
    'horse',
    'sky',
    'railroad',
    'calendar',
    'airplane',
    'ocean',
    'bicycle']
results = calc(choices)
printresults(results, choices)
