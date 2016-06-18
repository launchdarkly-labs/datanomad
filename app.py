import os
import sys
import time
import logging
from copy import copy
from flask import Flask, render_template, url_for, request, jsonify
from flask_socketio import SocketIO, emit
from pyformance import time_calls, global_registry
from pyformance.reporters.reporter import Reporter
from pyformance.reporters import ConsoleReporter
from metrics import WebsocketReporter
from events import save_event, get_event_by_id
from events import mongo_events
import json

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ
socketio = SocketIO(app)
mongo_events.initialize('mongodb://127.0.0.1:27017/')
ld_logger = logging.getLogger('ldclient')
ld_logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ld_logger.addHandler(ch)

metrics_reporter = WebsocketReporter(registry=global_registry(), socketio=socketio, reporting_interval=1)
metrics_reporter.start()
# console_reporter = ConsoleReporter(registry=global_registry(), reporting_interval=5)
# console_reporter.start()

@app.route('/', methods=['GET'])
@time_calls
def dashboard():
  return render_template('dashboard.html')

@app.route('/events', methods=['POST'])
@time_calls
def events():
  content = request.get_json()
  if content is None:
    return '', 400
  evt = save_event(content)
  ret = event_rep(evt)
  return jsonify(**ret), 201

@app.route('/events/<user_key>/<id>', methods=['GET'])
@time_calls
def get_event(user_key, id):
  evt = get_event_by_id(user_key, id)
  if evt is None:
    return '', 404
  else:
    ret = event_rep(evt)
    return jsonify(**ret)

@socketio.on('connect', namespace='/metrics')
def metrics_listner():
  """Sends outgoing chat messages, via `ChatBackend`."""
  # metrics_reporter.register()
  pass


@socketio.on('disconnect', namespace='/metrics')
def test_disconnect():
    print('Client disconnected')


def event_rep(evt):
  ret = copy(evt)
  evt_id = evt.get('_id')
  if '_id' in ret:
    del ret['_id']
  links = {
    'self': url_for('get_event', id=evt_id, user_key=ret['user']['key'])
  }
  ret['_links'] = links
  return ret

if __name__ == '__main__':
  socketio.run(app)
