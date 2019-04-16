# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 15:54:06 2019

@author: Nathan
"""

import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import re
import matplotlib.pyplot as plt
import pickle

url = "https://www.nytimes.com/section/corrections"

# download driver from https://github.com/mozilla/geckodriver/releases/
# unzip and place in working directory of python program
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(300)

# Firefox opens, click show more button

html_source = driver.page_source
driver.quit()

soup = BeautifulSoup(html_source, 'html.parser')
#print(soup.prettify())

links = []
for link in BeautifulSoup(html_source, parse_only=SoupStrainer('a')):
    if link.has_attr('href') and link['href'][0] == '/' and len(link['href']) > 1:
        links.append(link['href'])
 
del links[0:4]

# save to file
#with open('links', 'wb') as fp:
 #   pickle.dump(links, fp)
    
# get list from file
with open ('links', 'rb') as fp:
    links = pickle.load(fp)

###############################################################################
# Get comments from given article url

article_list = []

j = 0
for curr_url in links:
    #if (j > 100):
    #    break
    print(j)
    # NYTimes Community API url
    URL = "http://www.nytimes.com/svc/community/V3/requestHandler?"
    # set params
    api_key = 'R1b6O4q3brTgJcZkZ4NeCAk3qkw8sUjJ'
    cmd = "GetCommentsAll"
  
    #curr_url = 'https://www.nytimes.com/2019/03/28/science/frogs-fungus-bd.html'
    curr_url = 'https://www.nytimes.com' + curr_url
    
    # get readable name from url
    url_name = re.split('/',curr_url)
    url_name = re.split('\.', url_name[len(url_name)-1])[0]
    
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'api-key': api_key, 'cmd':cmd, 'url':curr_url} 
      
    # sending get request and saving the response as response object 
    response = requests.get(url = URL, params = PARAMS) 
      
    # extracting data in json format 
    data = response.json() 
    del response
    
    ###########################################################################
    # Get keywords from urls
    
    URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    # set params
    api_key = 'R1b6O4q3brTgJcZkZ4NeCAk3qkw8sUjJ'
    fq = 'web_url:("' + curr_url + '")'
    page = 0
    
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'api-key': api_key, 'fq':fq, 'page':page} 
    
    # sleep 6 sec since api request limit is 10 per min
    time.sleep(6)
    
    # sending get request and saving the response as response object 
    kw_response = requests.get(url = URL, params = PARAMS) 
      
    # extracting data in json format 
    kw_data = kw_response.json() 
    del kw_response
    
    keywords =[]
    i=0
    for kw in kw_data['response']['docs'][0]['keywords']:
        if i<5:
            keywords.append(kw['value'])
        i += 1
    ###########################################################################

    if data['results']['totalCommentsFound'] > 0:
        comments = []
        for com in data['results']['comments']:
            comments.append(com['commentBody'])
            if com['replyCount'] > 0:
                for rep in com['replies'] :
                    comments.append(com['commentBody'])
        
        article_list.append({'url_name':url_name, 'url':curr_url, 'total_comments':data['results']['totalCommentsFound'], 'comments':comments, 'keywords':keywords})
    else:
        article_list.append({'url_name':url_name, 'url':curr_url, 'total_comments':data['results']['totalCommentsFound'], 'keywords':keywords})
        
    j += 1
    
# save to file
#with open('article_list', 'wb') as fp:
#    pickle.dump(article_list, fp)
    
# get list from file
with open ('article_list', 'rb') as fp:
    article_list = pickle.load(fp)
    
###############################################################################    

article_keywords = []
for a in article_list:
    for k in a['keywords']:
        article_keywords.append(k)

from pandas import Series
ak = Series(article_keywords)

ak_counts = ak.value_counts()

ak_counts[0:10].plot(kind='bar')
plt.title('Corrected Article Keywords')
plt.ylabel('Keyword Frequency')
plt.xlabel('Keyword')
plt.show()
###############################################################################

URL = "https://api.nytimes.com/svc/archive/v1/2019/3.json?"
    # set params
api_key = 'R1b6O4q3brTgJcZkZ4NeCAk3qkw8sUjJ'

PARAMS = {'api-key': api_key} 
      
# sending get request and saving the response as response object 
response = requests.get(url = URL, params = PARAMS) 
data = response.json() 

keywords_orig =[]
j=0
for a in data['response']['docs']:
    print (j)
    if j > len(article_list):
        break
    
    curr_url = a['web_url']
    
    URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    # set params
    api_key = 'R1b6O4q3brTgJcZkZ4NeCAk3qkw8sUjJ'
    fq = 'web_url:("' + curr_url + '")'
    page = 0
    
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'api-key': api_key, 'fq':fq, 'page':page} 
    
    # sleep 6 sec since api request limit is 10 per min
    time.sleep(6)
    
    # sending get request and saving the response as response object 
    kw_response = requests.get(url = URL, params = PARAMS) 
      
    # extracting data in json format 
    kw_data = kw_response.json() 
    del kw_response
    
    i=0
    for kw in kw_data['response']['docs'][0]['keywords']:
        if i<5:
            keywords_orig.append(kw['value'])
        i += 1
    j += 1
    
# save to file
#with open('keywords_orig', 'wb') as fp:
#    pickle.dump(keywords_orig, fp)
    
# get list from file
with open ('keywords_orig', 'rb') as fp:
    keywords_orig = pickle.load(fp)

ako = Series(keywords_orig)

ako_counts = ako.value_counts()

ako_counts[0:10].plot(kind='bar')
plt.title('General Article Keywords')
plt.ylabel('Keyword Frequency')
plt.xlabel('Keyword')
plt.show()