import requests
from .models import Stocks
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime
import concurrent.futures


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


def fetch_stock_data(stock):
    service = Service("/usr/bin/chromedriver")  # Ensure this path is correct for chromedriver
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"  # Path to your Chromium browser
    
    # Enable headless mode
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Optional, helps with stability in headless mode
    options.add_argument("--no-sandbox")

    # Start the WebDriver with the service and options
    driver = webdriver.Chrome(service=service, options=options)
    url = "https://stocks.zerodha.com" + stock.stock_url
    print(url)
    driver.get(url)
    
    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hlcr"))
        )
        time.sleep(2)  # Additional wait for content stability

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        high_low_returns = soup.find("div", {"class": "hlcr"})
        
        if high_low_returns:
            high_price = high_low_returns.find("div", text="High").find_next("div", class_="value").text.strip()
            low_price = high_low_returns.find("div", text="Low").find_next("div", class_="value").text.strip()
            returns = high_low_returns.find("div", text="Returns").find_next("div", class_="value").text.strip()

            # Update the stock object
            stock.high_price = high_price
            stock.low_price = low_price
            stock.returns = returns
            stock.last_fetched_on = datetime.now()
            stock.save()

        else:
            print(f"{stock.stock_name}: Data not found.")
        
    except Exception as e:
        print(f"Error for {stock.stock_name}: {e}")
    
    finally:
        driver.quit()
    
    
def get_stock_price():
    stock_list = Stocks.objects.all()
    
    # Use ThreadPoolExecutor for parallel scraping
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Run the fetch_stock_data function concurrently for each stock
        executor.map(fetch_stock_data, stock_list)

    print("Stock price update completed.")
    
    
        
    