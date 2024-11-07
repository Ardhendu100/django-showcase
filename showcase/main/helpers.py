from bs4 import BeautifulSoup
import requests
from .models import Stocks
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_all_stock_urls():
    try:
        page = requests.get('https://stocks.zerodha.com/')
        soup = BeautifulSoup(page.content, features='html.parser')
        for ul in soup.find_all('div', class_= 'index-page'):
            for li in ul.findAll('li'):
                data = li.find('a')
                Stocks.objects.get_or_create(
                    stock_name=data.text,
                    stock_url=data['href']
                )
        
    except Exception as e:
        print(e)


# def get_stock_price():
#     try:
#         page = requests.get('https://stocks.zerodha.com/stocks/abb-india-ABB')
#         soup = BeautifulSoup(page.content, features='html.parser')
#         data = soup.findAll(True, {'class' : ['hlcr']})
#         print(data)
#     except Exception as e:
#         print(e)

def get_stock_price():
    try:
        # Set up Selenium with headless mode (optional)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        service = Service("/usr/local/bin/chromedriver")  # Update with your path to chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Open the webpage
        driver.get('https://stocks.zerodha.com/stocks/abb-india-ABB')
        
        # Wait for content to load
        time.sleep(5)  # Adjust sleep time if needed for page load

        # Locate elements with the 'value' class
        prices = driver.find_elements(By.CLASS_NAME, "value")
        for price in prices:
            print(price.text)

        # Close the browser
        driver.quit()
    except Exception as e:
        print(e)
    