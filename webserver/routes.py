from flask import Blueprint, request, abort, render_template, Response
import json
import time
from training_writer import TrainingWriter


def routes_blueprint_creator(car, db):
  """
    Sets up a blueprint for importing routes. car is an instance of the Car object
    db is an instance of the SQLAlchemy class created in app.py
    Blueprint allows refactoring routes into its own module.
  """
  routes = Blueprint('routes', __name__)
  # Training writer keeps track of whether we are in free-drive mode or
  # training mode (and if so, records the training to database)
  training_writer = TrainingWriter(db)

  def latest_image_generator(camera):
    """ Generator that yields the latest data from the camera """
    while True:
      frame = camera.get_frame()
      # Infinite loop generator is meant for consumption by Response
      yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

  @routes.route('/data', methods=['GET'])
  def sensors():
    """
      Returns JSON with ultrasonic distance, still image, move count and odometer data,
      as per requests
    """
    # Params for /data endpoint
    car_sensor_methods = {
      # Latest still image, ultrasonic distance, odometer, and move counter
      'pict': car.get_image,
      'dist': car.get_distance,
      'odom': car.get_distance_travelled,
      'move': car.get_moves
    }
    # Include basic information about the car
    response = { 'id': id(car), 'created': car.created }

    for param in request.args.keys():
      if not param in car_sensor_methods: 
        continue
      try:
        response[param] = str(car_sensor_methods[param]())
      except:
        abort(500)
    return json.dumps(response)

  @routes.route('/camera')
  def camera():
    """
      Returns a live MJPEG feed of the car camera. Insert as 'src' for a <img> to consume
      Code adapted from https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
    """
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    return Response(latest_image_generator(car.camera.start_thread()), mimetype=mimetype)

  @routes.route('/move', methods=['GET'])
  def move():
    """
      Moves the car in the forward, right and left directions, as requested
    """
    car_move_methods = {
      'f': car.go_straight,
      'l': car.go_left,
      'r': car.go_right,
    }

    requested_params = list(request.args.keys())
    if len(requested_params) != 1:
      return abort(400)
    
    try:
      move_function = car_move_methods[requested_params[0]]
    except KeyError:
      # Requested direction is invalid
      return abort(400)
    
    try:
      training_writer.record_training_if_active(car=car, direction=requested_params[0])
      written_in_db = True
    except:
      # Writing in DB failed
      written_in_db = False

    # Move the car
    move_function()

    return json.dumps({
      'success': True,
      'time': time.time(),
      'id': id(car),
      'written_in_db': written_in_db,
    })

  @routes.route('/enable_training')
  def enable_training():
    """
      This route is activated when 'training' is clicked on front end.
      When called in move route, it writes data to DB if necessary
    """
    expires = time.time() - (training_writer.activated + training_writer.TIMEOUT)
    training_writer.set_active()
    return json.dumps({ 'training': training_writer.active, 'expires': expires })

  return routes
