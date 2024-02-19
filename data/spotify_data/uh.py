import pandas as pd
import requests 

from bs4 import BeautifulSoup
from datetime import datetime, timedelta



# Initialize empty lists to store data



# Starting date
start_year = 2021

years_to_go_back = 36

'''
for i in range(years_to_go_back):
    # calculating the year of the page
    current_year = start_year - i

    # Constructing the URL
    url = f'https://www.theamas.com/winners-database/?winnerKeyword=&winnerYear={start_year}'

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id = 'resultsTable')

    print(results)

    break
'''
'''
url = f'https://www.imdb.com/event/ev0003172/2022/1/'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

award_categories = soup.find_all('div', class_='event-widgets__award-category')

print(award_categories)'''

from selenium import webdriver
from bs4 import BeautifulSoup

# Set up the Chrome driver
driver = webdriver.Chrome()

# Load the page
url = 'https://www.imdb.com/event/ev0003172/2022/1/'
driver.get(url)

# Get the page source after it has been modified by JavaScript
page_source = driver.page_source

# Close the driver
driver.quit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all award categories within the nominees section
award_categories = soup.find_all('div', class_='event-widgets__award-category')

for category in award_categories:
    # Extract the award category name
    category_name = category.find('div', class_='event-widgets__award-category-name').text.strip()
    
    nominations = category.find_all('div', )
