import requests
import os
import argparse
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from utils import append_to_file

# parse arguments
parser = argparse.ArgumentParser(description='inspect pages contain an id')
parser.add_argument('-p', '--arg1')
parser.add_argument('arg2', help='base url')
parser.add_argument('arg3', help='id')
args = parser.parse_args()


def find_target_id(html, target_id):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", attrs={"id": target_id})
    return div


def process():
    # read path file
    path = args.arg1
    base_url = urlparse(args.arg2)
    target_id = args.arg3

    # parse base url
    base_url = args.arg2 if base_url.scheme else "https://" + args.arg2
    lines = tuple(open(path, "r"))

    for x in lines:
        desire_path = x.replace("\n", "")
        url = base_url + desire_path
        try:
            r = requests.get(url)
            res = find_target_id(r.text, target_id)
            if res is None:
                err = os.path.basename("error.txt")
                append_to_file(err, url)
            else:
                result = os.path.basename("result.txt")
                append_to_file(result, url)
                print(url)
        except:
            err = os.path.basename("error.txt")
            append_to_file(err, url)


if __name__ == '__main__':
    process()
