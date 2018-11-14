from other_utils import *

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
