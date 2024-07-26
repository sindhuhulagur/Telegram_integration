
import pytz
from bson import CodecOptions
from pymongo import MongoClient
from app_config import AppConfig
from fastapi import APIRouter

app_configs_data = AppConfig()
router = APIRouter()


class MongoData:
    def __init__(self, database):
        mongo_conn = app_configs_data.get_database()
        self.client = MongoClient(host=mongo_conn["host"], port=mongo_conn["port"],
                                  username=mongo_conn["user_name"], password=mongo_conn["password"])
        self.database = self.client[database]

    def get_data(self, table_name, site_id, client_id, query=None, arguments=None):
        try:
            if query is None:
                query = {"$or": [{"site_id": site_id, "client_id": client_id, "isdeleted": {"$in": [False, "false"]}},
                                 {"default": True},
                                 {"site_id": site_id, "client_id": client_id, "is_deleted": {"$in": [False, "false"]}}]}
            if arguments is None:
                arguments = {"_id": 0, "_insertedTS": 0, "_modifiedTS": 0}
            if site_id and query:
                query.update({"site_id": {"$in": [site_id, '', None]}})
            if client_id and query:
                query.update({"client_id": {"$in": [client_id, '', None]}})
            if arguments == {}:
                return self.database[table_name].find(query)
            return self.database[table_name].find(query, arguments)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def get_one(self, table_name, site_id, client_id, query=None, arguments=None):
        try:
            if query is None:
                query = {"$or": [{"site_id": site_id, "client_id": client_id, "isdeleted": {"$in": [False, "false"]}},
                                 {"default": True},
                                 {"site_id": site_id, "client_id": client_id, "isdeleted": {"$in": [False, "false"]}}]}
            if arguments is None:
                arguments = {"_id": 0, "_insertedTS": 0, "_modifiedTS": 0}
            if site_id and query:
                query.update({"site_id": {"$in": [site_id, '', None]}})
            if client_id and query:
                query.update({"client_id":  {"$in": [client_id, '', None]}})
            return self.database[table_name].find_one(query, arguments)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def hard_delete(self, table_name, query):
        try:
            return self.database[table_name].remove(query)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def insert_update_delete(self, table_name, operation_type, insert_data, unique_key=None, unset_data=None, multi=False):
        try:
            if operation_type == "insert":
                return self.database[table_name].insert_one(insert_data)
            elif operation_type == "find_one_and_update":
                return self.database[table_name].update_one(unique_key, {"$set": insert_data}, upsert=True)
            elif operation_type == "update":
                if not multi:
                    return self.database[table_name].update_one(unique_key, {"$set": insert_data})
                else:
                    return self.database[table_name].update_many(unique_key, {"$set": insert_data})
            elif operation_type == "delete":
                return self.database[table_name].update(unique_key, {"$set": insert_data}, multi=multi)
            elif operation_type == "unset":
                return self.database[table_name].update(unique_key, {"$unset": unset_data})
            elif operation_type == "hard_delete":
                return self.database[table_name].delete_one(unique_key)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def mongo_aggregate(self, table_name, query=None):
        try:
            return self.database[table_name].aggregate(query)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def count_records(self, table_name, query=None):
        try:
            return self.database[table_name].count_documents(query)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def aggregate_func(self, table_name, pipe):
        try:
            return list(self.database[table_name].aggregate(pipeline=pipe))
        except Exception as e:
            return {"message": e, "status": "failed"}

    def get_collections(self):
        try:
            return self.database.list_collection_names()
        except Exception as e:
            return {"message": e, "status": "failed"}

    def ensure_index_common(self, table_name, operation_name, time):
        try:
            return self.database[table_name].ensure_index(operation_name, expireAfterSeconds=time)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def drop_index_common(self, table_name, operation_name):
        try:
            return self.database[table_name].drop_index(operation_name)
        except Exception as e:
            return {"message": e, "status": "failed"}

    def get_with_options(self, table_name, time_zone, query, from_data, length_upto, sort_based_on, sort_type):
        try:
            coll = self.database[table_name].with_options(codec_options=CodecOptions(
                tz_aware=True,
                tzinfo=pytz.timezone(time_zone)))
            data = coll.find(query).skip(
                int(from_data)).limit(int(length_upto)).sort(f'{sort_based_on}', int(sort_type))
            return data
        except Exception as e:
            print(e)
            return {"message": e, "status": "failed"}

