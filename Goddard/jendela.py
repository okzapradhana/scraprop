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


def scrap():
    url_string = "https://jendela360.com/search"
    # chromedriver path
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    
    timeout_wait = 20
    format_time = "%Y-%m-%d %H:%M:%S"

    # Home
    list_bulan = []
    list_unit_name = []
    list_room = []
    list_price = []
    list_price_label = []
    list_area = []
    list_tower = []
    list_floor = []
    list_time_taken = []

    #Page Detail
    list_facilities_unit = []
    list_facilities_apart = []
    list_conditions = []
    list_estimation_prices = []

    for each_page in range(5): #access 5 pages
        list_href = [] #reset every page

        print('Current page: ', (each_page+1), '\n')
        driver.get('https://jendela360.com/search?page='+str(each_page+1))

        try:
            present_element = EC.presence_of_element_located((By.CLASS_NAME, 'js-unit-tile'))
            WebDriverWait(driver, timeout_wait).until(present_element)
        except TimeoutException:
            print('Time out waiting page to Load')
        finally:
            print('Page successfully loaded!')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            results = driver.find_elements(By.CSS_SELECTOR, ".js-unit-tile")
            #print('Result', results)
            print(len(results))

            for each_unit in results:
                bayar_bulan = each_unit.find_element_by_class_name(
                    'monthly-label').text
                unit_name = each_unit.find_element_by_tag_name('h5').text
                info_room = each_unit.find_element_by_class_name(
                    'info-room').text.strip()
                price = each_unit.find_element_by_class_name('price').text
                price_label = each_unit.find_element_by_class_name(
                    'price-label').text
                link_href = each_unit.find_element(
                    By.CSS_SELECTOR, "a[href^='https://jendela360.com']").get_attribute("href")
                area = each_unit.find_element(
                    By.CSS_SELECTOR, "ul[class='info-facility'] > li:nth-child(1) > span").text
                tower = each_unit.find_element(
                    By.CSS_SELECTOR, "ul[class='info-facility'] > li:nth-child(2) > span").text
                floor = each_unit.find_element(
                    By.CSS_SELECTOR, "ul[class='info-facility'] > li:nth-child(3) > span").text
                curr_time = datetime.now(timezone('Asia/Jakarta'))
                time_taken = curr_time.strftime(format_time)

                #print('Unit name: ', unit_name)

                list_bulan.append(bayar_bulan)
                list_unit_name.append(unit_name)
                list_room.append(info_room)
                list_price.append(price)
                list_price_label.append(price_label)
                list_href.append(link_href)
                list_area.append(area)
                list_tower.append(tower)
                list_floor.append(floor)
                list_time_taken.append(time_taken)


            # driver.back()
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            for each_url in list_href:
                print('Current url: ', each_url, '\n')
                driver.get(each_url)
                try:
                    present_element = EC.presence_of_element_located((By.CLASS_NAME, 'container'))
                    WebDriverWait(driver, timeout_wait).until(present_element)
                except TimeoutException:
                    print('Time out waiting page to Load')
                finally:
                    unit_detail = driver.find_element(By.CSS_SELECTOR, "div[class='container']")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    #print('Unit detail', unit_detail)
                    
                    driver.implicitly_wait(5)
                    modal = driver.find_elements(By.CLASS_NAME, 'modal__panel')
                    if(len(modal) > 0):
                        print('Modal displayed!')
                        btn = driver.find_element(By.CLASS_NAME, 'helper__close__btn')
                        btn.click()
                    else:
                        print('Modal not displayed')
                    
                    facilities_detail = unit_detail.find_element(By.CLASS_NAME, "gridded--list")
                    #print('Facilities detail:', facilities_detail.text)

                    condition = unit_detail.find_element(By.CSS_SELECTOR, ".gridded--list li:nth-of-type(3)").text.strip()
                    #print('Condition: ', condition)

                    list_conditions.append(condition)

                    unit_facilities = unit_detail.find_elements(By.CSS_SELECTOR, "div[id='facility'] .facility-text")
                    list_facil_unit = [each_facil.text for each_facil in unit_facilities]

                    apart_facilities = unit_detail.find_elements(By.CSS_SELECTOR, "div[id='apartmentfacilities'] .facility-text")
                    list_facil_apart = [each_facil.text for each_facil in apart_facilities]

                    #print('Unit facil: ', list_facil_unit)
                    #print('Apart facil: ', list_facil_apart)

                    list_facilities_unit.append(list_facil_unit)
                    list_facilities_apart.append(list_facil_apart)

                    monthly_price = unit_detail.find_elements(By.CSS_SELECTOR, '#monthlyfees > p')
                    split_space_price = [ charge_text.text for charge_text in monthly_price  ]
                    split_colon_price = [ tuple(each_price.split(':')) for each_price in split_space_price ]
                    dict_price = dict((estimasi.strip(), price.strip()) for estimasi, price  in split_colon_price)
                    print('Dictionary Price Estimation', dict_price)

                    list_estimation_prices.append(dict_price)

                #Print List
            print('\nList\n')
            print('area', len(list_area))
            #print('bulan', list_bulan)
            #print('cond', list_conditions)
            print('estimation prices', len(list_estimation_prices))
            print('facil apart', len(list_facilities_apart))
            print('facil unit', len(list_facilities_unit))
            #print('floor', list_floor)
            #print('href', list_href)
            #print('price', list_price)
            #print('room', list_room)
            #print('time', list_time_taken)
            print('tower', len(list_tower))
            print('unit name', len(list_unit_name))

    df_home = pd.DataFrame({'datestamp': list_time_taken, 'nama_unit': list_unit_name, 'rentang_bayar': list_bulan,
                            'ruangan': list_room, 'harga': list_price, 'keterangan_harga': list_price_label,
                            'luas_bangunan': list_area, 'tower': list_tower, 'lantai': list_floor,
                            'condition': list_conditions, 'fasilitas_unit': list_facilities_unit,
                            'fasilitas_apartemen': list_facilities_apart, 'estimasi_harga': list_estimation_prices})

    df_home.to_csv('jendela360_page1_home.csv')

    #pagination_length = driver.find_element(By.CSS_SELECTOR, "div[id='js-pagination'] > a:nth-last-child(2)").text
    #print('Pagination', (pagination_length))
