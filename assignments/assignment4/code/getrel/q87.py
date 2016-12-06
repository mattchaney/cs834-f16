from getrel import *

for qnum in args.qnum:
    qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip = process(qnum)
    printresults(qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip)
    rprec = rprecision(rel, prun)
    print '|R|: {}'.format(len(rel))
    print 'R-precision: {}'.format(rprec)