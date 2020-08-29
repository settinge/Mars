from splinter import Browser
from bs4 import BeautifulSoup 
import time
import pandas as pd
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome = webdriver.Chrome("C:\\Users\\samantha.ettinger\\chromedriver.exe", chrome_options=chrome_options)

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
        #featured image to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    img_url=img_soup.select_one('figure.lede a img').get("src")
    final_img_url=f'https://www.jpl.nasa.gov{img_url}'
    print(final_img_url)

        #mars weather
    url="https://twitter.com/marswxreport?lang=en"
        # Retrieve page with the requests module
    response = requests.get(url)
        # Create BeautifulSoup object; parse with 'lxml'
    html_text="""
    <span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">InSight sol 611 (2020-08-15) low -93.8ºC (-136.9ºF) high -15.9ºC (3.4ºF)
    winds from the WNW at 7.3 m/s (16.3 mph) gusting to 17.9 m/s (40.2 mph)
    pressure at 7.90 hPa</span>
    """

    html = BeautifulSoup(html_text, "lxml")

    twitter_results = html.find('span',{'class':'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})

    mars_we=twitter_results.string

  
        #Mars Facts
    url='https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Measurement','Measure']
    html_table = df.to_html(index=False)
        #mars hemispheres
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    links = browser.find_by_css("a.product-item h3")
    hem_urls=[]
    for i in range(len(links)):
        hemispheres={}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_element=browser.find_link_by_text("Sample").first
        hemispheres['url']=sample_element['href']
        hemispheres['title']=browser.find_by_css("h2.title").text
        hem_urls.append(hemispheres)
        browser.back()
    




    
        # Store data in a dictionary
    mars_data = {
        "news_title": title_text,
        "news_paragraph": spl[0],
        "featured_image_url": final_img_url,
        "mars_weather": mars_we,
        "mars_facts": html_table,
        "hemisphere_info":hem_urls


    }
   
        # Close the browser after scraping
    browser.quit()

    return mars_data

    # return mars_data
        # Return results
        # return costa_data
