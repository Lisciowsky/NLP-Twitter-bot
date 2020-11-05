import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import selenium

#input demanded search
seed_urls = {'data scientist':'https://pl.indeed.com/praca?q=data+scientist&lang=en'}
#crucial to stop looping over the next pages if the ID value of advertisement is not unique.
unique_identity_values = []
#We have to add '&start=10' after hyperlink to indicate the next webpage


  
    
def build_dataset(seed_urls):
    '''creating job_offers list, that will 
    contain location and job title'''
    seed_urls = seed_urls
    global unique_identity_values 
    
# =============================================================================
#               ID, TITLE, Company Name, Location, Days_ago
# =============================================================================

    for pos in seed_urls.keys():
        sauce = requests.get(seed_urls.get(pos))
        soup = BeautifulSoup(sauce.content, 'html.parser')
        results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
        #creating unique_variables_list
        unique_id = []
        job_title = []
        company_name = []
        location = []
        days_ago = []
        enriched_id = []
        url = []
        
        for div in results:
            unique_id.append(div.a['id'])
            job_title.append(div.find('a', {'data-tn-element':'jobTitle'}).text[1:])
            #1) problem to solve, /n at the beginning of the company name in some cases
            company_name.append(div.find('span', {'class':'company'}).text[1:].strip())
            location.append(div.find('span', {'class': 'location'}).text)
            days_ago.append(div.find('span', {'class': 'date'}))
            unique_identity_values.append(div.a['id'])
            enriched_id.append('&vjk=' + div.a['id'])

        
        #creating dataframe
        df = pd.DataFrame({'ID' : unique_id,
                           'title' : job_title,
                           'company_name' : company_name,
                           'location' : location,
                           'days_ago' : days_ago,
                           'enriched_ID' : enriched_id})
                             
    return df





def url_pages_creator(number_of_pages):
    '''This function creates new set of urls.
       Because each URL corresponds to certain maximum
       Level of applications, there need to be funciton
       That handles this issue.'''
    #      &start=20
    pages = []
    for i in range(1, number_of_pages+1):
        pages.append(i*10)

    return pages
    
def next_pages():
    #job describtions
    df = build_dataset(seed_urls)
    triger = list(seed_urls)[0]
    webseite = seed_urls.get(triger)
    enriched_id = df['enriched_ID']
    ready = []
    
    for ID in enriched_id:
        ready.append(webseite + ID)
        
    return ready



# sauce = requests.get('https://pl.indeed.com/praca?q=data%20scientist&lang=en&vjk=cb485c792ae34bc6')
# soup = BeautifulSoup(sauce.content, 'html.parser')

#SELENIUM SELENIUM SELENIUM SELENIUM SELENIUM SELENIUM SELENIUM SELENIUM 


# for x in soup.findall('div', {'id' :'vjs-container'}):
#     print(x)
#     for y in x.find('div', {'id': 'vjs-desc'}):
#         print(y.text)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import numpy as np
import pandas as pd


url = 'https://pl.indeed.com/praca?q=data+scientist&lang=en'


def reading_job_profiles(number, url):
    '''Using Selenium to extract job describtions with job titles'''
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    #driver
    driver = webdriver.Firefox(firefox_options=(options),executable_path = '/home/kuba/python/mozilla/geckodriver') 
    title = []
    describtion = []
    df = pd.DataFrame(columns = ['title','job_describtion'])
    

    for link in links_creator(number, url):
        driver.get(link)
        elements = driver.find_elements_by_class_name('title')   
        time.sleep(np.random.randint(1,4))
        try:
        #waiting for Cookies / AD
            y = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
            y.click()
        except Exception:
            pass
        
        try:
            x = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'popover-x')))
            x.click()
 
        except Exception:
            pass

            for element in elements:
                print(element.text)
                element.click()
                element.click()
                title.append(element.text)
                for x in driver.find_elements_by_id('vjs-desc'):
                    time.sleep(np.random.randint(3,12))
                    describtion.append(x.text.splitlines())
                    
    return title, describtion



def url_pages_creator(number_of_pages):
   '''This function creates new set of urls.
      Because each URL corresponds to certain maximum
      Level of applications, there need to be funciton
      That handles this issue.'''
   #      &start=20
   pages = []
   for i in range(1, number_of_pages+1):
       pages.append(i*10)

   return pages

def links_creator(number ,url):
    '''creating links to feed driver next page'''
    links = []
    links.append(url)
    for num in (url_pages_creator(number)):
        links.append(url + '&start=' + str(num))
        
    return links



'''

options = Options()
# options.add_argument("--headless")
# options.add_argument("--start-maximized")
# options.add_argument("--disable-notifications")
# options.add_argument("--incognito")
#driver    
driver = webdriver.Firefox(firefox_options=(options),executable_path = '/home/kuba/python/mozilla/geckodriver') 

for link in links_creator(3, url):
    driver.get(link)
    try:
        z = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'icl-Icon icl-Icon--sm')))
        z.click()
    except Exception:
        pass

'''

    
    
    
    
    
    

#.splitlines()
    
    
# x = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
# x.click


# with open('soup.txt', 'w') as f:
#     f.write(soup.text)
    
#text_id

# for ID in unique_identity_values:
#     text = ''.join(['&vjk=', ID])
#     print(text)
    

#saving
# with open('soup.txt', 'w') as f:
#     f.write(soup.text)
