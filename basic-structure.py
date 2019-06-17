from flask import Flask, jsonify
import time
app = Flask(__name__)

class B(object):
  def __init__(self):
    self.i = 0
    print ('initing')
    
  def do_blocking(self):
    for k in range(4):
      time.sleep(1)
      self.i = k

x = B()

@app.route('/')
def hello_world():
    x.do_blocking()
    return 'Hello, World!'


@app.route('/l')
def l():
  return jsonify(i = x.i)