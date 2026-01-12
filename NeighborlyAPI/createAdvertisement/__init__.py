import logging
import azure.functions as func
import pymongo
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('CreateAdvertisement function processed a request.')

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

        result = collection.insert_one(req_body)
        
        return func.HttpResponse(
            json.dumps({"id": str(result.inserted_id)}),
            mimetype="application/json",
            status_code=201
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
