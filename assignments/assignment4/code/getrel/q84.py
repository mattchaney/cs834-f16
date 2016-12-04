from getrel import *

def printdata(rrun, prun, fname):
    with open(fname, 'w') as fd:
        zipped = zip(rrun, prun)
        for z in zipped:
            fd.write('{0}\t{1}\n'.format(z[0], z[1]))

results = process(args.qnum)
printresults(*results)
qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip = results
printdata(rrun, prun, 'urpg{0}.dat'.format(qnum))

irrun, iprun = ipr(rrun, prun)
printdata(irrun, iprun, 'ipr{0}.dat'.format(qnum))
