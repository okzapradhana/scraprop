import pandas as pd
import os
import time
import pandas_gbq
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from pytz import timezone
from celery import Celery

app = Celery('jendela',
            backend='amqp://',
            broker='pyamqp://guest@localhost//')

chrome_options = Options()
chrome_options.add_argument("--headless")

def scrap_link():
    # chromedriver path
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path, options=chrome_options)
    driver.set_window_size(1440, 900)

    timeout_wait = 20
    curr_page = 0
    list_urls = []
    max_page = 0
    
    #access pages
    while True:
        print('Current page: ', (curr_page+1), '\n')
        driver.get('https://jendela360.com/search?page='+str(curr_page+1))

        try:
            present_element = EC.presence_of_element_located((By.CLASS_NAME, 'js-unit-tile'))
            WebDriverWait(driver, timeout_wait).until(present_element)
        except TimeoutException:
            print('Time out waiting page to Load')
        finally:
            print('Page successfully loaded!')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            driver.implicitly_wait(5)
            
            #waits for modal appear
            modal = driver.find_elements(By.CLASS_NAME, 'modal__panel')
            if(len(modal) > 0):
                btn = driver.find_element(By.CLASS_NAME, 'helper__close__btn')
                btn.click()
            else:
                print('Modal not displayed')

            results = driver.find_elements(By.CSS_SELECTOR, ".js-unit-tile")

            #executes once
            if curr_page == 0:
                pagination = driver.find_element(By.CSS_SELECTOR, "div[id='js-pagination']  a:nth-last-child(2)")
                print('page', pagination.text)
                max_page = pagination.text

            # get urls of unit details page in current pagination
            for each_unit in results:
                link_href = each_unit.find_element(
                    By.CSS_SELECTOR, "a[href^='https://jendela360.com']").get_attribute("href")
                list_urls.append(link_href)

            #go to next page
            if curr_page == int(max_page):
                break
            curr_page+=1
    
    return list_urls

def scrap_each_page(urls):
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path, options=chrome_options)
    driver.set_window_size(1440, 900)

    start = time.time()
    timeout_wait = 20
    format_time = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    now_timestamp = datetime.timestamp(now)

    list_unit_names, list_bedrooms, list_bathrooms, \
    list_rent_prices, list_areas, list_towers, list_floors, \
    list_time_taken, list_facilities_unit, list_facilities_apart, \
    list_conditions, list_estimation_prices = ([] for i in range(12))

    #visit each page
    for url in urls:
        print('Current url: ', url, '\n')
        driver.get(url)
        try:
            present_element = EC.presence_of_element_located((By.CLASS_NAME, 'container'))
            WebDriverWait(driver, timeout_wait).until(present_element)
        except TimeoutException:
            print('Time out waiting page to Load')
        finally:
            curr_time = datetime.now(timezone('Asia/Jakarta'))
            time_taken = curr_time.strftime(format_time)

            list_time_taken.append(time_taken)

            unit_detail = driver.find_element(By.CSS_SELECTOR, "div[class='container']")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            
            driver.implicitly_wait(5)
            modal = driver.find_elements(By.CLASS_NAME, 'modal__panel')
            if(len(modal) > 0):
                btn = driver.find_element(By.CLASS_NAME, 'helper__close__btn')
                btn.click()
            else:
                print('Modal not displayed')

            unit_name = unit_detail.find_element(By.CSS_SELECTOR, "div[id='units'] > h1").text
            bedroom = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(1)").text.strip()
            bathroom = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(2)").text.strip()
            condition = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(3)").text.strip()
            area = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(4)").text.strip()
            floor = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(5)").text.strip()
            tower = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(6)").text.strip()
            rent_periods = unit_detail.find_elements(By.CSS_SELECTOR, ".price-card ul[class='price-btn-tabs'] >li")
            rent_keys = ["full", "monthly"]
            
            dict_rent_period = {}

            for rent_period in rent_periods:
                anchor_href = rent_period.find_element(By.CSS_SELECTOR, ".price-tab")
                rent_month_text = rent_period.find_element(By.CSS_SELECTOR, ".price-tab > span").text
                anchor_href.click()

                rent_price = unit_detail.find_elements(By.CSS_SELECTOR, ".price-content .star-price")
                year_month_price = [ price.text.strip() for price in rent_price if price.text != '' ]
                split_slash_price = [ price.split('/')[0] for price in year_month_price ] #get price only
                dict_rent_price = dict((key, price.strip()) for price, key in zip(split_slash_price, rent_keys))
                dict_rent_months = {rent_month_text:dict_rent_price}
                dict_rent_period.update(dict_rent_months)

            list_unit_names.append(unit_name)
            list_bedrooms.append(bedroom)
            list_bathrooms.append(bathroom)
            list_areas.append(area)
            list_floors.append(floor)
            list_towers.append(tower)
            list_rent_prices.append(dict_rent_period)
            list_conditions.append(condition)

            unit_facilities = unit_detail.find_elements(By.CSS_SELECTOR, "div[id='facility'] .facility-text")
            list_facil_unit = [each_facil.text for each_facil in unit_facilities]

            apart_facilities = unit_detail.find_elements(By.CSS_SELECTOR, "div[id='apartmentfacilities'] .facility-text")
            list_facil_apart = [each_facil.text for each_facil in apart_facilities]

            list_facilities_unit.append(list_facil_unit)
            list_facilities_apart.append(list_facil_apart)

            monthly_price = unit_detail.find_elements(By.CSS_SELECTOR, '#monthlyfees > p')
            split_space_price = [ charge_text.text for charge_text in monthly_price  ]
            split_colon_price = [ tuple(each_price.split(':')) for each_price in split_space_price ]
            dict_price = dict((estimasi.strip(), price.strip()) for estimasi, price  in split_colon_price)

            list_estimation_prices.append(dict_price)


            df_home = pd.DataFrame({'datestamp': list_time_taken, 'nama_unit': list_unit_names,
                            'kamar_tidur': list_bedrooms, 'kamar_mandi': list_bathrooms,
                            'harga': list_rent_prices,
                            'luas_bangunan': list_areas, 'tower': list_towers, 'lantai': list_floors,
                            'condition': list_conditions, 'fasilitas_unit': list_facilities_unit,
                            'fasilitas_apartemen': list_facilities_apart,
                            'estimasi_harga': list_estimation_prices})

        df_home.to_csv('../files/jendela_'+str(now_timestamp)+'_.csv')
        pandas_gbq.to_gbq(df_home, os.getenv("JENDELA_TABLE_NAME"),
                        os.getenv("PROJECT_ID"), if_exists="replace")

    print('Running time: ', time.time() - start)