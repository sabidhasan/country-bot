from __init__ import create_app
# For setting env variable for dev mode
from helpers.os import set_environ
if len(sys.argv) > 1 and sys.argv[1].upper() == "DEV=1":
  set_environ('TESTING')

# import hardware.engine as engine
# import hardware.car as car
# engine = engine.Engine()
# car = car.Car(engine)

if __name__ == "__main__":
  app = create_app()
  app.run(host='0.0.0.0', port=4000)