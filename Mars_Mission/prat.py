from splinter import Browser
from bs4 import BeautifulSoup 
import time
import pandas as pd
import pymongo
import requests

def init_browser():

    executable_path = {'executable_path': r"C:\\Users\\samantha.ettinger\\chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser=init_browser()
   
#news url to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
   


    first_results = soup.find_all('div', class_='rollover_description_inner')
    paragraph=[]
    for result in first_results:
        title_text=result.text
        print(title_text)
    # if title_text not in paragraph:
    #     paragraph.append(title_text)
    # res = [sub.replace('\n', '') for sub in paragraph]
    # res=  [sub.replace('\"','')for sub in res]
    # print(res)
    
    second_results = soup.find_all('div', class_='content_title')
    title=[]
    for result in second_results:
        t_text=result.find('a').text
        if t_text not in title:
            title.append(t_text)
    spl = [sub.replace('\n', '') for sub in title]
    print(spl)
    mars_data = {
        "news_title": title_text,
        "news_paragraph": spl[0]
    }
    browser.quit()
scrape_info()