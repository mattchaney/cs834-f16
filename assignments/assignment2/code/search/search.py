import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser('basic search engine')
    parser.add_argument('-file','-f', help='the file to search', default='invidx.dat')
    parser.add_argument('-terms', '-t', nargs='+', help='terms to search for')
    args = parser.parse_args()

    #initialize results map
    results = {}
    for term in args.terms:
        results[term] = set()

    # iterate over inverted index, matching terms and docs
    with open(args.file) as infile:
        for line in infile:
            parts = line.split('\t')
            term = parts[0]
            docs = parts[1:]
            if term in args.terms:
                for doc in docs:
                    results[term].add(doc)

    # print results
    for term, docs in results.items():
        print term,' '.join(docs)