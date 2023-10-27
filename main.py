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
def extract_card_data(driver:webdriver.Chrome):
    card_data = []

    # cards element class box search_result ng-scope and is a div


    cards = driver.find_elements(By.CLASS_NAME,"box.search_result.ng-scope")


    # cards = driver.find_elements(By.CLASS_NAME,"box search_result ng-scope")
    for card in cards:
        try:
            data = {
                'subject': 'N/A',
                'type': 'N/A',
                'course': 'N/A',
                'category':'N/A',
                'year': 'N/A',
                'students': [],
                'professors': [],
                'university': 'N/A',
                'moshavers': [],
                }
            #card xpath         /html/body/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]
            # first div row     /html/body/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]
            # first_div is first div with class row inside the card
            data['subject']=card.find_element(By.CLASS_NAME,"search_title.ng-binding").text


            first_div = card.find_element(By.XPATH,".//div[@class='row']")
            column_div = first_div.find_element(By.XPATH,".//div[@class='col-md-10 col-sm-10']")
            row_divs = column_div.find_elements(By.XPATH,
                                                ".//div[contains(@class, 'row')]")
            type_row = row_divs[0]
            category_row = row_divs[1]
            contributers_row=row_divs[2]
            university_row = row_divs[3]
            inside_type = type_row.find_elements(By.XPATH,".//div")
            for ins in inside_type:
                if 'col-sm-5' in ins.get_attribute("class").split():
                    data['type'] = ins.text
                    # if ins has col-sm-4 class
                elif 'col-sm-4' in ins.get_attribute("class").split():
                    data['course']=ins.text
                elif 'col-sm-3' in ins.get_attribute("class").split():
                        data['year']=ins.text
            inside_category = category_row.find_elements(By.XPATH,".//div")
            if len(inside_category)>0:
                spans = inside_category[0].find_elements(By.TAG_NAME,"span")
                if len(spans)>0:
                    data['category']=spans[-1].text

            inside_contributers = contributers_row.find_elements(By.XPATH,".//div[@class='col-md-12']")
            if len(inside_contributers)>0:
                spans = inside_contributers[0].find_elements(By.XPATH,".//span[@ng-repeat='contribution in article.contributions']")
                if len(spans)>0:
                    for span in spans:
                        role = span.find_element(By.CLASS_NAME,"contribution_role.ng-binding").text
                        name = span.find_element(By.TAG_NAME,"a").text
                        if "پدید" in role:
                            data['students'].append(name)
                        elif "راهنما" in role:
                            data['professors'].append(name)
                        elif 'مشاور' in role:
                            data['moshavers'].append(name)
            inside_university = university_row.find_elements(By.XPATH,".//div")
            if len(inside_university)>0:
                data['university'] = inside_university[0].text
            card_data.append(data)
        except Exception as e:
            print(e)
            input("cont error")
    return card_data

# Set up Selenium WebDriver
# Set up Selenium WebDriver
driver = webdriver.Chrome()
pg_number = 1
max_pg_number = None
result_count = 0
temp =[]
start_year = 1382

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
            card_data = extract_card_data(driver)
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
expanded_temp = []

# Create a function to get the maximum number of items in any list
def max_items_in_lists(*lists):
    return max(len(lst) for lst in lists)

# Determine the maximum number of columns needed
max_students = max_professors = max_moshavers = 0

for data in temp:
    new_std = []
    for std in data['students']:
        if std not in new_std:
            new_std.append(std)
    data['students'] = new_std

    new_prof = []
    for prof in data['professors']:
        if prof not in new_prof:
            new_prof.append(prof)
    data['professors'] = new_prof

    new_mosh = []
    for mosh in data['moshavers']:
        if mosh not in new_mosh:
            new_mosh.append(mosh)
    data['moshavers'] = new_mosh
    max_students = max(max_students,
                       len(data['students']))
    max_professors = max(max_professors,
                         len(data['professors']))
    max_moshavers = max(max_moshavers,
                        len(data['moshavers']))

# Create field names for the CSV based on the maximum number of items
fieldnames = ['subject', 'type', 'course', 'category', 'year', 'university'] + [f'student_{i + 1}' for i in range(max_students)] + [f'professor_{i + 1}' for i in range(max_professors)] + [f'moshaver_{i + 1}' for i in range(max_moshavers)]

# Populate the expanded_temp list with the data
for data in temp:
    new_data = {key: data.get(key,
                              'N/A') for key in fieldnames}
    new_data['subject'] = data['subject']
    new_data['type'] = data['type']
    new_data['course'] = data['course']
    new_data['category'] = data['category']
    new_data['year'] = data['year']
    new_data['university'] = data['university']

    students = data.get('students',
                        [])
    professors = data.get('professors',
                          [])
    moshavers = data.get('moshavers',
                         [])

    for i, student in enumerate(students):
        new_data[f'student_{i + 1}'] = student

    for i, professor in enumerate(professors):
        new_data[f'professor_{i + 1}'] = professor

    for i, moshaver in enumerate(moshavers):
        new_data[f'moshaver_{i + 1}'] = moshaver

    expanded_temp.append(new_data)

# Open the CSV file for writing
with open(csv_file,
          mode = 'w',
          newline = '',
          encoding = 'utf-8') as file:
    writer = csv.DictWriter(file,
                            fieldnames = fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data rows
    writer.writerows(expanded_temp)

print(f'Data written to {csv_file}')