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
craplinkList = ['Wikipedia:Link rot',]
listed_tags = ['Created by','Starring','Executive producer(s)','Production company(s)','Past members']


def is_none_object(obj_to_check):
    return (obj_to_check is None)

def is_in_unwanted_list(link):
    return (link in craplinkList)

def is_info_card_exist(soup,filtered_element_dictionary,show_url):
    try:
        get_all_elements_in_tree(soup,filtered_element_dictionary)
    except Exception as e:
        log_exceptions(e,show_url)
        return False
    else:
        return True

def get_show_soup(show_url):
    return get_soup_from_url(str(SHOW_URL_FORMAT + show_url))

def  get_show_link_dictionary(show_soup_obj):
    show = {
        'name':show_soup_obj.get('title'),
        'url':show_soup_obj.get('href')
    }
    return show

def get_tag_value_in_soup(soup,tag):
    return soup.find(tag)

def get_all_elements_in_tree(soup,element):
    return soup.find_all(element)

def get_filtered_element_dictionary(tag,attribute,attribute_value):
    return {
    'tag':tag,
    'attribute':attribute,
    'attribute_value':attribute_value,
    }

def get_filtered_element_from_soup(soup,elements_to_filter):
    return soup.find(elements_to_filter['tag'],{elements_to_filter['attribute']:elements_to_filter['attribute_value']})

def get_soup_from_url(url):
    tv_shows_soup = None
    try:
        with urllib.request.urlopen(url) as response:
            page_status = response.status
            if page_status == 200:
                html = response.read()
                tv_shows_soup = BeautifulSoup(html, 'lxml')
            return tv_shows_soup
    except:
        return tv_shows_soup

def get_card_info(card_detail_soup):
    entry_desc_dict = {
    "show_name" : card_detail_soup[0].text,
    }
    for entry in card_detail_soup[1:]:
        entry_desc_dict = get_show_entry_details(entry,entry_desc_dict)
    return entry_desc_dict

def get_tv_shows(soup):
    tv_shows = list()
    tv_shows_filtered = soup.find('div',{'class':'mw-parser-output'}).find_all('i')
    for show in tv_shows_filtered:
        show_obj = get_tag_value_in_soup(show,'a')
        if not is_none_object(show_obj):
            show_dictionary = get_show_link_dictionary(show_obj)
            if not is_in_unwanted_list(show_dictionary['name']):
                tv_shows.append(show_dictionary)
    return tv_shows

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
        return existing_dict
    else:
        return existing_dict

def log_exceptions(e,show_url):
    with open(LOG_FILE_NAME, 'a') as filePointer:
        filePointer.write(CONTENT_SAPERATOR + str(e) + " at " + show_url)

def write_to_db(content):
    write_client = MongoClient('localhost', 27017)
    write_client_db = write_client.shows_db
    write_client_db.tv_series_details.insert(content,check_keys=False)

def write_to_file(content):
    with open(SHOW_DETAILS_FILE_NAME, 'a') as filePointer:
        filePointer.write( CONTENT_SAPERATOR + str(content))

def display_show_list(shows):
    for show in shows:
        pprint("Name:" + show['name'] + "\n" + "Link:" + show['url'] + "\n")

def display_list(list_values):
    for item in list_values:
        pprint(item)

def fetch_show_info(show_links):
    # Card Filter Dictionaries
    INFOBOX_VEVENT = get_filtered_element_dictionary('table','class','infobox vevent')
    INFOBOX = get_filtered_element_dictionary('table','class','infobox')
    INFOBOX_VPLAINLIST = get_filtered_element_dictionary('table','class','infobox vcard plainlist')

    for show in show_links:
        show_page = get_show_soup(show['url'])
        if show_page == None:
            continue

        filtered_element_dictionary = INFOBOX_VEVENT
        show_info_card = get_filtered_element_from_soup(show_page,filtered_element_dictionary)

        if show_info_card == None:
            filtered_element_dictionary = INFOBOX
            show_info_card = get_filtered_element_from_soup(show_page,filtered_element_dictionary)

        if show_info_card == None:
            filtered_element_dictionary = INFOBOX_VPLAINLIST
            show_info_card = get_filtered_element_from_soup(show_page,filtered_element_dictionary)

        if is_info_card_exist(show_info_card,filtered_element_dictionary,show['url']):
            show_details_soup = get_all_elements_in_tree(show_info_card,INFOBOX_ITEMS_TAG)
            cleaned_show_card_details = get_card_info(show_details_soup)
            write_to_db(cleaned_show_card_details)
