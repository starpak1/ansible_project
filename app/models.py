from datetime import datetime
from app import db
from flask import jsonify
from sqlalchemy import inspect

from datetime import datetime

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description = db.Column(db.String(140))
    state = db.Column(db.String(140))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return '<Events {}>'.format(self.username)

    def addEvent(data):
        event = Events(
            name = data['name'],
            date = datetime.utcnow(),
            description = data['description'],
            state = data['state']
        )
        db.session.add(event)
        success=True
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            success=False
        return success

    def delEventByName(name):
        event = Events.query.filter(Events.name == name).first()
        success=True
        try:
            db.session.delete(event)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            success=False
        return success

    def getEvents():
        events = Events.query.all()
        eventsArr = []
        for event in events:
            eventsArr.append(event.toDict()) 
        return jsonify(eventsArr)

    def getEventByName(name):
        event = Events.query.filter(Events.name == name).first()
        if event != None:
            return jsonify(event.toDict())
        return False