# ----- IMPORTS STARTS -----------------
import traceback
from flask import jsonify, request
from models.base_model import BaseModel
# from models.redis_client import RedisClient
from configs.database import check_mongo_connection
# ----- IMPORTS ENDS  -----------------


def hello_world():
    return '<p>Hello World</p>'

# ======================================
#     MONGO TEST ROUTES
# ======================================
class TestMongo(BaseModel):
    def __init__(self, collection:str):
        super().__init__(collection)

# mongo connection
def test_mongo_connection():
    return check_mongo_connection()

# mongo insert in specific collection
def test_mongo_insert(collection:str, data:dict):
    data = TestMongo(collection).insert(data)
    return {
        "status"    : "Success",
        "collection": collection,
        "data"      : str(data[0])
    }

# mongo get one from specific collection
def test_mongo_get(collection:str, data:dict):
    data        = TestMongo(collection).find_all(data)
    return {
        "status"    : "Success",
        "collection": collection,
        "data"      : data
    }

# mongo get all from specific collection
def test_mongo_get_all(collection:str):
    data = TestMongo(collection).find_all()
    return {
        "status"    : "Success",
        "collection": collection,
        "data"      : data
    }

# mongo delete from specific collection
def test_mongo_delete(collection:str, data:dict):
    data = TestMongo(collection).delete(data)
    return {
        "status"    : "Success",
        "collection": collection,
        "data"      : data
    }

# mongo update in specific collection
def test_mongo_update(collection:str, filter:dict, update:dict):
    print("test_mongo_update:",filter,update)
    if "_id" in filter:
        data = TestMongo(collection).update_by_id(filter["_id"], update)
    else:
        data = TestMongo(collection).update(filter, update)

    return {
        "status"    : "Success",
        "collection": collection,
        "data"      : data
    }

# mongo usert in specific collection
def test_mongo_upsert(collection:str, filter:dict, update:dict):
    data = TestMongo(collection).insert_or_update(filter,update)
    return {
        "status"    : "Success",
        "collection": collection,
        "data"      : data
    }


# ======================================
#     REDIS TEST ROUTES
# ======================================
# redis connection
def test_redis_connection():
    check = RedisClient().check_connection()
    if check['status']:
        return {
            "status": "Success",
            "message": "Redis connection successful."
        }
    else:
        return {
            "status": "Error",
            "message": check['message']
        }

# redis store in specific key
def test_redis_store(key:str, value:str, expire:int=0):
    if int(expire) != 0:
        check = RedisClient().set(key, value, expire)
    else:
        check = RedisClient().set(key, value)

    return {
        "status": "Executed",
        "data"  : check
    }

def test_redis_get_all_keys():
    check = RedisClient().keys()
    return {
        "status": "Executed",
        "data": check
    }

# redis get from specific key
def test_redis_get(key:str):
    check = RedisClient().get(key)
    return {
        "key"   : key,
        "status": "Executed",
        "data"  : check
    }

# redis get all keys
def test_redis_get_all():
    check = RedisClient().get_all()
    return {
        "status": "Success",
        "data": check
    }

# redis delete from specific key
def test_redis_delete(key:str):
    check = RedisClient().delete(key)
    return {
        "key"   : key,
        "status": "Executed",
        "data"  : check
    }

# redis flush all keys
def test_redis_flush():
    check = RedisClient().flushdb()
    return {
        "status": "Success",
        "message": str(check)
    }

# data encode using frowzy and secret
def test_data_encode(cdc:str, secret:str, key:str):
    return {
        'tangled': data_tangle(cdc, secret, key)
    }

def test_implementation():
    try:
        token = request.headers.get('auth-token')
        if token == "jkeehitf9922496ec864c9b1jjkk78725d22f29bae753da6b52e17gghyu67545kk":
            request_data = request.json
            method_name  = request_data['method']
            parameters   = request_data['data'] if 'data' in request_data else {}
            collection   = parameters['collection'] if 'collection' in parameters else None
            func         = globals()[method_name]

            if 'data' in parameters and len(parameters['data']) != 0:

                if method_name in ["test_mongo_insert","test_mongo_get","test_mongo_get_all","test_mongo_delete"]:
                    result = func(*(collection, parameters['data']))

                elif method_name in ["test_mongo_update", "test_mongo_upsert"]:
                    search = parameters['data']['filter']
                    update = parameters['data']['update']
                    result = func(*(collection, search, update))

                else:
                    result = func(*parameters)
            else:
                if collection:
                    result = func(collection)

                else:
                    if method_name in ["test_redis_store"]:
                        key    = parameters['key']
                        value  = parameters['value']
                        expire = parameters['expire'] if parameters['expire'] else 0
                        result = func(*(key, value, expire))

                    elif method_name in ["test_redis_get", "test_redis_delete"]:
                        key    = parameters['key']
                        result = func(key)

                    elif method_name in ["test_data_encode"]:
                        cdc    = parameters['cdc']
                        key    = parameters['key']
                        secret = parameters['secret']
                        result = func(cdc, secret, key)

                    elif method_name in ["test_bmg_order_data_api"]:
                        token     = parameters['token']
                        order_ids = parameters['order_ids']
                        result    = func(token, order_ids)

                    else:
                        result = func()


            return jsonify(result), 200

        else:
            return jsonify({
                'status': 'false',
                'message': 'Authentication failed'
            }), 401
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status'   : 'false',
            'message'  : e,
        }), 500