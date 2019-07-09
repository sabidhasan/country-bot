import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Training(db.Model):
  index = db.Column(db.Integer, primary_key=True)
  created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  image_jpeg = db.Column(db.LargeBinary, nullable=False)
  image_np = db.Column(db.PickleType, nullable=False)
  ultrasonic = db.Column(db.Float, nullable=False, default=0)
  cmd_forward = db.Column(db.Boolean, default=False)
  cmd_right = db.Column(db.Boolean, default=False)
  cmd_left = db.Column(db.Boolean, default=False)
  moves = db.Column(db.Integer)