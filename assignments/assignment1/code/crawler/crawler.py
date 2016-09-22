import argparse
import requests
from time import sleep
from collections import deque
from bs4 import BeautifulSoup


def crawl():
    while True:
        url = frontier.popleft()
        if url not in visited:
            print 'retrieving', url
            try:
                res = requests.get(url)
            except:
                continue
            if res.ok:
                visited.add(url)
                soup = BeautifulSoup(res.text, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    try:
                        linkurl = link['href'].strip()
                        if linkurl not in visited:
                            frontier.append(linkurl)
                    except KeyError:
                        continue
        sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('web crawler')
    parser.add_argument('--host', default='http://cs.odu.edu/~mln')
    args = parser.parse_args()
    visited = set()
    frontier = deque()
    frontier.append(args.host)
    crawl()
