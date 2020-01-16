import pandas as pd
from selenium import webdriver

if __name__ == "__main__":
    url_string = "https://jendela360.com/search"
    executable_path = "C:/Users/okzam/AppData/Local/Temp/Rar$EXa15924.25956/chromedriver.exe" #chromedriver path
    driver = webdriver.Chrome(executable_path)

    driver.get(url_string)


    #using beautifulsoup, cant get result because of javascript.
    #open_url = Request(url_string, headers={'User-Agent': 'Chrome/51.0.2704.103'})
    #uReq = urlopen(open_url)
    #page_html = uReq.read()
    #uReq.close()
    #page_html_soup = soup(page_html, "lxml")
    #unit_card = page_html_soup.findAll("div", {"class": "unit-tile-container"})
    #print(unit_card)