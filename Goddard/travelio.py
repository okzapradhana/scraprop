import os
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrap():
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    timeout_wait = 30
    list_fields = []

    driver.get('https://www.travelio.com/search?searchType=daily&destinationCategory=City&destinationUrlName=jakarta&destination=Jakarta&checkIn=10-02-2020&checkOut=11-02-2020&bottomPrice=59764&upperPrice=6000000&destinationId=544a05f190e50d6a3d000001&hotelName=&areaId=&buildingId=&facilityId=&roomTypeId=&propTypeId=&unitType=&badge=&instant=&sortBy=&sortOrder=')
    try:
        present_element = EC.visibility_of_element_located((By.ID, 'hotel-list-box'))
        WebDriverWait(driver, timeout_wait).until(present_element)
    except TimeoutException:
        print('Time out waiting page to Load')
    finally:
        property_list = driver.find_elements(By.CSS_SELECTOR, "div[id='hotel-list-box'] div[class='property-box']")
        list_href = [each_property.find_element(By.CSS_SELECTOR, "a[href^='//www.travelio.com']").get_attribute("href") for each_property in property_list]

        for each_href in list_href:
            dict_field = {}
            driver.get(each_href)

            try:
                present_element = EC.presence_of_element_located((By.ID, 'page-body-wrapper'))
                WebDriverWait(driver, timeout_wait).until(present_element)
                print('Loading finished')
            except TimeoutException:
                print('Time out waiting price')
            finally:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                name = driver.find_element(By.CSS_SELECTOR, "div[id='hotel-name'] > h2").get_attribute('title')
                print('\nName', name, '\n')
                hotel_item = driver.find_elements(By.CSS_SELECTOR, "div[id='page-body-left'] > div:nth-child(6), div[id='page-body-left'] > div:nth-child(7), div[id='page-body-left'] > div:nth-child(8)")
                print(len(hotel_item))

                for item in hotel_item:
                    #print(item.text)
                    title = item.find_element(By.CLASS_NAME, "hotel-left-head-title").text
                    print(title)
                    key_fac = item.find_elements(By.CSS_SELECTOR, ".hotel-left-item-info-wrapper .hotel-left-item-info-head")
                    value_fac = item.find_elements(By.CSS_SELECTOR, ".hotel-left-item-info-wrapper .hotel-left-item-info-detail")
                    fac = dict((each_key.text, each_val.text) for each_key, each_val in zip(key_fac, value_fac))
                    print(fac)
                    if title.lower() == 'properti':
                        furnitures = item.find_elements(By.CLASS_NAME, "row")
                        print('Furnitures', len(furnitures))
                        temp = [f.text for f in furnitures]
                        print('temp test', temp)


                    '''for each_fur in furnitures:
                        key_fur = each_fur.find_element(By.CSS_SELECTOR, ".hotel-left-item-info-head").text
                        print('key fur', key_fur)
                        key_detail_fur = each_fur.find_elements(By.CSS_SELECTOR, ".row .margintop10")
                        text_detail_fur = [ f.text for f in key_detail_fur ]
                        print('Text', text_detail_fur)'''
