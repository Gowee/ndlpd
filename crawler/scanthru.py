#!/usr/bin/env python3
from pathlib import Path

import requests

IDLIST = Path(__file__).parent / 'ids.txt'

BOOK_INFO_URL = "https://dl.ndl.go.jp/api/item/search/info:ndljp/pid/"

USER_AGENT = "ndlpdbot/0.0(+https://github.com/Gowee/ndlpd)"

def main():
    with open(IDLIST, 'r') as f:
        ids = f.read()
    ids = list(map(int, ids))
    ids.sort()

    for i, j in zip(ids, ids[1:]):
        if j - i > 1:
            print(i)
            break
        
def fetch_info(bookid):
    requests.get(BOOK_INFO_URL + str(bookid), headers={'User-Agent': USER_AGENT})
    requests.raise_for_status()

if __name__ == '__main__':
    main()
