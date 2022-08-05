# qgis-processing-rest-api 🌍⚙

## Description

This is a REST API that expose algorithms written in QGIS processing framework.

QGIS processing framework guide: https://docs.qgis.org/3.22/en/docs/user_manual/processing/index.html

## Capabilities

`GET /ping` - check the status of the API

`GET /list` - lisg all QGIS processing algorithms available

`GET /help/<provider_id>/<algorithm_id>` - return help and documentation for the specified algorithm

`POST /process/<provider_id>/<algorithm_id>` - process the specified algorithm with given parameters. Accepts JSON produces JSON.

## Contents

```
.
├── app
│   ├── logs
│   ├── app.py
│   ├── executer.py
│   ├── helpers.py
│   └── utils.py
├── docs
│   └── postman_collection.json
├── test-data
│   ├── benchmarks
│   ├── inputs
│       └── ...
│   └── outputs
├── Dockerfile
├── docker-compose.yml
├── plugins.txt
├── readme.md
└── requirements.txt
```

## Getting started

1. Clone the repository
1. Add an `.env` file
1. `$docker-compose build`
1. `$docker-compose up`
1. Go to `http://localhost:5000/ping`
1. Read documention `http://localhost:5000/apidocs`

### Example request

```sh
curl --location --request POST 'http://localhost:5000/process/native/buffer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "INPUT": "/test-data/inputs/aoi.shp",
    "DISTANCE": 0.01,
    "SEGMENTS": 5,
    "END_CAP_STYLE": 0,
    "JOIN_STYLE": 0,
    "MITER_LIMIT": 2,
    "DISSOLVE": false,
    "OUTPUT": "/test-data/outputs/buffer/aoi_buff.shp"
}'
```

## Environment file

```properties
FLASK_ENV="development"

DEBUG="TRUE"
TIMEZONE="US/Eastern"
```
