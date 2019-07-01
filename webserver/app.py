from flask import Flask, send_from_directory, render_template
# Allow importing parent module
import sys
sys.path.append('..')

from routes import routes_blueprint_creator
from routes_static import static_blueprint_creator
from helpers.os import set_environ

if len(sys.argv) > 1 and sys.argv[1].upper() == "DEV=1":
  set_environ('TESTING')

from hardware import car, engine

engine = engine.Engine()
car = car.Car(engine)

# Template folder serves the HTML files. JS and CSS are served from static_routes
app = Flask(__name__, template_folder = "./frontend/dist")

# Register all routes
routes_blueprint = routes_blueprint_creator(car)
static_blueprint = static_blueprint_creator()
app.register_blueprint(routes_blueprint)
app.register_blueprint(static_blueprint)

# Catch all route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)