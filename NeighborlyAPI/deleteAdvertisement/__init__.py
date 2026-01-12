import logging
import azure.functions as func
import pymongo
from bson.objectid import ObjectId

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('DeleteAdvertisement function processed a request.')

    id = req.params.get('id')
    
    if not id:
        return func.HttpResponse(
            "Please pass an id on the query string",
            status_code=400
        )

    try:
        import os
        url = os.environ["MyDbConnection"]
        
        client = pymongo.MongoClient(url)
        database = client['neighborly']
        collection = database['advertisements']

        query = {'_id': ObjectId(id)}
        collection.delete_one(query)
        
        return func.HttpResponse(
            "Advertisement deleted successfully",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
