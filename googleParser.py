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

        # Time for google to load image and via this driver can sync and get valid html
        sleep(0.3)

        html = self.driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        imgs = soup.findAll(attrs={"alt":alt_val})
        return imgs[-1]["src"]


    def parse(self,request_value,amount = 1,resolution = ""):
        url = self.__create_search_link(request_value,resolution)
        
    
    

    


    # Finish driver work
    def close(self):
        self.driver.close()



















# driver.close()