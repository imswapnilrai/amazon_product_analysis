#scrapping home page

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import os

if not os.path.exists('data'):
    os.makedirs('data')
    
driver = webdriver.Chrome()
file=0
for i in range(1,20):
    driver.get(f"https://www.amazon.in/s?k=laptop&page={i}&crid=B54RMYARI3NR&qid=1723352243&sprefix=laptop%2Caps%2C228&ref=sr_pg_{i}")

    elem=driver.find_elements(By.CLASS_NAME,"puisg-row")
    print(f"{len(elem)} items found")
    for j in elem:
        d=j.get_attribute("outerHTML")
        with open(f'data/product{file}.html',"w",encoding="utf-8") as f:
            f.write(d)
            file+=1
    #time.sleep(3)
driver.close()

#creating intial csv file using HTML parser (data.csv)
from bs4 import BeautifulSoup
import os

d={'title': [],'price':[],'link':[],'discount':[], 'delivery':[]}
urls=[]


for file in os.listdir("data"):
    try:
        with open(f"data/{file}") as f:
            html_doc=f.read()
            soup=BeautifulSoup(html_doc, 'html.parser')

        t=soup.find("h2")
        title=t.get_text()
        
        l=t.find('a')
        link="https://www.amazon.in/"+l['href']
        urls.append(link)
        
        # p=soup.find("span", attrs={"class":'a-price-whole'})
        # price=p.get_text()
        
        # dis=soup.find("span", attrs={"class":'a-truncate-full a-offscreen'})
        # discount=dis.get_text()
        
        # deli=soup.find("span", attrs={"class":'a-color-base a-text-bold'})
        # delivery=deli.get_text()

        # d['title'].append(title)
        # d['price'].append(price)
        # d['link'].append(link)
        # d['discount'].append(discount)
        # d['delivery'].append(delivery)
        
    except Exception as e:
        print(e)
        
import pandas as pd
df=pd.DataFrame(data=d)
df.to_csv('data.csv')



# extracting mobile html data

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import os

if not os.path.exists('laptop data'):
    os.makedirs('laptop data')
    
driver = webdriver.Chrome()
file=1
for i in urls:
    driver.get(i)
    
    elem = driver.find_elements(By.CLASS_NAME, "centerColAlign")

    print(f"{len(elem)} items found")
    for j in elem:
        d=j.get_attribute("outerHTML")
        with open(f'laptop data/laptop_{file}.html',"w",encoding="utf-8") as f:
            f.write(d)
            file+=1
driver.close()


#creating mobile csv

from bs4 import BeautifulSoup
import os

# Initialize the dictionary to store extracted data
d = {
    'Brand': [], 'Model Name': [], 'Screen Size': [], 'Colour': [], 'CPU Model': [], 
    'RAM Memory Installed Size': [], 'Operating System': [], 'Special Feature': [], 
    'Graphics Card Description': [], 'CPU Speed': [], 'HDD':[], 'Price':[]
}

# Process each HTML file in the "laptop data" directory
for file in os.listdir("laptop data"):
    try:
        with open(f"laptop data/{file}", encoding='utf-8',errors='ignore') as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')

        # Extract each feature using BeautifulSoup
        def extract_feature(class_name, feature_name):
            tag = soup.find("tr", class_=class_name)
            if tag:
                return tag.find("td", class_="a-span9").get_text(strip=True)
            return None

        d['Brand'].append(extract_feature('po-brand', 'Brand'))
        d['Model Name'].append(extract_feature('po-model_name', 'Model Name'))
        d['Screen Size'].append(extract_feature('po-display.size', 'Screen Size'))
        d['Colour'].append(extract_feature('po-color', 'Colour'))
        d['CPU Model'].append(extract_feature('po-cpu_model.family', 'CPU Model'))
        d['RAM Memory Installed Size'].append(extract_feature('po-ram_memory.installed_size', 'RAM Memory Installed Size'))
        d['Operating System'].append(extract_feature('po-operating_system', 'Operating System'))
        d['Special Feature'].append(extract_feature('po-special_feature', 'Special Feature'))
        d['Graphics Card Description'].append(extract_feature('po-graphics_description', 'Graphics Card Description'))
        d['CPU Speed'].append(extract_feature('po-cpu_model.speed', 'CPU Speed'))
        d['HDD'].append(extract_feature('po-hard_disk.size','HDD'))
        
        price_tag = soup.find("span", class_="a-price-whole")
        
        if price_tag:
            price = price_tag.get_text(strip=True)
            d['Price'].append(price)
        else:
            d['Price'].append(None)

        print(file)

    except Exception as e:
        print(e)

        
import pandas as pd
df=pd.DataFrame(data=d)
df.to_csv('mobile.csv')