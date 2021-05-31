# Streaming Service

from flask import Flask
from flask_restful import Resource, Api
import os
import flask
from flask_restful import Resource, Api
from flask import Flask, redirect, url_for, request, render_template, make_response
import pymongo
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import json
from bson import json_util

import logging

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.controls

class listAll(Resource):
    def get(self, format=None):
        k = request.args.get('top', default=-1, type=int)
        if k <= 0:
            k = None
        if format == None:
            format = "json"
        if format != "csv" and format != "json":
            return make_response(format + " is not a suported format.")
        allArr = []
        for things in db.controls.find({}, {"_id": 0, "km": 0})[:k]:
            allArr.append(things)
        if format == "json":
            allJson = {}
            for x in range(len(allArr)):
                 allJson[x+1] = allArr[x]
            return allJson
        if format == "csv":
            if len(allArr) == 0:
                return ""
            head = list(allArr[0].keys())
            values = ""
            for things in allArr:
                values = values + ','.join(list(things.values()))
                values = values + "\n"
            return (",".join(head) + "\n" + values[:-1])


class listOpenOnly(Resource):
        def get(self, format=None):
            k = request.args.get('top', default=-1, type=int)
            if k <= 0:
                k = None
            if format == None:
                format = "json"
            if format != "csv" and format != "json":
                return make_response(format + " is not a suported format.")
            openArr = []
            for things in db.controls.find({}, {"_id": 0, "km": 0, "close": 0})[:k]:
                openArr.append(things)
            if format == "json":
                openJson = {}
                for x in range(len(openArr)):
                    openJson[x + 1] = openArr[x]
                return openJson
            if format == "csv":
                if len(openArr) == 0:
                    return ""
                head = list(openArr[0].keys())
                values = ""
                for things in openArr:
                    values = values + ','.join(list(things.values()))
                    values = values + "\n"
                return (",".join(head) + "\n" + values[:-1])




class listCloseOnly(Resource):
    def get(self, format = None):
        k = request.args.get('top', default=-1, type=int)
        if k <= 0:
            k = None
        if format == None:
            format = "json"
        if format != "csv" and format != "json":
            return make_response(format + " is not a suported format.")
        closeArr = []
        for things in db.controls.find({}, {"_id": 0,"km":0,"open":0})[:k]:
             closeArr.append(things)
        if format == "json":
            closeJson = {}
            for x in range(len(closeArr)):
                closeJson[x + 1] = closeArr[x]
            return closeJson
        if format == "csv":
            if len(closeArr) == 0:
                return ""
            head = list(closeArr[0].keys())
            values = ""
            for things in closeArr:
                values = values + ','.join(list(things.values()))
                values = values + "\n"
            return (",".join(head) + "\n" + values[:-1])

class test(Resource):
    def get(self):
        x = {
            "1": {
                "closes": "01 / 01 / 21 01: 01",
                "open": "01/01/21 00:01",
                "close": "01/01/21 01:01"
            },
            "2": {
                "open": "01/01/21 00:01",
                "close": "01/01/21 01:01"
            },
            "3": {
                "open": "01/01/21 03:01",
                "close": "01/01/21 08:01"
            },
            "4": {
                "open": "01/01/21 05:01",
                "close": "01/01/21 13:01"
            },
            "5": {
                "open": "01/01/21 05:01",
                "close": "01/01/21 13:01"
            }
        }
        return x


# Create routes
# Another way, without decorators
api.add_resource(test, '/test')
api.add_resource(listAll, '/listAll/<string:format>', '/listAll', '/listAll/')
api.add_resource(listOpenOnly, '/listOpenOnly/<string:format>', '/listOpenOnly','/listOpenOnly/')
api.add_resource(listCloseOnly, '/listCloseOnly/<string:format>', '/listCloseOnly','/listCloseOnly/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
