from flask import Flask, send_from_directory, render_template
from dbconfig import database_file, db
from routes import routes_blueprint_creator
from routes_static import static_blueprint_creator

# Allow importing parent module (helpers.os and hardware)
import sys
sys.path.append('..')
from helpers.os import set_environ

if len(sys.argv) > 1 and sys.argv[1].upper() == "DEV=1":
  set_environ('TESTING')

from hardware import car, engine

####################################
####################################

engine = engine.Engine()
car = car.Car(engine)

# Template folder serves the HTML files. JS and CSS are served from static_routes
app = Flask(__name__, template_folder = "./frontend/dist")

# Define db
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db.init_app(app)

# Register all routes (db passed to routes so they can write to it)
routes_blueprint = routes_blueprint_creator(car)
app.register_blueprint(routes_blueprint)

static_blueprint = static_blueprint_creator()
app.register_blueprint(static_blueprint)

# Catch all route for serving Vue app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)