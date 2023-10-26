import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common import service, options

# Function to check if the document is ready
def is_document_ready(driver):
    return driver.execute_script("return document.readyState === 'complete';")

# Function to extract card data
def extract_card_data(page_source):
    card_data = []

    soup = BeautifulSoup(page_source, 'html.parser')
    cards = soup.find_all('div', class_='box search_result ng-scope')

    for card in cards:
        data = {
            'subject': '',
            'type': '',
            'course': '',
            'year': '',
            'student': '',
            'professor': '',
            'university': '',
            'moshaver':''
        }

        # Extract subject
        subject = card.find('span', class_='search_title')
        if subject:
            data['subject'] = subject.text.strip()

        # Extract type, course, and year
        details = card.find_all('div', class_='col-md-3 col-sm-5 col-xs-6')
        if len(details) >= 3:
            data['type'] = details[0].find('span', class_='ng-binding').text.strip()
            data['course'] = details[1].find('span', class_='ng-binding').text.strip()
            data['year'] = details[2].find('span', class_='ng-binding').text.strip()

        # Extract student and professor
        contributors = card.find_all('div', class_='col-md-12')
        for contributor in contributors:
            contribution_role = contributor.find('span', class_='contribution_role')
            if contribution_role:
                role = contribution_role.text.strip()
                name = contributor.find('a', class_='ng-binding')
                if name:
                    name = name.text.strip()
                    if role == 'پدیدآور:':
                        data['student'] = name
                    elif role == 'استاد راهنما:':
                        data['professor'] = name
                    elif role == 'استاد مشاور:':
                        data['moshaver'] = name


        # Extract university
        university = card.find('span', class_='ng-binding', style='color: #333;')
        if university:
            data['university'] = university.text.strip()

        card_data.append(data)

    return card_data

# Set up Selenium WebDriver
# Set up Selenium WebDriver
driver = webdriver.Chrome()
pg_number = 1
max_pg_number = None
result_count = 0
temp =[]
start_year = 1380

def estimated_results_count(driver):
    time.sleep(2)
    target_element_selector = (By.CSS_SELECTOR, 'label[for="results_total_count"]')
    while True:
            wait = WebDriverWait(driver,
                                 10)
            target_element = wait.until(EC.presence_of_element_located(target_element_selector))
            sibling = target_element.find_element(By.XPATH,
                                                  'following-sibling::div')
            if target_element and sibling:
                if sibling.text not in ["",'']:
                    break
                else:
                    raise ValueError
            else:
                continue
    return int(sibling.text)


''
def get_cards(driver,page_result):
    if page_result>100:
        if int(driver.current_url[-1])>1:
            page_result = page_result -100
        else:
            page_result = 100

    if page_result == 0:
        return []
    while True:
        try:
            card_data = extract_card_data(driver.page_source)
            if len(card_data) ==page_result:
                return card_data

        except:
            continue
url = f"https://ganj.irandoc.ac.ir/#/search?keywords=%D8%A8%DB%8C%D9%88%D8%A7%D9%86%D9%81%D9%88%D8%B1%D9%85%D8%A7%D8%AA%DB%8C%DA%A9&basicscope=1&sort_by=1&fulltext_status=1&results_per_page=4&year_from={start_year}&year_to={start_year}&page={pg_number}"
dupl = [0,0,0]
while start_year<=1403:
    if pg_number-1 ==0:
        pg_number=2
    url = f"https://ganj.irandoc.ac.ir/#/search?keywords=%D8%A8%DB%8C%D9%88%D8%A7%D9%86%D9%81%D9%88%D8%B1%D9%85%D8%A7%D8%AA%DB%8C%DA%A9&basicscope=1&sort_by=1&fulltext_status=1&results_per_page=4&year_from={start_year}&year_to={start_year}&page={pg_number-1}"


    print("data : ",len(temp),"now:",start_year)
    # Open the URL
    try:
        while True:
            driver.get(url)
            page_result = estimated_results_count(driver)

            cards = get_cards(driver,page_result)
            for card in cards:
                temp.append(card)
            print("start_year : ",start_year,"cards:",len(cards))
            if page_result > 100:
                dupl[2] = page_result
                dupl[0]=start_year
                dupl[1]+=len(cards)
                if dupl[1]==dupl[2]:
                    dupl = [0,0,0]
                    start_year+=1
                    pg_number =1
                    break
                pg_number +=1
            else:
                start_year+=1
            break
    except Exception as e:
        print(e)
        continue

# Close the WebDriver after the loop
driver.quit()

print(len(temp))
# List of dictionaries


# CSV file name
csv_file = 'data.csv'

# Field names (keys from the dictionaries)
fieldnames = temp[0].keys()

# Write the data to the CSV file
with open(csv_file,
          mode = 'w',
          newline = '',
          encoding = "utf-8") as file:
    writer = csv.DictWriter(file,
                            fieldnames = fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data rows
    writer.writerows(temp)

print(f'Data written to {csv_file}')