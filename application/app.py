import logging, boto3
from flask import Flask, jsonify, request
from Database import getAllItemsForLanguageCode, getTranslationForCodeAndKey, createTranslationForCodeAndKey
from InitiateDatabase import createTranslationsTable

app = Flask(__name__)
table = None

@app.route('/alive', methods=['GET'])
def alive():
    data = {'Status': 'Alive & well'}
    return jsonify(data), 200

@app.route('/translations', methods=['GET'])
def getAllTranslationsForCode():
    languageCode = None
    languageKey = None

    try:
        if request.args.get('language-code') != None:
            languageCode = request.args.get('language-code')
        if request.args.get('language-key') != None:
            languageKey = request.args.get('language-key')

        logging.info("i got this far")
        
        if (languageCode is not None) and (languageKey is not None):
            items = getTranslationForCodeAndKey(languageCode, languageKey)

        elif (languageCode is not None) and (languageKey is None):
            items = getAllItemsForLanguageCode(languageCode)

        elif (languageCode is None):
            return jsonify("Missing parameters."), 400

        translations = {}

        for item in items:
            translations[item['LanguageKey']] = item['Translation']

        return jsonify(translations), 200

    except Exception as e:
        logging.error(e)
        return jsonify("Error in getting translations, dude"), 500

@app.route('/translations', methods=['POST'])
def createTranslation():
    body = None
    try: 
        body = request.json
        assert body is not None
    except Exception as e:
        return jsonify({'Status': '500', 'Message': 'Error while fetching request\'s body. Body can\'t be empty.'})
    
    try:
        attributes = body['data']['attributes']
        languageKey = attributes['languageKey']
        languageCode = attributes['languageCode']
        translation = attributes['translation']

        body = createTranslationForCodeAndKey(languageCode, languageKey, translation)

    except Exception as e:
        print(e)
        return jsonify({'Status': '500', 'Message': 'Some attributes are missing.'})
    

    return(body)

# We only need this for local development.
if __name__ == '__main__':
    app.run(debug=True)
