from app import app
from models import db

db.init_app(app)

with app.app_context():
  db.create_all()