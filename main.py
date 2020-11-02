import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

#input demanded search
seed_urls = {'data scientist':'https://pl.indeed.com/praca?q=data+scientist&lang=en',
             'data analyst': 'https://pl.indeed.com/praca?q=data+analyst&lang=en}'}
#crucial to stop looping over the next pages if the ID value of advertisement is not unique.
unique_identity_values = []
#We have to add '&start=10' after hyperlink to indicate the next webpage

def url_pages_creator(number_of_pages):
    '''This function creates new set of urls.
       Because each URL corresponds to certain maximum
       Level of applications, there need to be funciton
       That handles this issue.'''
    #      &start=20
    for i in range(1, number_of_pages+1):
        print(i*10)
        






                 
def build_dataset(seed_urls):
    '''creating job_offers list, that will 
    contain location and job title'''
    seed_urls = seed_urls
    global unique_identity_values 
    
# =============================================================================
#               ID, TITLE, Company Name, Location, Days_ago
# =============================================================================

    for url in seed_urls.keys():
        sauce = requests.get(seed_urls.get(url))
        soup = BeautifulSoup(sauce.content, 'html.parser')
        results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
        #creating unique_variables_list
        unique_id = []
        job_title = []
        company_name = []
        location = []
        days_ago = []
        enriched_id = []
        
        for div in results:
            unique_id.append(div.a['id'])
            job_title = div.find('a', {'data-tn-element':'jobTitle'}).text
            company_name.append(div.find('span', {'class':'company'}).text)
            location.append(div.find('span', {'class': 'location'}))
            days_ago.append(div.find('span', {'class': 'date'}))
            unique_identity_values.append(div.a['id'])
            enriched_id.append('&vjk=' + div.a['id'])

        
        #creating dataframe
        df = pd.DataFrame({'ID' : unique_id,
                           'title' : job_title,
                           'company_name' : company_name,
                           'locaiton' : location,
                           'days_ago' : days_ago,
                           'enriched_ID' : enriched_id})
                             
    return df


    



#text_id

# for ID in unique_identity_values:
#     text = ''.join(['&vjk=', ID])
#     print(text)
    


#saving
# with open('soup.txt', 'w') as f:
#     f.write(soup.text)