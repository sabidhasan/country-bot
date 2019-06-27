from flask import Flask
# Allow importing parent module
import sys
sys.path.append('..')

from app.routes import routes_blueprint_creator
from helpers.os import set_environ

if len(sys.argv) > 1 and sys.argv[1].upper() == "DEV=1":
  set_environ('TESTING')

from hardware import car, engine
engine = engine.Engine()
car = car.Car(engine)

app = Flask(__name__)

# Register all routes
routes_blueprint = routes_blueprint_creator(car)
app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)