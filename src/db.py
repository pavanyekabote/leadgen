from pymongo import MongoClient
from pymongo.database import Database
from config import DBConfig, DBCollections
from datetime import datetime

class MongoDb:

    _CONNECTION = None

    def __init__(self) -> None:
        self._connection = MongoClient(DBConfig.URI)
        self._db: Database = self._connection[DBConfig.NAME]
        print("BD is ", self._db)

    @staticmethod 
    def get_instance():
        if not MongoDb._CONNECTION:
            MongoDb._CONNECTION = MongoDb()
        return MongoDb._CONNECTION
    
    @property
    def db(self) -> Database:
        print("DB INS ", self._db)
        return self._db



def save_request(data):
    db = MongoDb.get_instance().db
    keywords = data.get('keywords')
    user = data.get('user')
    platform = data.get("platform") 

    print(f"Saving user {user} request to scrape platform {platform} with keywords {keywords}")


    payload = {
        "keywords": keywords,
        "user": user,
        "platform": platform,
        "created_date": datetime.utcnow()
    }
    id = db[DBCollections.USER_LOG].insert_one(payload).inserted_id
    print(f"Saved user {user} request to scrape platform {platform} with keywords {keywords}")


def save_login_details(data):
    
    db: Database = MongoDb.get_instance().db
    user = data.get("user")
    print(f"Saving login log to db for user :: {user}")
    login_with = data.get('login_with')
    platform = data.get("platform")
    payload = {"user": user, "login_with": login_with, "platform": platform, "created_date": datetime.utcnow()}
    db[DBCollections.USER_LOGIN].insert_one(payload)
    print(f"Login log is saved successfully for user :: {user}")

def save_cookies(data):
    db: Database = MongoDb.get_instance().db
    user = data.get("user")
    cookies = data.get("cookies")
    collection = db[DBCollections.USER_COOKIES]
    print(f"Saving cookies of user {user} to db")
    recent_cookie = collection.find_one({"user": user}, sort=[("created_date", -1)])
    if recent_cookie:
        collection.update_one({"user": user, "_id": recent_cookie.get("_id")}, { "$set": { "expired": True } })
        print(f"Set recent cookie {recent_cookie.get('_id', '')} to expired.")
    payload = {
        "user": user,
        "cookies": cookies,
        "created_date": datetime.utcnow(),
        "expired": False
    }
    cookie_id = collection.insert_one(payload).inserted_id
    print(f"Cookie has been inserted for user :: {user} with cookie record id :: {cookie_id}")

def get_user_cookies(data):
    user = data.get("user")
    db: Database = MongoDb.get_instance().db
    col = db[DBCollections.USER_COOKIES]
    return col.find_one({"user": user}, sort=[("created_date", -1)])
