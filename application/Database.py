import logging
import boto3
from flask.json import jsonify
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb',
    endpoint_url="http://dynamodb:8000",
    region_name="eu-north-1",
    verify=False
)
hashKey = "LanguageCode"
rangeKey= "LanguageKey"

def getAllItemsForLanguageCode(code):
    try:
        table = dynamodb.Table("translations")
    except Exception as e:
        return jsonify({'Status': '500', 'Message': 'Could not find table name called translations'})

    try:
        response = table.query(
            KeyConditionExpression=Key(hashKey).eq(code)
        )

    except Exception as e:
        logging.error(e)
        return jsonify({'Status': '500', 'Message': 'Error while querying the table'})

    logging.info("___________")
    logging.info("Response:")
    logging.info(response)
    return response['Items']

def getTranslationForCodeAndKey(code, key):
    try:
        table = dynamodb.Table("translations")
    except Exception as e:
        return jsonify({'Status': '500', 'Message': 'Could not find table name called translations'})

    try:
        response = table.query(
            KeyConditionExpression=Key(hashKey).eq(code) & Key(rangeKey).eq(key)
        )
        
    except Exception as e:
        return jsonify({'Status': '500', 'Message': 'Error while querying the table'})

    return response['Items']

def createTranslationForCodeAndKey(code, key, translation="missing translation"):
    try:
        table = dynamodb.Table("translations")
        
    except Exception as e:
        return jsonify({'Status': '500', 'Message': 'Could not find table name called translations'})

    try:
        response = table.put_item(
        Item={
                'LanguageCode': code,
                'LanguageKey': key,
                'Translation': translation
            }
        )
    except Exception as e:
        return jsonify({'Status': '500', 'Message': 'Error while putting item'})

    return response
