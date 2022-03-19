import os

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

PATH_DIR = 'C:/Users/User/Desktop/Programming/Cat_breeds/'
WEBDRIVER_PATH = 'C:/Users/User/Desktop/Programming/Cat_breeds/webdriver/chromedriver.exe'


def make_dir():
    path_data = PATH_DIR + 'cats_dataset/'

    if not os.path.exists(path_data):
        os.makedirs(path_data)

    img_dir_path = path_data + 'img/'

    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)

    return img_dir_path


# source: https://www.youtube.com/watch?v=Yt6Gay8nuy0
def get_link(breed, folder_name):
    img_urls = set()
    driver = webdriver.Chrome(WEBDRIVER_PATH)
    driver.maximize_window()
    search = breed.replace(' ', '+')
    search_url = f'https://www.google.com/search?q={search}&source=lnms&tbm=isch'
    driver.get(search_url)

    #Scrolling
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    #Find all containers with images and its links
    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.find_all('div', {'class':'isv-r PNCib MSM1fd BUooTd'})

    length = len(containers)

    #print(f'found {length} containers')

    #xpath:
    #//*[@id="islrg"]/div[1]/div[1]
    #selector:
    ##islrg > div.islrc > div:nth-child(2)

    for i in range(1, length):
        if i % 25 == 0:
            continue
        xpath = f'//*[@id="islrg"]/div[1]/div[{i}]'
        #Grabbing url of small image
        #//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
        previewimgXpath = f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img'
        previewimgElem = driver.find_element(by=By.XPATH, value=previewimgXpath)
        previewimgURL = previewimgElem.get_attribute("src")

        driver.find_element(by=By.XPATH, value=xpath).click()

        timeStarted = time.time()
        while True:
            #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img
            imgXpath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img'
            imgElem = driver.find_element(by=By.XPATH, value=imgXpath)
            imgURL = imgElem.get_attribute('src')

            if imgURL != previewimgURL:
                break
            else:
                currentTime = time.time()
                if currentTime - timeStarted > 10:
                    print("Timeout!")
                    break
                img_urls.add(imgURL)

        try:
            img_download(imgURL, folder_name, i)
            print(f"Img #{i} for {breed} successfully downloaded")
        except:
            print(f"Can not download img #{i} for {breed}")
    driver.close()


def img_download(url, folder_name, num):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, str(num) + ".jpg"), 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    cat_breeds = []

    with open('cat_breeds.txt', 'r') as file:
        for breed in file:
            cat_breeds.append(breed.replace('\n', ''))
    #print(cat_breeds)
    #print(len(cat_breeds))
    img_dir_path = make_dir()

    i = 0
    for breed in cat_breeds:
        folder_name = img_dir_path + breed.replace(' ', '_')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        if (i > 41):
            get_link(breed, folder_name)
        i += 1