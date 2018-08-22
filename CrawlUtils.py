import urllib.request
import gc
from bs4 import BeautifulSoup
from pprint import pprint

PARSE_URL = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
SHOW_URL_FORMAT = "https://en.wikipedia.org"
INFOBOX_ITEMS_TAG = "tr"
CONTENT_SAPERATOR = "\n\n\n"
LOG_FILE_NAME = "logs.txt"
SHOW_DETAILS_FILE_NAME = "showDetails.txt"
crapLinkTitleList = ['Wikipedia:Link rot',]

def isNoneObject(checkObj):
    return (checkObj is None)

def isInCrapList(linkTitle):
    return (linkTitle in crapLinkTitleList)

def isCardExist(soup,filteredElementDictionary,showUrl):
    try:
        getAllElementsInsoup(soup,filteredElementDictionary)
    except Exception as e:
        logExceptionsToFile(e,showUrl)
        return False
    else:
        return True

def getIndividualShowSoup(showUrl):
    return getUrlSoup(str(SHOW_URL_FORMAT + showUrl))

def  getShowLinkDict(showObj):
    show = {
        'name':showObj.get('title'),
        'url':showObj.get('href')
    }
    return show

def getTagInSoupObject(soupObject,tagName):
    return soupObject.find(tagName)

def getAllElementsInsoup(soupedData,element):
    return soupedData.find_all(element)

def getFilteredElementDictionary(tag,attribute,attributeValue):
    return {
    'tag':tag,
    'attribute':attribute,
    'attributeValue':attributeValue,
    }

def getFilteredElementInSoup(soupedData,filterDictionary):
    return soupedData.find(filterDictionary['tag'],{filterDictionary['attribute']:filterDictionary['attributeValue']})

def getUrlSoup(url):
    with urllib.request.urlopen(url) as response:
         html = response.read()
         tvShowListsoup = BeautifulSoup(html, 'lxml')
         return tvShowListsoup

def getTvShowList(soupedData):
    tvShowList = list()
    filteredTvShowEntries = soupedData.find('div',{'class':'mw-parser-output'}).find_all('i')
    for showEntry in filteredTvShowEntries:
        showObj = getTagInSoupObject(showEntry,'a')
        if not isNoneObject(showObj):
            showDictionary = getShowLinkDict(showObj)
            if not isInCrapList(showDictionary['name']):
                tvShowList.append(showDictionary)
    return tvShowList 

def getShowDescriptiveInfoList(showLinkList):
    for show in showLinkList:
        
        showPageSoup = getIndividualShowSoup(show['url'])
        filteredElementDictionary = getFilteredElementDictionary('table','class','infobox vevent')
        showInfoCardSoup = getFilteredElementInSoup(showPageSoup,filteredElementDictionary)
        
        if isCardExist(showInfoCardSoup,filteredElementDictionary,show['url']):
            allShowCardDetails = getAllElementsInsoup(showInfoCardSoup,INFOBOX_ITEMS_TAG)
            writeToFile(SHOW_DETAILS_FILE_NAME,allShowCardDetails)

def runGarbageCollector():
    gc.collect()

def logExceptionsToFile(e,showUrl):
    with open(LOG_FILE_NAME, 'a') as filePointer:
        filePointer.write(CONTENT_SAPERATOR + str(e) + " at " + showUrl)

def writeToFile(filename,content):
    with open(SHOW_DETAILS_FILE_NAME, 'a') as filePointer:
        filePointer.write( CONTENT_SAPERATOR + str(content))

def displayDictList(showList):
    for show in showList:
        pprint("Name:" + show['name'] + "\n" + "Link:" + show['url'] + "\n")

def displayAnyList(anyList):
    for item in anyList:
        pprint(item)
