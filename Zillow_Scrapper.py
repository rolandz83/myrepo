#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas
#import time << needed for getstat() to avoid captcha

base_url = "https://www.zillow.com/"
town = input('Enter town and state e.g: "hicksville NY"')
url = base + "-" + town + "/"
page_counter = 1

data = start_parse(url, page_counter) #for local test: start_parse("Zillow_Local.html")

df = pandas.DataFrame(data)
df.to_csv("Output.csv")


def start_parse(url, page):
    head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
        'referer':'https://www.google.com/'}
    r = requests.get(url, headers=head)
    content = r.content

    #For Testing with a local file
    #with open(url, "r", encoding='UTF-8') as f:
    #   content = f.read()

    soup = BeautifulSoup(content,"html.parser")
    allcards = soup.find_all("div",{"class":"list-card-info"})

    for cards in allcards:
        listing = {}
        address = cards.find("address",{"class":"list-card-addr"}).text.split(",")
        listing["Address"] = address[0]
        listing["Locality"] = address[1] + ", " + address[2]
        listing["Price"] = cards.find("div",{"class":"list-card-price"}).text
        listing["Status"] = getstat(card.find("a", {"class":"list-card-link"}).attrs['href'])
        listing["Listing URL"] = card.find("a", {"class":"list-card-link"}).attrs['href']
        data.append(listing)

    if is_it_lastpage(soup):
        return data
    else:
        page += 1
        start_parse(url + str(page) + "_p/", page)


def getstat(url):
    """ CODE NOT TESTED WITH LIVE DATA
        individual home listing url passed, function waits for 60 sec then
        sends a requests to avoid captcha  """

    #time.sleep(60)
    #head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    #r = requests.get("url", headers=head)
    #c = r.content
    #soup = BeautifulSoup(c,'html.parser')
    #return soup.find('span',{"class":"ds-status-details"}).text)
    return None


def is_it_lastpage(c):
    ''' CODE NOT TESTED WITH LIVE DATA
    returns true if next page button disabled
    '''
    next = c.find_all('a', {"rel":"next"})
    return next[0]['disabled'] == '' and next[0]['tabindex'] == "-1")
