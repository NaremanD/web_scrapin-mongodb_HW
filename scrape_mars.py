# import Dependencies 
import time
from bs4 import BeautifulSoup 
import requests
from selenium import webdriver 
import pandas as pd
def init_driver():
    driver = webdriver.Firefox()
    return driver     
def scrape():
 #Scrapes various websites for information about Mars, and returns data in a dictionary
    data_mars = {}  
    driver = webdriver.Firefox()
    #Get the info from the NASA News Webpage
    nasa_url = "https://mars.nasa.gov/news/"
    driver = webdriver.Firefox()
    driver.get(nasa_url)
    html_nasa = driver.page_source
    # Scrape page into soup
    soup_nasa = BeautifulSoup(html_nasa, 'html.parser')
    # save the most latest News Title and Paragraph Text 
    #news_date = soup_nasa.find ('div', class_='list_date').text
    news_title = soup_nasa.find('div', class_='content_title').find('a').text
    news_p = soup_nasa.find('div',class_='article_teaser_body').text
    data_mars["News_Title"] = news_title
    data_mars["News_Pargraph"] = news_p
    
    # GEt the featured image of the JPL
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver = webdriver.Firefox()
    driver.get(image_url)
   #html_image = driver.page_source
    driver.find_element_by_partial_link_text("FULL IMAGE").click()
    time.sleep(5)
    html_image = driver.page_source 
    driver.find_element_by_partial_link_text("more info ").click()
    html_image = driver.page_source 
     # Parse HTML with Beautiful Soup
    jpl_soup = BeautifulSoup(html_image, 'html.parser')
    # Retrieve Featured Image url 
    featured_image_url  = jpl_soup.find("img", class_='main_image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}' 
    data_mars['featured_image_url'] = featured_image_url
     # Visit the Mars Weather twitter account and scrap the lates Mars weather tweet.
    weather_url = "https://twitter.com/marswxreport?lang=en"
    driver = webdriver.Firefox()
    driver.get(weather_url)
    # HTML Object 
    html_weather = driver.page_source
    # Scrape page into soup
    weather_soup = BeautifulSoup(html_weather, 'html.parser')
    mars_weather_tweet = weather_soup.find ("div", class_="js-tweet-text-container").text.strip()
    data_mars['weather_summary'] = mars_weather_tweet
    # visit space facts and scrap the mars facts table
    facts_url = 'http://space-facts.com/mars/'
    # Use Panda's 'read_html' to parse the url
    mars_facts = pd.read_html(facts_url)
    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]
    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']
    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)
    # Save html code to folder Assets
    mars_fact_html =mars_df.to_html()
    data_mars["fact_table"] = mars_fact_html
    # scrape images of Mars' hemispheres from the USGS site
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    driver = webdriver.Firefox()
    driver.get(hemispheres_url)
    # HTML Object 
    html_hemispheres = driver.page_source
    # Scrape page into soup
    hemispheres_soup = BeautifulSoup(html_hemispheres, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = hemispheres_soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        # Store link that leads to full image website
        partial_img_url = hemispheres_soup.find('a', class_='itemLink product-item')['href']
        # Visit the link that contains the full image website 
        driver.get(hemispheres_main_url + partial_img_url)
        # HTML Object of individual hemisphere information website 
        partial_img_html = driver.page_source
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        data_mars["hemisphere_imgs"] = hemisphere_image_urls
    return data_mars
