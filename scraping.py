#imports Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

#imports ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

#imports other dependencies
import pandas as pd
import datetime as dt

def scrape_all():
    #sets the executable path and initializes the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    #sets news_title and news_p variables into the mars_news function (returns 2 variables)
    news_title, news_p = mars_news(browser)

    #runs all scraping function and returns in a library
    data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
    #defined browser to call up browser variable defined outside the function

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

    #adds try/except for error handling
    try:
        #creates the first search
        #grabs the first item that matches both arguments
        slide_elem = news_soup.select_one('ul.item li.slide')
        
        #extracts the text title using the parent element
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        #extracts the article body summary using the parent element
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p



def featured_image(browser):
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
    
    #adds in the error handling
    try:
        #extracts image/partial url
        image_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')
        
    except AttributeError:
        return None

    #gets base url to create absolute url 
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url_rel}'

    return img_url


def mars_facts():
### FACTS

    #adds the error handling
    try:
        #extracting the html table and convert it into a pandas dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    #sets the columns and assigns the index for the dataframe
    df.columns = ['description', 'value']
    df.set_index('description', inplace = True)

    return df.to_html(classes = 'table table-striped')
    #likewise the dataframe can also be converted back into html for uploading into a new web page

if __name__ == '__main__':
    #if running as a script, print scraped data
    print(scrape_all())