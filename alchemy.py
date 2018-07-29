## Database

'''INSERT INTO `registration`(`id`, `eventId`, `memberId`, `leaderId`) VALUES 
(0, 1, 'AAKPYC1ZT', 'AAKPYC1ZT'), 
(1, 2, 'ANISHA23GT' ,'VAGISHA0IK'),
(2, 2, 'AAKPYC1ZT', 'ANISHA23GT'), 
(3, 4, 'ANISHA23GT', 'ANISHA23GT'), 
(4, 4, 'SHAER342IY', 'SHAER3421Y'), 
(5, 4, 'AAKPYC1ZT', 'AAKPYC1ZT')
'''
'''
INSERT INTO Notifications VALUES
('1', 'drum the roll shifted', 'cultDD2', 2, 'Cultural'), 
('2', 'coding the ptyhonfsf', 'techDD', 4, 'Technical'), 
('3', 'Bhangra Stage at main arena', 'cultDD', 1, 'Cultural'), 
('4', 'Event started at the CC', 'cultDD3', 1, 'Cultural');
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class EventRegistration(db.Model):

	__tablename__ = 'registration'

	id = db.Column(db.Integer, primary_key=True)
	eventId = db.Column(db.Integer, db.ForeignKey('event.eventId'), nullable=False)
	memberId = db.Column(db.String(10), nullable=False)
	leaderId = db.Column(db.String(10), nullable=False)

	eventId_relation = relationship("event")


class event(db.Model):
	__tablename__ = 'event'
	eventId = db.Column('eventId', db.Unicode, primary_key=True)
	eventName = db.Column('name', db.Unicode, primary_key=False)


class Notifications(db.Model):
    __tablename__ = 'Notifications'

    notificationId = db.Column(db.String(10), primary_key = True)
    notificationTitle = db.Column(db.String(100), nullable = False)
    notificationDetails = db.Column(db.String(4096), nullable = True)
    eventId = db.Column(db.Integer, db.ForeignKey('event.eventId'), nullable=False)
    notificationType = db.Column(db.String(10), nullable = False)

    notif_rel = relationship('event')
