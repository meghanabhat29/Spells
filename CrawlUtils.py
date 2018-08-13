from bs4 import BeautifulSoup
import urllib.request

PARSE_URL = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
crapLinkTitleList = ['Wikipedia:Link rot',]

def getUrlSoup(url):
    with urllib.request.urlopen(url) as response:
         html = response.read()
         tvShowListsoup = BeautifulSoup(html, 'html.parser')
         return tvShowListsoup


def getTvShowList(soupedData):
    tvShowList = list()
    for listing in soupedData.find('div',{'class':'mw-parser-output'}).find_all('i'):
        showObj = listing.find('a')
        if showObj != None:
            showUrl = showObj.get('href')
            showName = showObj.get('title')
            if  showName not in crapLinkTitleList:
                show={
                    'name':showName,
                    'url':showUrl,
                }
                tvShowList.append(show)
    return tvShowList 

def displayDictList(showList):
    for show in showList:
        print("Name:" + show['name'] + "\n" + "Link:" + show['url'] + "\n")