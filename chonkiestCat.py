import sys
import urllib.request
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing


if __name__ == "__main__":
    print(f"Arguments Count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")


cat_url = "http://humanesocietysoco.org/adopt/cats/"

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_cats(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print("No cats right now :(")
                return None
    except RequestException as e:
        print("Error getting cats")



cats_html = get_cats(cat_url)
len(cats_html)
print(raw_html)