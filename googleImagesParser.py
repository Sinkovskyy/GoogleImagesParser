from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep 
import io
import requests
from PIL import Image
from os.path import isfile
import random
import pathlib
import base64



class GoogleImagesParser:

    # Initializate webdriver
    def __init__(self):
        option = Options()
        # option.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path="geckodriver.exe",options=option)

    # Create url for google search 
    def __create_search_link(self,request_value,resolution):
        search = "+".join(request_value.split())
        if resolution:
            search += "+imagesize%3A" + resolution
        url = "https://www.google.com/search?q="+ search +"&tbm=isch"
        return url

    # Get image url via alt attribute
    def __get_image_url(self,url,alt_val):
        self.driver.get(url)
        sleep(0.3) # Time for google to load image and via this driver can sync and get valid html source
        # Parse image
        html = self.driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        imgs = soup.findAll(attrs={"alt":alt_val})
        return imgs[-1]["src"]

    # Simulate click on image and get a new url
    def __click(self,img):
        img.location_once_scrolled_into_view
        img.click()
        return self.driver.current_url   

    # Get alt attribute value via which we can idintify our image
    def __get_alt_value(self,img):
        return img.get_attribute("alt")

    # Find all images elements
    def __find_all_imgs(self,url):
        self.driver.get(url)
        # div.mJxzWe its a div that contain all images
        imgs = self.driver.find_elements_by_css_selector("div.mJxzWe img")
        return imgs

    # Find images url by request
    def get_images_url(self,request_value,amount = 1,resolution = ""):
        url = self.__create_search_link(request_value,resolution)
        imgs_url = []
        for i in range(0,amount):
            imgs = self.__find_all_imgs(url)
            img = imgs[i]
            alt_val = self.__get_alt_value(img)
            url = self.__click(img)
            img_url = self.__get_image_url(url,alt_val)
            imgs_url.append(img_url)
        return imgs_url 

    def __decode_base64(self,url):
        if url.find("data:image/jpeg;base64") != -1:
            url = url[url.find("/9"):]
            return base64.b64decode(url)
        else:
            return url
            


    def __download_image(self,img,request_value):
        req_words = request_value.split()
        dir = "_".join(req_words[:5] if len(req_words) > 5 else req_words)
        dir = "images/" + dir + "/"
        pathlib.Path(dir).mkdir(parents=True,exist_ok=True)
        r = int(random.uniform(10000000000,999999999999))
        while isfile(dir + str(r) + ".png"):
            r = int(random.uniform(10000000000,999999999999))
        f = open(dir + str(r) + ".png","wb")
        f.write(img)
        f.close()
        


    def download_images(self,request_value,amount=1,resolution = ""):
        imgs_url = self.get_images_url(request_value,amount,resolution)
        for url in imgs_url:
            url = self.__decode_base64(url)
            file = requests.get(url).content
            self.__download_image(file,request_value)
            


    # Finish driver work
    def close(self):
        self.driver.close()

