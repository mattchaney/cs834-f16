from getrel import *

results = process(args.qnum)
printresults(*results)

qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip = results

with open('urpg{0}.dat'.format(qnum), 'w') as fd:
    zipped = zip(rrun, prun)
    for z in zipped:
        fd.write('{0}\t{1}\n'.format(z[0], z[1]))
