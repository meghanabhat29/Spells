from crawl_utils import *

def main():
    all_show_list_page = get_soup_from_url(PARSE_URL)
    shows_list = get_tv_shows(all_show_list_page)
    fetch_show_info(shows_list)

if __name__ == '__main__':
    main()
