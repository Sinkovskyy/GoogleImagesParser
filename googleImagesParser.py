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

    # Limit for downloading image in seconds
    __timeLimit = 0
    __DELAY = 0.2

    # Initializate webdriver
    def __init__(self,timeLimit = 3,headless = True):
        option = Options()
        self.__timeLimit = timeLimit
        if headless:
            option.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path="geckodriver.exe",options=option)

      # Check if url is base64 encoded
    def __is_base64_encoded(self,url):
        if url.find("data:image/jpeg;base64") != -1:
            return True
        else:
            return False
    
    def __is_encrypted(self,url):
        if not url.find("https://encrypted"):
            return True
        else:
            return False


    # Decode base64 image 
    def __decode_base64(self,url):
        url = url[url.find("/9"):]
        return base64.b64decode(url)

    # Create url for google search 
    def __create_search_link(self,request_value,resolution):
        search = "+".join(request_value.split())
        if 0 not in resolution:
            search += "+imagesize%3A" + "x".join([str(i) for i in resolution])
        url = "https://www.google.com/search?q="+ search +"&tbm=isch"
        return url

    # Get image url via alt attribute
    def __get_image_url(self,url,alt_val):
        self.driver.get(url)
        sleep(0.3) # Time for google to load image and via this driver can sync and get valid html source
        # Parse image
        html = self.driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        imgs = soup.findAll(attrs={"class":"n3VNCb","alt":alt_val})
        img = imgs[0]["src"]
        # Waiting while google download image 
        time = 0
        while (self.__is_base64_encoded(img) or self.__is_encrypted(img)) and time < self.__timeLimit: 
            time += self.__DELAY
            sleep(self.__DELAY)
            html = self.driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            imgs = soup.findAll(attrs={"class":"n3VNCb","alt":alt_val})
            img = imgs[0]["src"]     
        return img

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
        imgs = self.driver.find_elements_by_css_selector("div.mJxzWe img.Q4LuWd")
        return imgs

    # Find images url by request
    def get_images_url(self,request_value,amount = 1,resolution = {0,0},ignore_bad_quality_img = False):
        url = self.__create_search_link(request_value,resolution)
        imgs_url = []
        i = 0
        while i < amount:
            imgs = self.__find_all_imgs(url)
            img = imgs[i]
            alt_val = self.__get_alt_value(img)
            url = self.__click(img)
            img_url = self.__get_image_url(url,alt_val)
            i += 1
            if ignore_bad_quality_img and (self.__is_base64_encoded(img_url) or self.__is_encrypted(img_url)):
                amount += 1
                continue
            imgs_url.append(img_url)
        return imgs_url 

  
        

    # Download single image
    def __download_image(self,img,request_value):
        # create path for image
        req_words = request_value.split()
        dir = "_".join(req_words[:5] if len(req_words) > 5 else req_words)
        dir = "images/" + dir + "/"
        pathlib.Path(dir).mkdir(parents=True,exist_ok=True)
        # create file name for image and ckeck if such a file exist
        r = int(random.uniform(10000000000,999999999999))
        while isfile(dir + str(r) + ".png"):
            r = int(random.uniform(10000000000,999999999999))
        # download image
        f = open(dir + str(r) + ".png","wb")
        f.write(img)
        f.close()
        


    def download_images(self,request_value,amount=1,resolution = {0,0},ignore_bad_quality_img = False):
        imgs_url = self.get_images_url(request_value,amount,resolution,ignore_bad_quality_img)
        for url in imgs_url:
            if self.__is_base64_encoded(url):
                file = self.__decode_base64(url)
            else:
                try:
                    file = requests.get(url).content
                except Exception:
                    continue
            self.__download_image(file,request_value)


