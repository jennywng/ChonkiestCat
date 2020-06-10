#! /usr/bin/env python

import sys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print(f"Arguments Count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")


cat_url = "http://humanesocietysoco.org/adopt/cats/"
cat_url1 = "https://www.sfspca.org/wp-json/sfspca/v1/filtered-posts/get-adoptions?per_page=100"


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    print(f"content type: {content_type}")
    print(f"status code: {resp.status_code}")
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_cats(url):
    try:
        response = get(url)
        print(response)
        return response.content
        # with closing(get(url, stream=True)) as resp:
        #     if is_good_response(resp):
        #         return resp.content
        #     else:
        #         print("No cats right now :(")
        #         return None
    except RequestException as e:
        print(f"Error getting cats: {e}")


cats_html_raw = get_cats(cat_url1)
# len(cats_html_raw)
# print(cats_html_raw)
#
# html = BeautifulSoup(cats_html_raw, 'html.parser')
# for i, div in enumerate(html.select('div')):
#     if div['class'] == 'description':
#         print(div.text)
        



