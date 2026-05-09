import pymongo
from pymongo.server_api import ServerApi
from config import cfg

dburl = cfg['db_url']
db = cfg['db_name']

client = pymongo.MongoClient(dburl, server_api=ServerApi('1'))
db = client[db]
profiles = db['profiles']

def db_profile_exist(uid):
    if profiles.find_one({"_id": uid}) is not None:  
        return True
    else:
        return False

def db_profile_exist_usr(username):
    if profiles.find_one({"username": username}) is not None:  
        return True
    else:
        return False

def db_profile_insertone(query):
    return profiles.insert_one(query)

def db_profile_access(uid):
    profile = profiles.find_one({'_id': uid})
    if profile:  
        return profile['access']
    return 0 

def db_profile_banned(uid):
    profile = profiles.find_one({'_id': uid})
    if profile:  
        return profile['ban'] == 1
    return False 

def db_profile_updateone(query, query2):
    return profiles.update_one(query, query2)

def db_profile_get_usrname(username, get):
    profile = profiles.find_one({'username': username})
    if profile:  
        return profile[get]
    return None 