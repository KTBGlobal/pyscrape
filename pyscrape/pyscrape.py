from bs4 import BeautifulSoup
import requests 

base_url = 'https://www.thomasnet.com/'
optional_url = 'nsearch.html?cov=NA&heading=8843096&typed_term=building+materials&searchterm=building+materials&what=Building+Materials&WTZO=Find+Suppliers&searchsource=suppliers'
url = base_url + optional_url

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
#get link URL, then parse link URL and extract data that way. 
lists = soup.find_all('div', class_="profile-card__data") #use underscore or it looks for python class. 

for list in lists:
    company_name = list.find('h2', class_="profile-card__title")
    info = [company_name]
    print(info)

