import os
import pandas as pd
import math
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from pytz import timezone

def scrap(links: []):
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    timeout_wait = 20
    now = datetime.now()
    now_timestamp = datetime.timestamp(now)

    apartments = []
    for link in links:
        driver.get(link)
        print("Current Apart Link: ", link)

        #wait for price list to be clickable while load the page
        try:
            clickable_element = EC.element_to_be_clickable((By.ID, '#monthly'))
            WebDriverWait(driver, timeout_wait).until(clickable_element)
            print('Loading finished')
        except TimeoutException:
            print('Time out waiting price')
        finally:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            price_tabs = driver.find_elements(By.CSS_SELECTOR, "ul.nav-tabs > li")
            len_price_tabs = len(price_tabs)
            apartments_dict = {}
            checklists_perabotan = []
            price_labels = []
            prices = []
            for tab in price_tabs:
                tab_element = tab.find_element(By.CSS_SELECTOR, "a")
                if '\n' in tab_element.text:
                    label = tab_element.text.split('\n')[1]
                else:
                    label = tab_element.text
                price_labels.append(label)
                print("Current tab: ", label)
                tab_element.click()
                timeout_tab = 8

                #wait for prices to be clickable after click the Tab
                try:
                    overlay_element_present = EC.presence_of_element_located((By.ID, 'controller-box-overlay'))
                    WebDriverWait(driver, timeout_tab).until_not(overlay_element_present)
                except:
                    print('Time out waiting price')
                finally:
                    price_value = driver.find_element(By.CSS_SELECTOR, 'span.price-value')
                    if price_value.text == '-':
                        print('Tidak ada harga!')
                        no_avail = driver.find_element(By.CSS_SELECTOR, 'div#no-available-room') 
                        text = no_avail.text
                        print('no avail element', no_avail)
                    else:
                        print('Ada harganya!')

                        #check dropdown a.k.a select options
                        if is_element_exist('CSS_SELECTOR', 'div.select-wrapper > select', driver):
                            print("Options nya ada")
                            options = driver.find_elements(By.CSS_SELECTOR, 'select.search-input > option')
                            for option in options:
                                if option.text == 'Bayar Penuh':
                                    option.click()
                                    try:
                                        overlay_element_present = EC.presence_of_element_located((By.ID, 'controller-box-overlay'))
                                        WebDriverWait(driver, timeout_tab).until_not(overlay_element_present)
                                    except:
                                        print('Time out waiting price')
                                    finally:
                                        print("Waiting success!")
                                    break
                        total_price_el = driver.find_element(By.CSS_SELECTOR, 'div.price-total-price') 
                        text = total_price_el.text
                    prices.append(text)
                    print("Prices: ", prices)

            print(price_labels)
            
            print("Price tabs length ", len_price_tabs)
            facilities = driver.find_elements(By.CLASS_NAME, "hotel-left-head-title")
            
            facilities_title = [ facility.text for facility in facilities 
                                if facility.text != '' 
                                and 'Galeri' not in facility.text 
                                and 'Informasi Sewa' not in facility.text ] #'' means not visible in UI.

            print("Facilities", facilities_title)
            detail_facilities = driver.find_elements(By.CLASS_NAME, "hotel-left-item-info-head")
            detail_facilities_title = [ dt.text for dt in detail_facilities if dt.text != '' ]
            print("Detail facilities", detail_facilities_title)
            
            name = driver.find_element(By.CSS_SELECTOR, "div[id='hotel-name'] > h2").get_attribute('title')
            print("Apart name", name)

            value_facilities = driver.find_elements(By.CLASS_NAME, "hotel-left-item-info-detail")
            value_facilities_text = [ val.text for val in value_facilities if val.text != '' ]
            print("Values", value_facilities_text)
            
            keys_perabotan = driver.find_elements(By.CSS_SELECTOR, "div.row > div.margintop10")
            print("Length kp", len(keys_perabotan))
            keys_perabotan_text = [ kp.text for kp in keys_perabotan ]
            print("perabotan key", keys_perabotan_text)
            if len(keys_perabotan) > 0:
                for idx, kp in enumerate(keys_perabotan):
                    print("Key text: ", kp.text)
                    class_attr_kp = kp.get_attribute("class")

                    #class_attr_kp => margintop10 col-xs-12
                    selector_each_kp = "div.{}:nth-child({}) + div.col-xs-12".format(class_attr_kp.split()[0], ((idx*2)+1))
                    print("SELECTOR ", selector_each_kp)
                    facilities_kp_el = driver.find_element(By.CSS_SELECTOR, selector_each_kp)
                    print("Attr el ", facilities_kp_el.get_attribute("class"))
                    furniture_items = facilities_kp_el.find_elements(By.CSS_SELECTOR, "div.furniture-item")
                    furniture_text = [item.text for item in furniture_items ]
                    print("Furniture Checklists text: ", furniture_text)
                    checklists_perabotan.append(furniture_text)

            building_facility_items = driver.find_elements(By.CSS_SELECTOR, "div.hotel-left-item-info > div.row > div.hotel-facility-item")
            items_text = [ bfi.text for bfi in building_facility_items ]
            print(len(items_text))
            print("items text", items_text)

            #detail fac & values
            facilities_dict = dict((fac, val) for fac, val in zip(detail_facilities_title, value_facilities_text))
            print("Dictionary for facilities\n", facilities_dict)

            #price
            prices_dict = dict((label, price) for label, price in zip(price_labels, prices))
            print("Dictionary for prices\n", prices_dict)

            apartments_dict.update(facilities_dict)
            apartments_dict.update(prices_dict)

            if len(keys_perabotan) == 0:
                perabotan_dict = {"Perabotan": []}
            else:
                perabotan_dict = dict((key, perabotan) for key, perabotan in zip(keys_perabotan_text, checklists_perabotan))
            apartments_dict.update(perabotan_dict)
            print("Dictionary for perabotan and its checklist\n", perabotan_dict)
            print("\nCurrent Aparts Dictionary\n", apartments_dict)

            apartments.append(apartments_dict)

    with open('apartments_{}.json'.format(now_timestamp), 'w') as file:
        json.dump(apartments, file)
        print("success write file")


