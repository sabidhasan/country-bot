from flask import Blueprint, send_from_directory

def static_blueprint_creator():
  """
    Sets blueprint for static resources' routes
  """
  static = Blueprint('static', __name__)

  @static.route('/js/<path:path>')
  def send_js(path):
    return send_from_directory('frontend/dist/js', path)

  @static.route('/css/<path:path>')
  def send_css(path):
    return send_from_directory('frontend/dist/css', path)

  return static
