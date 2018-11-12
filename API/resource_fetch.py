import traceback
from pymongo import MongoClient

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
