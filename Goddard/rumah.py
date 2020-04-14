import os
import pandas as pd
import math
import json
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from datetime import datetime
from pytz import timezone

def scrap_region():
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    timeout_wait = 5
    driver.get('https://www.rumah123.com/')
    try:
        presence_element = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.displayToggle > a'))
        WebDriverWait(driver, timeout_wait).until(presence_element)
        print('Loading finished')
    except TimeoutException:
        print('Time out waiting Tampilkan Lebih Lengkap text')
    finally:
        new_housing_el = driver.find_elements(By.CSS_SELECTOR, 'div.container > div')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        toggle_el = driver.find_element(By.CSS_SELECTOR, 'div.displayToggle > a')
        print('toggle', toggle_el)
        driver.execute_script("arguments[0].click()", toggle_el)
        print(len(new_housing_el))
        links = [ housing.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for housing in new_housing_el ]
        print('New housing', links)

        return links

def scrap_properties(regions):
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    properties = []
    timeout_wait = 20
    for region in range(3):
        print("\nCurrent region: ", regions[region])
        driver.get(regions[region])
        try:
            presence_element = EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='https://www.rumah123.com/properti/']"))
            WebDriverWait(driver, timeout_wait).until(presence_element)
            print('Loading finished')
        except TimeoutException:
            print('Time out waiting all aparts finished loading')
        finally:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            pagination = driver.find_elements(By.CSS_SELECTOR, "ul.page-range-pagination > li")
            if len(pagination) > 0:
                print("Ada pagination!")
                list_pagination = [ page.text for page in pagination ]
                print(list_pagination)
            property_el = driver.find_elements(By.CSS_SELECTOR, "div.jiwck > ul.hqtMPr > li.hrjLKa")
            print("How many aparts?", len(property_el))
            links = []
            for prop in property_el:
                property_selector = "a[href^='https://www.rumah123.com/properti/']"
                new_house_selector = "a[href^='https://www.rumah123.com/perumahan-baru/']"
                if len(prop.find_elements(By.CSS_SELECTOR, property_selector)) > 0:
                    prop_link = prop.find_element(By.CSS_SELECTOR, property_selector).get_attribute('href')
                else:
                    prop_link = prop.find_element(By.CSS_SELECTOR, new_house_selector).get_attribute('href')
                links.append(prop_link)
            properties.extend(links)
            print("Current properties link: ", properties)
    print("Properties Link: ", properties)
    return properties

def scrap(properties):
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    now = datetime.now()
    now_timestamp = datetime.timestamp(now)
    properties_info = []


    for prop in properties:
        driver.get(prop)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        print("Current link: ", prop)
        title_el = driver.find_element(By.CLASS_NAME, 'description-title')
        desc_el = driver.find_element(By.CLASS_NAME, 'property-description')
        price_el = driver.find_element(By.CSS_SELECTOR, 'div.property-price')
#        installment_el = driver.find_element(By.CSS_SELECTOR, 'div.money-per-month')
        address_el = driver.find_element(By.CSS_SELECTOR, 'span.property-address')

        title = title_el.text
        price = price_el.text
#        installment = installment_el.text
        desc = desc_el.text
        address = address_el.text

        property_tabs = driver.find_elements(By.CSS_SELECTOR, 'div.ant-tabs-nav-wrap')

        print("Title: ", title)
        print("Desc: ", desc)
        print("Price: ", price)
#        print("Installment: ", installment)
        print("Address: ", address)
        more_btn = driver.find_elements(By.CSS_SELECTOR, 'div.ant-tabs-tabpane div.show-more-button')

        if(len(property_tabs) > 0):
            print("Ada tab Properti!")
            prop_tab_el = driver.find_elements(By.CSS_SELECTOR, 'div.ant-tabs-nav > div.ant-tabs-tab')
            for prop in prop_tab_el: #loop Tabs in Properti
                tab_text = prop.text
                print("Tab text: ", tab_text)
                driver.execute_script("arguments[0].click()", prop)
                if len(more_btn) > 0:
                    print("Ada more button!")
                    more_btn_el = driver.find_element(By.CSS_SELECTOR, 'div.ant-tabs-tabpane > div.ShowMorestyle__ShowMoreContainer-OZuAg > div.show-more-button > a')
                    print("more btn text:", more_btn_el.text)
                    driver.execute_script("arguments[0].click()", more_btn_el)
                    driver.implicitly_wait(10)
                if tab_text == "Detil properti":
                    properties_detail = driver.find_elements(By.CSS_SELECTOR, 'div.iIZHa > div')
                    properties_detail_text = [ prop.text for prop in properties_detail ] #still contains \n between key and value
                    properties_detail_text_delim = [ re.sub('\n', ' ', prop).split(':') for prop in properties_detail_text ]
                    print(properties_detail_text_delim)            
                    properties_detail_dict = dict((key, value) for key, value in properties_detail_text_delim)
                elif tab_text == "Fasilitas":
                    facility_el = driver.find_element(By.CSS_SELECTOR, 'div.feature-description-content')
                    properties_detail_dict = {tab_text: facility_el.text}
                print("Detail Properties: ", properties_detail_dict)
        else:
            print("Tidak ada tab properti!")
            if len(more_btn) > 0:
                print("Ada more button!")
                more_btn_el = driver.find_element(By.CSS_SELECTOR, 'div.ant-tabs-tabpane > div.ShowMorestyle__ShowMoreContainer-OZuAg > div.show-more-button > a')
                print("more btn text:", more_btn_el.text)
                driver.execute_script("arguments[0].click()", more_btn_el)
                driver.implicitly_wait(10)

            properties_detail = driver.find_elements(By.CSS_SELECTOR, 'div.iIZHa > div')
            properties_detail_text = [ prop.text for prop in properties_detail ] #still contains \n between key and value
            properties_detail_text_delim = [ re.sub('\n', ' ', prop).split(':') for prop in properties_detail_text ]
            print(properties_detail_text_delim)
            properties_detail_dict = dict((key, value) for key, value in properties_detail_text_delim)

        
        property_dict = {
            'nama properti': title,
            'deskripsi': desc,
            'harga': price,
            #'angsuran': installment,
            'alamat': address
        }

        property_dict.update(properties_detail_dict)

        print("\nProperty JSON: ", property_dict)
        properties_info.append(property_dict)
        print("*"*20, '\n')
    
    with open('../files/rumah123_{}.json'.format(now_timestamp), 'w') as file:
        json.dump(properties_info, file)
        print("success write file")
