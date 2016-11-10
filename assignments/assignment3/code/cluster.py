#!/usr/bin/env python

from stem import *

def printtables(resultset, mode='w'):
    head = '\\begin{table}[h!]\n\\centering\n\\begin{tabular}{ | c | c | }\n'
    foot = '\\hline\n\\end{tabular}\n\\caption{``%s\'\' stems}\n\\label{tab:%s}\n\\end{table}\n'
    print 'writing tables'
    with open('clustertab.tex', mode) as outfile:
        outfile.write('\n\n\n\\noindent\n')
        for stemclass in resultset.items():
            outfile.write(stemclass[0])
            outfile.write(': ')
            outfile.write(', '.join(stemclass[1]))
            outfile.write('\\\\\n')

def convert(filtered):
    converted = {}
    for stem, fres in filtered.items():
        if len(fres) > 0:
            res = set()
            for result in fres:
                res.add(result.a)
                res.add(result.b)
            converted[stem] = res
    return converted

# skipping first 13,000 terms because they are all numeric
# and won't meet language probability expectations
first1k = sorted(words.keys())[13000:14000]

classes, results = getstems(first1k)
printtables(classes)

filtered = {stem: [result for result in rset if result.getdice() > 0.1] for stem, rset in results.items()}
converted = convert(filtered)
printtables(converted, mode='a')

filtered = {stem: [result for result in rset if result.getdice() > 0.00001] for stem, rset in results.items()}
converted = convert(filtered)
printtables(converted, mode='a')
