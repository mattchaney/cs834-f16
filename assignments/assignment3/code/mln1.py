#!/usr/bin/env python

from stem import *
import networkx as nx
import matplotlib.pyplot as plt

wordlist = [
    'affiliates',
    'affiliation',
    'affiliated',
    'fire',
    'firing',
    'fired',
    'changing',
    'changed',
    'changes',
    'change'
]

def buildgraph(filtered):
    graph = nx.Graph()
    for stem, results in filtered.items():
        for result in results:
            graph.add_edge(result.a, result.b)
    return graph

classes, results = getstems(wordlist)
printtables('mln1tab.tex', classes)

filtered = {stem: [result for result in rset if result.getdice() > 0.1] for stem, rset in results.items()}
converted = convert(filtered)
printtables('mln1tab.tex', converted, mode='a')

graph = buildgraph(filtered)
figure = plt.figure()
nx.draw_networkx(graph)
figure.savefig('figure1.png')
