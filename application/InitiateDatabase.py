from logging import Logger
import logging
import boto3

def createTranslationsTable(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    try:
        dynamodb.create_table(
        TableName='translations',
        KeySchema=[
            {
                'AttributeName': 'LanguageCode',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'LanguageKey',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'LanguageCode',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'LanguageKey',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    except Exception as e:
        logging.error("Table already exists")
        pass
