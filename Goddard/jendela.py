import pandas as pd
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from pytz import timezone
import time


def scrap():
    # chromedriver path
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)

    timeout_wait = 20
    format_time = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    now_timestamp = datetime.timestamp(now)

    list_unit_name, list_bedroom, list_bathroom, \
    list_rent_price, list_area, list_tower, list_floor, \
    list_time_taken, list_facilities_unit, list_facilities_apart, \
    list_conditions, list_estimation_prices = ([] for i in range(12))

    start = time.time()
    curr_page = 0

    while True: #access 5 pages
        list_href = [] #reset every page
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
            results = driver.find_elements(By.CSS_SELECTOR, ".js-unit-tile")
            pagination = driver.find_element(By.CSS_SELECTOR, "div[id='js-pagination']  a:nth-last-child(2)")
            print('page', pagination.text)

            for each_unit in results:
                link_href = each_unit.find_element(
                    By.CSS_SELECTOR, "a[href^='https://jendela360.com']").get_attribute("href")
                list_href.append(link_href)

            for each_url in list_href:
                print('Current url: ', each_url, '\n')
                driver.get(each_url)
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
                    rent_times = unit_detail.find_elements(By.CSS_SELECTOR, ".price-card ul[class='price-btn-tabs'] >li")
                    rent_keys = ["full", "monthly"]
                    
                    dict_rent_time = {}

                    for each_rent_time in rent_times:
                        anchor_href = each_rent_time.find_element(By.CSS_SELECTOR, ".price-tab")
                        rent_month_text = each_rent_time.find_element(By.CSS_SELECTOR, ".price-tab > span").text
                        anchor_href.click()

                        rent_price = unit_detail.find_elements(By.CSS_SELECTOR, ".price-content .star-price")
                        year_month_price = [ price.text.strip() for price in rent_price if price.text != '' ]
                        split_slash_price = [ price.split('/')[0] for price in year_month_price ] #get price only
                        dict_rent_price = dict((key, price.strip()) for price, key in zip(split_slash_price, rent_keys))
                        dict_rent_months = {rent_month_text:dict_rent_price}
                        dict_rent_time.update(dict_rent_months)

                    list_unit_name.append(unit_name)
                    list_bedroom.append(bedroom)
                    list_bathroom.append(bathroom)
                    list_area.append(area)
                    list_floor.append(floor)
                    list_tower.append(tower)
                    list_rent_price.append(dict_rent_time)
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
            
            curr_page+=1
            if curr_page == int(pagination):
                break

    df_home = pd.DataFrame({'datestamp': list_time_taken, 'nama_unit': list_unit_name,
                            'kamar_tidur': list_bedroom, 'kamar_mandi': list_bathroom,
                            'harga': list_rent_price,
                            'luas_bangunan': list_area, 'tower': list_tower, 'lantai': list_floor,
                            'condition': list_conditions, 'fasilitas_unit': list_facilities_unit,
                            'fasilitas_apartemen': list_facilities_apart,
                            'estimasi_harga': list_estimation_prices})

    df_home.to_csv('../files/jendela_'+str(now_timestamp)+'_.csv')

    print('Running time: ', time.time() - start)