# Simple translation app

With this application, you can create, read, update and delete translations for different translation codes.

The application uses a local instance of AWS DynamoDB to keep track of the translations. The database uses HashKey "LanguageCode", SortKey "LanguageKey" and translations will be stored in "Translation".

## Getting Started

### Dependencies

* docker-compose
* docker
* Windows/Ubuntu/Mac

### Installing

* Either clone this project, download the zip or use the zip that has been sent to you
* If something fails, a potential fix could be to lower the version number on line no.1 in docker-compose.yml

### Executing program

* Navigate to the base folder (where you can see docker-compose.yml) and run the following command:
```
docker-compose up --build

(--build tag isn't needed for every single run)
```
* The state of the database is persistent throughout, so you can compose down without losing data


### Using the API

* The following endpoints exists:

```
GET

localhost:5000/translations

Query Params:
* language-code (mandatory)
* language-key  (optional, if missed out, fetches all translations for provided code)
```

```
POST

localhost:5000/translations


Attach a body with format of json, must be formatted accordingly to JSON-API specification https://jsonapi.org/
{
    "data": {
        "type": "translations",
        "attributes": {
            "languageCode": "en",
            "languageKey": "drink-water",
            "translation": "Drink water"
        }
    }
}

```

```
PUT (Post requests sent with identical code and key will replace the translation)

localhost:5000/translations

Attach a body with format of json, must be formatted accordingly to JSON-API specification https://jsonapi.org/
{
    "data": {
        "type": "translations",
        "attributes": {
            "languageCode": "en",
            "languageKey": "drink-water",
            "translation": "Drink water"
        }
    }
}
```

```
DELETE

localhost:5000/translations

localhost:5000/translations

Query Params:
* language-code (mandatory)
* language-key  (mandatory)
```

Preview of the database:

![image](https://user-images.githubusercontent.com/39117571/118272920-9963a980-b4c3-11eb-906d-f01ef221eee4.png)

Preivew of a json response:

![image](https://user-images.githubusercontent.com/39117571/118273008-b26c5a80-b4c3-11eb-9d51-2c46cce1961c.png)
