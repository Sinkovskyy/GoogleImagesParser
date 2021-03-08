from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep 



class GoogleImageParser:

    # Initializate webdriver
    def __init__(self):
        option = Options()
        option.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path="geckodriver.exe",options=option)

    # Create url for google search 
    def __create_search_link(self,request_value,resolution):
        search = "+".join(request_value.split())
        if resolution:
            search = resolution + "+" + search
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
        imgs = self.driver.find_elements_by_tag_name("img")
        return imgs

    def get_images(self,request_value,amount = 1,resolution = ""):
        url = self.__create_search_link(request_value,resolution)
        imgs_url = []
        for i in range(amount):
            imgs = self.__find_all_imgs(url)
            img = imgs[i]
            alt_val = self.__get_alt_value(img)
            url = self.__click(img)
            img_url = self.__get_image_url(url,alt_val)
            imgs_url.append(img_url)
        return imgs_url   
    

    


    # Finish driver work
    def close(self):
        self.driver.close()


