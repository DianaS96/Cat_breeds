import os
import requests
from bs4 import BeautifulSoup
import lxml

CAT_BREEDS_URL = "https://www.purina.com/cats/cat-breeds?page="
FILE = "breeds.html"
cat_breeds = []

def get_page():
    i = 0
    while (1):
        url = CAT_BREEDS_URL + f"{i}"
        url_content = requests.get(url).text
        tree = BeautifulSoup(url_content, 'lxml')
        pagination = tree.find_all(class_="paginationSkip-label")
        if (pagination[-1].text == "Previous page"):
            return (i)
        else:
            i += 1


def get_cat_breeds(i):
    j = 0
    while (j <= i):
        url = CAT_BREEDS_URL + f"{j}"
        content = requests.get(url).text
        soup = BeautifulSoup(content, "lxml")
        breeds = soup.find_all(class_="callout-label")

        for breed in breeds:
            cat_breeds.append(breed.text.replace('\n', ''))
        j += 1

if __name__ == "__main__":
    pages = int(get_page())
    get_cat_breeds(pages)

    with open("cat_breeds.txt", 'w', encoding="utf-8") as file:
        for breed in cat_breeds:
            file.write(breed + '\n')
