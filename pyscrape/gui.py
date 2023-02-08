#Import the required Libraries
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests 
from csv import writer
import threading

#Create an instance of tkinter frame
win = Tk()
#Set the geometry of tkinter frame
win.geometry("900x500")
#app name
win.title("THOMASNET SCRAPER")
win.configure(bg="grey")
### BUILD IN LOOP PAUSE. 
#Define a function to show a message
base_url = 'https://www.thomasnet.com/'

#store last URL
last_url = ''
next_page_url = ''
page_count = 1
def myclick():
    global next_page_url
    global page_count
    if(len(next_page_url)) >= 1:
       url = next_page_url
    else:
        url = entry.get()
    
    
    last_url = url
    message= "SCRAPED: "+ url
    label= Label(frame, text= message, font= ('Times New Roman', 8)).grid(column=0, row=15, padx=10, pady=25)
    entry.delete(0, 'end')
    #Loop page urls needs to be added, up to 10 pages of 25 entries***
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #get link URL, then parse link URL and extract data that way. 
    try:
        lists = soup.find_all('div', class_="profile-card__data") #use underscore or it looks for python class.
    except:
        print('Error getting lists')
    counter = 0
    
    next_page_url = soup.find('li', {'class':'page-item'}).find('a').get("href")
    with open('leads.csv', 'a', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        header = ['Company', 'Commodity', 'City', 'State', 'Phone', 'Website', 'Last Name', 'Lead Type']
        thewriter.writerow(header)
        for list in lists:
            try:
                counter+=1
                link = list.find('a').get("href")
                #print(link)
                sub_url = base_url + link
                sub_page = requests.get(sub_url)
                page_search = BeautifulSoup(sub_page.content, 'html.parser')
                company_h1 = page_search.find('h1', {'class':'copro-supplier-name'})
                #Fixed company name bug. 
                try:
                    company_name = company_h1.find('a').contents[0].replace(",", '')
                except:
                    company_name = company_h1.text
                commodity_div = page_search.find('div', {'class':'prodserv_group'})
                commodity_name = commodity_div.find('h3').contents[0]
                location_div = page_search.find('span', {'class':'copro-address-line'})
                location_name = location_div.text.split()
                city_name = location_name[0].replace(",", '')
                try:
                    state_name = location_name[1].replace(",", '')
                except:
                    state_name = ''
                i = 0
                while(len(state_name) > 2):
                    i+=1
                    state_name = location_name[i].replace(",", '')
                contact_p = page_search.find('p', {'class':'phoneline'})
                #*BUILD TRY EXCEPT TO FIND PH IF NO WEBSITE. 
                phone_span = contact_p.findChildren("span" , recursive=False) 
                try:
                    phone_number = phone_span[1].text
                except:
                    phone_number = phone_span[0].text
                try:
                    website_link = company_h1.find('a').get("href")
                except:
                    website_link = ''
                last_name = company_name 
                lead_type = 'Unknown'
                info = [company_name, commodity_name, city_name, state_name, phone_number, website_link, last_name, lead_type]
                thewriter.writerow(info)

                print(str(counter) + " grabbing " + str(company_name))
            except Exception as e: 
                print(e)
    while(page_count < 10):
        page_count+=1
        next_page_url = str(base_url) + str(next_page_url[1:-1] + str(page_count))
        print(next_page_url)
        print(page_count)
        myclick()    
                    #print("Error with " + str(counter))
                #wait 1 second between loops to avoid crashing webserver needs added*  
                #Event.wait(1)
        

#LABEL ABOVE URL INPUT
w = ttk.Label(text="ENTER URL", compound="top", foreground="white", background="black")
w.pack()
#Creates a Frame
frame = LabelFrame(win, width= 700, height= 400, bd=5)
frame.pack()
#Stop the frame from propagating the widget to be shrink or fit
frame.pack_propagate(False)

#Create an Entry widget in the Frame
entry = ttk.Entry(frame, width= 300)
entry.insert(INSERT, last_url)
entry.pack()
#Create a Button
ttk.Button(win, text="GET LEADS", command= myclick).pack(pady=20)

threads = []
parser = threading.Thread(target=myclick)
threads.append(parser)
win.mainloop()






