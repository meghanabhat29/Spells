import traceback
from pymongo import MongoClient
from bson.json_util import dumps

class ShowAPI():

    Mongo_Obj = MongoClient('localhost', 27017)
    shows_db = Mongo_Obj.shows_db

    def get(self):
        return self.shows_db

def get_all_shows():
    db_cursor_obj = ShowAPI()
    db_cursor = db_cursor_obj.get()
    try:
        tv_shows_sources = db_cursor.tv_series_details.find({})

        if tv_shows_sources == None:
            error_message = {"status":"error","message":"Internal error. Shows cannot be found."}
            return error_message

        all_tv_show_list = list()
        for show in tv_shows_sources:
            show = {
            "name": show['show_name'],
            "api_url":"/api/show/"+ str(str(show['show_name']).replace(' ','_')),
            }
            all_tv_show_list.append(show)
        return all_tv_show_list

    except Exception as e:
        print(traceback.format_exc())

def get_show_details(show_name):
    db_cursor_obj = ShowAPI()
    db_cursor = db_cursor_obj.get()

    try:
        show_details_query={"show_name":str(show_name).replace('_',' ')}
        tv_shows_details = db_cursor.tv_series_details.find_one(show_details_query)

        if tv_shows_details == None:
            error_message = {"status":"error","message":"No such show exist."}
            return error_message

        tv_show_desc = {
        "show_name":tv_shows_details["show_name"],
        "Genre":tv_shows_details["Genre"],
        "Distributor":tv_shows_details["Distributor"],
        "Running_time":tv_shows_details["Running time"],
        "No. of episodes":tv_shows_details["No. of episodes"],
        "Production company(s)":tv_shows_details["Production company(s)"],
        "Original network":tv_shows_details["Original network"],
        "Executive producer(s)":tv_shows_details["Executive producer(s)"],
        "Country of origin":tv_shows_details["Country of origin"],
        "No. of seasons":tv_shows_details["No. of seasons"],
        }

        return tv_show_desc
    except Exception as e:
        print(traceback.format_exc())
