from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from alchemy import EventRegistration, event, Notifications
from sqlalchemy import or_, and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskdb'
db = SQLAlchemy(app)



## Get user's registered event's details
@app.route('/user/registeredEvents', methods=['GET'])
## eg /user/registeredEvents?id=AAKPYC1TV
def getUserRegisteredEvents():

  pecfestId = request.args['id']
  #############################################################################################
  # get the user's registered events using eventregistrations where memberId = user's pecfestId or leaderId = user's pecfestId
  # Eventregistration.eventId_relation is the relation between the foreign key of Event registration and primary key 'eventId' of Event
  # and is defined in /models/event_registration.py
  
  events = db.session.query(Event).\
  join(EventRegistration.eventId_relation).\
  filter(or_(EventRegistration.memberId == pecfestId , EventRegistration.leaderId == pecfestId)).all()
  
  #### Also try :- 
  '''events = db.session.query(Event).\
  filter(or_(EventRegistration.memberId == pecfestId , EventRegistration.leaderId == pecfestId)).\
  join(EventRegistration.eventId_relation).all()'''

  registeredEvents = []      ## a list of dicts, each entry of the list stores information of the registered event

  for i in range(0, len(events)):
    events_dict = {}
    events_dict["name"] = events[i].eventName
    events_dict["day"] = events[i].day
    events_dict["venue"] = events[i].location
    events_dict["time"] = events[i].time
    registeredEvents += [events_dict]

  return jsonify(registeredEvents)




@app.route('/user/notifications', method=['GET'])
## eg /user/notifications?id=AAKPYC1TV
def getUserNotifications():

  pecfestId = request.args['id']
  #################################################################################################
  ## get the notifications pertaining to user's registered events using Notifications and EventRegistration table 
  ## filtered by memberId = user's pecfestId or leaderId = user's pecfestId

  ## notif_ rel is the relation between the foreign key 'Notifications.eventId' and primary key 'eventId' of Event
  ## This has been used to get the name of the event using the eventId in notifications

  notifs = db.session.query(Notifications, event).\
  join(EventRegistration, Notifications.eventId == EventRegistration.eventId).\
  join(Notifications.notif_rel).\
  filter(or_(EventRegistration.memberId == pecfestId , EventRegistration.leaderId == pecfestId)).\
  all()

  ## Also try
  '''notifs = db.session.query(Notifications, event).\
  filter(or_(EventRegistration.memberId == pecfestId , EventRegistration.leaderId == pecfestId)).\
  join(EventRegistration, Notifications.eventId == EventRegistration.eventId).\
  join(Notifications.notif_rel).\
  all()'''

  user_notifications = []         ## a list of dicts, each entry of the list stores notification of a registered event

  for i in range(0, len(notifs)):
    notif_dict = {}
    notif_dict["eventName"] = notifs[i][1].eventName
    notif_dict["notificationTitle"] = notifs[i][0].notificationTitle
    notif_dict["notificationDetails"] = notifs[i][0].notificationDetails
    user_notifications += [notif_dict]
  
  return jsonify(user_notifications)
