import pymongo 

class Database():
    URI = "mongodb://127.0.0.1:27017"

    def __init__ (self, dbname): 
        self.client = pymongo.MongoClient(Database.URI)
        self.dbname = self.client[dbname]

    def insert(self,collection,data):
        self.dbname[collection].insert(data)

    def find(self,collection, query=None):
        return self.dbname[collection].find(query)

    def find_one(self,collection, query):
        return self.dbname[collection].find_one(query)
    
    def update_one(self, collection,query,update):
        self.dbname[collection].update_one(query,update, upsert=True)
    
    def get_list_collections(self):
        return self.dbname.list_collection_names()

