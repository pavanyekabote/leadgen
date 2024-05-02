from get import method_GET
from post import method_POST
import json


def main(event, context):
    print("Event is ", event)

    if event.get("httpMethod") == 'POST':
        return method_POST(event, context)
    elif event.get("httpMethod") == 'GET':
        return method_GET(event, context)
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Request method not supported"})
    }
