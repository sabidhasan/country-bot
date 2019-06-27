from flask import Blueprint, request, abort, render_template
import json
import time

def routes_blueprint_creator(car):
  routes = Blueprint('routes', __name__)

  car_sensor_methods = {
    'cam': car.get_image,
    'dist': car.get_distance,
    'moving': car.currently_moving,
    'odom': car.get_distance_travelled,
    'moves': car.get_moves
  }
  car_move_methods = {
    's': car.go_straight,
    'l': car.go_left,
    'r': car.go_right,
  }

  @routes.route('/data', methods=['GET'])
  def sensors():
    # This method returns JSON with latest camera, ultra sonic distance, moves, and distance travelled
    
    response = {'id': id(car)}
    # Loop through requested parameters, and gather data
    for param in request.args.keys():
      if not param in car_sensor_methods: 
        continue
      try:
        response[param] = car_sensor_methods[param]()
      except:
        abort(500)
    # We need to stringify distance, as Infinity is not a valid JSON keyword
    if 'dist' in response:
      response['dist'] = str(response['dist'])
    return json.dumps(response)


  @routes.route('/move', methods=['GET'])
  def move():
    # Moves car in R/L/F direction
    requested_params = list(request.args.keys())
    if len(requested_params) != 1:
      return abort(400)
    
    try:
      move_function = car_move_methods[requested_params[0]]
      success = move_function()
    except KeyError:
      # Requested direction is invalid
      return abort(400)
    
    if success == False:
      return abort(500)

    return json.dumps({
      'success': success,
      'time': time.time(),
      'id': id(car)
    })


  @routes.route('/*', methods=['GET'])
  def index():
    return render_template('index.html')

  return routes




