import logging, boto3
from flask import Flask, jsonify, request
from Database import getAllItemsForLanguageCode, getTranslationForCodeAndKey, createTranslationForCodeAndKey, deleteTranslationByCodeAndKey

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
        return jsonify("Error in getting translations."), 500

@app.route('/translations', methods=['POST', 'PUT'])
def upsertTranslation():
    body = None
    try: 
        body = request.json
        assert body is not None
    except Exception as e:
        logging.error(e)
        return jsonify({'Status': '500', 'Message': 'Error while fetching request\'s body. Body can\'t be empty.'})
    
    try:
        attributes = body['data']['attributes']
        languageKey = attributes['languageKey']
        languageCode = attributes['languageCode']
        translation = attributes['translation']

        body = createTranslationForCodeAndKey(languageCode, languageKey, translation)

    except Exception as e:
        logging.error(e)
        return jsonify({'Status': '500', 'Message': 'Some attributes are missing.'})
    

    return(body)

@app.route('/translations', methods=['DELETE'])
def deleteTranslation():
    try:
        languageCode = None
        languageKey = None

        if request.args.get('language-code') is None or request.args.get('language-key') is None:
            return jsonify("Need both a code and a key to delete a translation."), 500
            
        languageKey = request.args.get('language-key')
        languageCode = request.args.get('language-code')

        response = deleteTranslationByCodeAndKey(languageCode, languageKey)

        return jsonify(response), 200

    except Exception as e:
        logging.error(e)
        return jsonify("Error while deleting item"), 500

# We only need this for local development.
if __name__ == '__main__':
    app.run(debug=True)
