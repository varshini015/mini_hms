import json

def hello(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Hello from Serverless API!",
            "source": "mini_hms serverless"
        })
    }
