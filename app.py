import os
import time
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from pyformance import time_calls, global_registry
from pyformance.reporters.reporter import Reporter
from pyformance.reporters import ConsoleReporter
from metrics import WebsocketReporter

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ
socketio = SocketIO(app)

metrics_reporter = WebsocketReporter(registry=global_registry(), socketio=socketio)
console_reporter = ConsoleReporter(registry=global_registry(), reporting_interval=5)
metrics_reporter.start()
console_reporter.start()

@app.route('/')
@time_calls
def dashboard():
  time.sleep(0.1)
  print "in here"
  return render_template('dashboard.html')

@socketio.on('connect', namespace='/metrics')
def metrics_listner():
  """Sends outgoing chat messages, via `ChatBackend`."""
  # metrics_reporter.register()
  pass


@socketio.on('disconnect', namespace='/metrics')
def test_disconnect():
    print('Client disconnected')

@time_calls
def test():
  time.sleep(0.1)

for i in range(10):
  test()

if __name__ == '__main__':
  socketio.run(app)