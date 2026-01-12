import logging
import azure.functions as func
import pymongo
from bson.objectid import ObjectId

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('UpdateAdvertisement function processed a request.')

    id = req.params.get('id')
    
    if not id:
        return func.HttpResponse(
            "Please pass an id on the query string",
            status_code=400
        )

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        import os
        url = os.environ["MyDbConnection"]
        
        client = pymongo.MongoClient(url)
        database = client['neighborly']
        collection = database['advertisements']

        query = {'_id': ObjectId(id)}
        new_values = {"$set": req_body}
        collection.update_one(query, new_values)
        
        return func.HttpResponse(
            "Advertisement updated successfully",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
