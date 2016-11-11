#!/usr/bin/env python

from stem import *

# skipping first 13,000 terms because they are all numeric
# and won't meet language probability expectations
first1k = sorted(words.keys())[13000:14000]

classes, results = getstems(first1k)
printtables('clustertab.tex', classes)

filtered = {stem: [result for result in rset if result.getdice() > 0.1] for stem, rset in results.items()}
converted = convert(filtered)
printtables('clustertab.tex', converted, mode='a')

filtered = {stem: [result for result in rset if result.getdice() > 0.00001] for stem, rset in results.items()}
converted = convert(filtered)
printtables('clustertab.tex', converted, mode='a')
