from bs4 import BeautifulSoup
import urllib.request

PARSE_URL = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
crapLinkTitleList = ['Wikipedia:Link rot',]

def getUrlSoup(url):
    with urllib.request.urlopen(url) as response:
         html = response.read()
         tvShowListsoup = BeautifulSoup(html, 'html.parser')
         return tvShowListsoup

def isNoneObject(checkObj):
    if checkObj is None:
        return True
    else:
        return False

def  getShowDict(showObj):
    show = {
        'name':showObj.get('title'),
        'url':showObj.get('href')
    }
    return show

def isInCrapList(linkTitle):
    if linkTitle in crapLinkTitleList:
        return True
    else:
        return False
def findTagInSoupObject(soupObject,tagName):
    return soupObject.find(tagName)

def getTvShowList(soupedData):
    tvShowList = list()
    filteredTvShowEntries = soupedData.find('div',{'class':'mw-parser-output'}).find_all('i')
    for showEntry in filteredTvShowEntries:
        showObj = findTagInSoupObject(showEntry,'a')
        if not isNoneObject(showObj):
            showDictionary = getShowDict(showObj)
            if not isInCrapList(showDictionary['name']):
                tvShowList.append(showDictionary)
    return tvShowList 

def displayDictList(showList):
    for show in showList:
        print("Name:" + show['name'] + "\n" + "Link:" + show['url'] + "\n")