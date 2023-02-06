from bs4 import BeautifulSoup
import requests 
from csv import writer

base_url = 'https://www.thomasnet.com/'
optional_url = 'nsearch.html?cov=UT&heading=8843096&searchsource=suppliers&searchterm=building+materials&searchx=true&what=building+materials&which=prod'
url = base_url + optional_url

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
#get link URL, then parse link URL and extract data that way. 
lists = soup.find_all('div', class_="profile-card__data") #use underscore or it looks for python class.
counter = 0
with open('leads.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Company', 'Commodity', 'City', 'State', 'Phone', 'Website', 'Last Name']
    thewriter.writerow(header)
    for list in lists:
        counter+=1
        link = list.find('a').get("href")
        #print(link)
        sub_url = base_url + link
        sub_page = requests.get(sub_url)
        page_search = BeautifulSoup(sub_page.content, 'html.parser')
        company_h1 = page_search.find('h1', {'class':'copro-supplier-name'})
        company_name = company_h1.find('a').contents[0].replace(",", '')
        commodity_div = page_search.find('div', {'class':'prodserv_group'})
        commodity_name = commodity_div.find('h3').contents[0]
        location_div = page_search.find('span', {'class':'copro-address-line'})
        location_name = location_div.text.split()
        city_name = location_name[0].replace(",", '')
        state_name = location_name[1].replace(",", '')
        i = 0
        while(len(state_name) > 2):
            i+=1
            state_name = location_name[i].replace(",", '')
        contact_p = page_search.find('p', {'class':'phoneline'})
        phone_span = contact_p.findChildren("span" , recursive=False)
        phone_number = phone_span[1].text
        website_link = company_h1.find('a').get("href")
        last_name = company_name
        info = [company_name, commodity_name, city_name, state_name, phone_number, website_link, last_name]
        thewriter.writerow(info)
        #print(company_name, commodity_name, city_name, state_name, phone_number, website_link)
        print(counter)
