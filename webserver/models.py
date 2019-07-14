import datetime
from dbconfig import db

class Training(db.Model):
  index = db.Column(db.Integer, primary_key=True)
  created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  # ImageData object of the image
  image_data = db.Column(db.PickleType, nullable=False)
  # Distance sensor reading
  ultrasonic = db.Column(db.Float, nullable=False, default=0)
  # Boolean of what command was issued at this input
  cmd_forward = db.Column(db.Boolean, default=False)
  cmd_right = db.Column(db.Boolean, default=False)
  cmd_left = db.Column(db.Boolean, default=False)
  # What was the move number for this command (reset when server restarted)
  moves = db.Column(db.Integer)
  # whether this data was human-acquired, or faked
  real_data = db.Column(db.Boolean, default=True)