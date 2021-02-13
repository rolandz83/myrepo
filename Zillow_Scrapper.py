
#import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas

#base_url = "https://www.zillow.com/"
#town = input('Enter town and state e.g: "hicksville NY"')
#url = base + "-" + town + "/"
url = "C:\\Users\\user1\\Desktop\\ZillowSearchResult\\NYZillow.htm"
page_counter = 1
data = []

def start_parse(url, page):
    #head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    #    'referer':'https://www.google.com/'}
    #r = requests.get(url, headers=head)
    #content = r.content

    #For Testing with a local file
    with open(url, "r", encoding='UTF-8') as f:
       content = f.read()

    soup = BeautifulSoup(content,"html.parser")
    allcards = soup.find_all("div",{"class":"list-card-info"})

    for cards in allcards:
        listing = {}
        address = cards.find("address",{"class":"list-card-addr"}).text.split(",")
        listing["Address"] = address[0]
        listing["Locality"] = address[1] + ", " + address[2]
        listing["Price"] = cards.find("div",{"class":"list-card-price"}).text
        listing["Status"] = cards.find("li", {"class":"list-card-statusText"}).text[2:]
        listing["Listing URL"] = cards.find("a", {"class":"list-card-link"}).attrs['href']
        listing["Date"] = datetime.now().strftime("%d-%B-%Y %H:%M:%S:%f")
        listing["PageNum"] = str(page)
        data.append(listing)

    if is_it_lastpage(soup):
        return None
    else:
        page += 1
        start_parse("C:\\Users\\user1\\Desktop\\ZillowSearchResult\\NYZillow_p2.htm", page)
        #start_parse(url + str(page) + "_p/", page)

def is_it_lastpage(c):
    next = c.find_all('a', {"rel":"next"})
    try:
        return next[0]['disabled'] == '' and next[0]['tabindex'] == "-1"
    except KeyError:
        return False

start_parse(url, page_counter) #for local test: start_parse("Zillow_Local.html")

df = pandas.DataFrame(data)
df.to_csv("Output.csv")
