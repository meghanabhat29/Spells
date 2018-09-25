import urllib.request
import gc
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient

PARSE_URL = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
SHOW_URL_FORMAT = "https://en.wikipedia.org"
INFOBOX_ITEMS_TAG = "tr"
CONTENT_SAPERATOR = "\n"
LOG_FILE_NAME = "logs.txt"
SHOW_DETAILS_COLLECTION_NAME = "series_details"
crapLinkTitleList = ['Wikipedia:Link rot',]
listed_tags = ['Created by','Starring','Executive producer(s)','Production company(s)']

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

def get_show_entry_details(entry,existing_dict):
    each_entry_details = entry.find('th')
    if entry.th != None:
        entry_name = str(entry.th.text)
        if str(entry.th.text) in listed_tags:
            values_list = entry.td.stripped_strings
            detail_list = list()
            for detail in values_list:
                detail_list.append(detail)
            existing_dict[entry_name] = detail_list
        else:
            if entry.td != None:
                entry_value = str(entry.td.text).strip("\n")
                existing_dict[entry_name] = entry_value
            else:
                existing_dict[entry_name] = ''
        pprint(existing_dict)
        return existing_dict
    else:
        return existing_dict

def get_card_info(card_detail_soup):
    entry_desc_dict = {
    "show_name" : card_detail_soup[0].text,
    }
    for entry in card_detail_soup[1:]:
        entry_desc_dict = get_show_entry_details(entry,entry_desc_dict)
    return entry_desc_dict

def getShowDescriptiveInfoList(showLinkList):
    for show in showLinkList:
        showPageSoup = getIndividualShowSoup(show['url'])
        filteredElementDictionary = getFilteredElementDictionary('table','class','infobox vevent')
        showInfoCardSoup = getFilteredElementInSoup(showPageSoup,filteredElementDictionary)

        if isCardExist(showInfoCardSoup,filteredElementDictionary,show['url']):
            allShowCardDetails = getAllElementsInsoup(showInfoCardSoup,INFOBOX_ITEMS_TAG)
            cleaned_card_detail = get_card_info(allShowCardDetails)
            #write_to_db(SHOW_DETAILS_COLLECTION_NAME,allShowCardDetails)


def runGarbageCollector():
    gc.collect()

def logExceptionsToFile(e,showUrl):
    with open(LOG_FILE_NAME, 'a') as filePointer:
        filePointer.write(CONTENT_SAPERATOR + str(e) + " at " + showUrl)

def write_to_db(collection_name,content):
    write_client = MongoClient('localhost', 27017)
    write_client_db = write_client.shows_db
    write_client_db.collection_name.insert_one(content)

def displayDictList(showList):
    for show in showList:
        pprint("Name:" + show['name'] + "\n" + "Link:" + show['url'] + "\n")

def displayAnyList(anyList):
    for item in anyList:
        pprint(item)