def scrap_href():
    load_dotenv()
    executable_path = os.getenv('EXECUTABLE_PATH')
    driver = webdriver.Chrome(executable_path)
    curr_page = 1
    links = []
    
    driver.get('https://www.travelio.com/sewa-apartemen-jakarta/jakarta-pusat')
    item_per_page = driver.find_element(By.CSS_SELECTOR, "div#hotel-pagination > div > div#showing-hotel > span:nth-child(1)")
    max_item = driver.find_element(By.CSS_SELECTOR, "div#hotel-pagination > div > div#showing-hotel > span:nth-child(2)")
    item_per_page_text = item_per_page.text.split(" - ")[1]
    max_item_text = max_item.text
    pagination = math.ceil(int(max_item_text)/int(item_per_page_text))

    while True:
        print("Current page: ", curr_page)
        print("Pagination: ", pagination)

        property_list = driver.find_elements(By.CSS_SELECTOR, "div[id='hotel-list'] div[class='property-box']")
        links_per_page = [each_property.find_element(By.CSS_SELECTOR, "a[href^='//www.travelio.com']").get_attribute("href") for each_property in property_list]
        links.extend(links_per_page)
        curr_page+=1

        print("Links length: ", len(links), '\n')
        if curr_page == pagination:
            break
        driver.get('https://www.travelio.com/sewa-apartemen-jakarta/jakarta-pusat?page={}'.format(curr_page))

    return links
        
def is_element_exist(by, selector, driver):
    try:
        if by == 'CSS_SELECTOR':
            driver.find_element(By.CSS_SELECTOR, selector)
        elif by == 'XPATH':
            driver.find_element(By.XPATH, selector)
    except NoSuchElementException:
        return False
    return True
