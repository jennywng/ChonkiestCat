#! /usr/bin/env python

import sys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

# if __name__ == "__main__":
#     print(f"Arguments Count: {len(sys.argv)}")
#     for i, arg in enumerate(sys.argv):
#         print(f"Argument {i:>6}: {arg}")
#

cat_url = "http://humanesocietysoco.org/adopt/cats/"
cat_url1 = "https://www.sfspca.org/wp-json/sfspca/v1/filtered-posts/get-adoptions?per_page=100"


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    # print(f"content type: {content_type}")
    # print(f"status code: {resp.status_code}")
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_cats(url):
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

        with closing(get(url, stream=True, headers=headers)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print("No cats right now :(")
                return None
    except RequestException as e:
        print(f"Error getting cats: {e}")


cats_html_raw = get_cats(cat_url)


soup = BeautifulSoup(cats_html_raw, "html.parser")
divs = soup.find_all('div', {"class": ["dog", "Cat"]})


nameTags = []
descTags = []

for div in divs:
    nameTags.append(div.find_all('div', {"class": "name"})[0])
    descTags.append(div.find_all('div', {"class": "description"})[0])


catInfo = {}
for i in range(len(divs)):
    weight = re.search(r'([0-9]+\.*[0-9]*)(lbs)', descTags[i].text)
    if weight:
        catInfo[nameTags[i].text] = float(weight.group(1))
    else:
        catInfo[nameTags[i].text] = 0.0

# print(catInfo)

print('--------------------------------------------------')
maxWeight = 0
maxCat = ''

print("Searching for fat cats ...")

for cat, weight in catInfo.items():
    print(f"Weighing {cat}")
    # print(f"{cat} is {weight} lbs")
    if weight > maxWeight:
        maxWeight = weight
        maxCat = cat

print("Weighing complete")
print(f"Chonkiest cat is: {maxCat} at {maxWeight} lbs")

print('--------------------------------------------------')



