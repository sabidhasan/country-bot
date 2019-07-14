import json
import time
import datetime
from flask import Blueprint, request, abort, render_template, Response, jsonify
from training_writer import TrainingWriter
from models import Training

def routes_blueprint_creator(car):
  """
    Sets up a blueprint for importing routes. car is an instance of the Car object
    db is an instance of the SQLAlchemy class created in app.py
    Blueprint allows refactoring routes into its own module.
  """
  routes = Blueprint('routes', __name__)
  # Training writer keeps track of whether we are in free-drive mode or
  # training mode (and if so, records the training to database)
  training_writer = TrainingWriter()

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
    car_move_methods = { 'f': car.go_straight, 'l': car.go_left, 'r': car.go_right }

    requested_params = list(request.args.keys())
    if len(requested_params) != 1:
      return abort(400)
    
    try:
      move_function = car_move_methods[requested_params[0]]
    except KeyError:
      # Requested direction is invalid
      return abort(400)
    
    try:
      written_in_db = training_writer.record_training_if_active(car=car, direction=requested_params[0])
    except:
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
    training_writer.set_active()
    return json.dumps({ 'training': training_writer.active })

  @routes.route('/training')
  def training():
    """
      Gets training data from training database, of requested index <int>
      if query paramater `full=true`, then gets jpeg of histogram too.
    """
    count = Training.query.count()
    if not 'index' in request.args:
      # Return generic count of how many data points exist
      response = jsonify({ 'count': count })
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response
    else:
      # Return data of requested training point
      tr_pnt = Training.query.get(request.args['index'])

      if tr_pnt is None:
        training_data = {}
      else:
        move_names = { 0: 'F', 1: 'R', 2: 'L' }
        image = tr_pnt.image_data

        training_data = {
          'count': count,
          'index': tr_pnt.index,
          'created': (tr_pnt.created - datetime.datetime(1970,1,1)).total_seconds(),
          'image_jpeg': str(image.tobase64())[2:-1],
          'image_height': image.height,
          'image_width': image.width,
          'histogram': json.dumps(image.histogram(luminescence_threshold=0.6,output='numpy').tolist()),
          'ultrasonic': tr_pnt.ultrasonic,
          'move': move_names[[tr_pnt.cmd_forward, tr_pnt.cmd_right, tr_pnt.cmd_left].index(1)],
          'moves': tr_pnt.moves
        }

      if request.args.get('full', None) == 'true':
        histogram_b64 = image.histogram(luminescence_threshold=0.6,output='base64')
        # Convert bytes object to string and remove b" string at beginning, and " @ end
        training_data['histogram_jpeg'] = str(histogram_b64)[2:-1]
      response = jsonify(training_data)
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response

  return routes
