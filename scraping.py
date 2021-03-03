#imports Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

#imports ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

#imports pandas
import pandas as pd

#sets the executable path and initializes the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

###TITLE AND BODY
#visits the mars nasa website
url = 'http://mars.nasa.gov/news/'
browser.visit(url)

#optional delay for loading the page
#searching for elements with specific combinations, ul tag w/ item_list attributes and li tag with slide attribute
browser.is_element_present_by_css('ul.item_list li.slide', wait_time = 1)

#gets the html content of the page
html = browser.html

#parses html page
news_soup = soup(html, 'html.parser')

#creates the first search
#grabs the first item that matches both arguments
slide_elem = news_soup.select_one('ul.item_list li.slide')

#extracts only the text title
news_title = slide_elem.find('div', class_= 'content_title').get_text()
news_title

#extracts only the article body summary
news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()
news_p

### FEATURED IMAGES
#visits the website
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

#find and click full image button
full_image_elem= browser.find_by_tag('button')[1]
full_image_elem.click()

#parses the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#extracting image
image_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
image_url_rel #only partial url

#gets base url to create absolute url 
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url_rel}'
img_url

### FACTS
#extracting the html table and convert it into a pandas dataframe
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace = True)

df.to_html()
#likewise the dataframe can also be converted back into html for uploading into a new web page

#quits session
browser.quit()


