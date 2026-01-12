import logging
import azure.functions as func
import pymongo
from bson.json_util import dumps

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GetPosts function processed a request.')

    try:
        import os
        url = os.environ["MyDbConnection"]
        
        client = pymongo.MongoClient(url)
        database = client['neighborly']
        collection = database['posts']

        result = collection.find({})
        
        return func.HttpResponse(
            dumps(result),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
