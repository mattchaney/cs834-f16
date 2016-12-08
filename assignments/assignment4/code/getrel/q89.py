from getrel import *

HEAD = """\\begin{table}[H]
\\centering
\\begin{tabular}{ | l | l | l | l |}
\\hline
Query & R & BPREF(1) & BPREF(2) \\\\
\\hline
"""

ROW = """{} & {} & {} & {}\\\\
\\hline
"""

TAIL = """\\end{tabular}
\\caption{Table of BPREF values for a selection of CACM queries.}
\\label{tab:bpref}
\\end{table}
"""

def printtab(values):
    with open('q89.tab', 'w') as fd:
        fd.write(HEAD)
        for qnum, R, b1, b2 in values:
            fd.write(ROW.format(qnum, R, b1, b2))
        fd.write(TAIL)

def getsub(rel, retr):
    """bound the size of retrieved list by R non-relevant documents"""
    sub = []
    count = 0
    for doc in retr:
        if doc not in rel:
            count += 1
        if count > len(rel):
            break
        sub.append(doc)
    return sub

values = []
for qnum in args.qnum:
    results = process(qnum)
    retr, rel = results[2], results[3]
    if not retr:
        print 'no results for query {}'.format(qnum)
        continue
    sub = getsub(rel, retr)
    b1 = bpref1(rel, sub)
    b2 = bpref2(rel, sub)
    print 'Query:  {}'.format(qnum)
    print 'R: {}'.format(len(rel))
    print 'BPREF1: {}'.format(b1)
    print 'BPREF2: {}'.format(b2)
    values.append((qnum, len(rel), b1, b2))
printtab(values)