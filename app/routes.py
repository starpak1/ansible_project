from app import app
from flask import request, jsonify
from app.models import Events
from app.validators import EventsValidator

import json

@app.route('/events', methods=['GET'])
def getAllEvents():
    return Events.getEvents()
        
@app.route('/events', methods=['POST'])
def addEvent():
    data = request.json
    if EventsValidator.validateAddEvent(data):
        result = Events.addEvent(data)
        if result:
            return jsonify({"status":"success", "message":"record added"})
    return jsonify({"status":"error", "message":"wrong data send"})

@app.route('/events/<name>', methods=['GET'])
def getEvent(name):
    if EventsValidator.validateGetEvent(name):
        result = Events.getEventByName(name)
        if result:
            return result
    return jsonify({"status":"error", "message":"wrong data send"})

@app.route('/events/<name>', methods=['DELETE'])
def delEvent(name):
    if EventsValidator.validateGetEvent(name):
        result = Events.delEventByName(name)
        if result:
            return jsonify({"status":"success", "message":"records was deleted"})
    return jsonify({"status":"error", "message":"wrong data send"})


        