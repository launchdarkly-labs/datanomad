from pyformance.reporters.reporter import Reporter
import json

class WebsocketReporter(Reporter):


  def __init__(self, socketio, registry=None, reporting_interval=5, clock=None):
    super(WebsocketReporter, self).__init__(
      registry, reporting_interval, clock)
    self.clients = list()
    self.socketio = socketio

  def register_client(self, client):
    """Register a websocket listener to recieve metrics updates"""
    self.clients.append(client)

  def report_now(self, registry=None, timestamp=None):
    metrics = self._collect_metrics(registry or self.registry)
    self.socketio.emit('metrics', metrics, namespace='/metrics')

  def _collect_metrics(self, registry):
    return registry.dump_metrics()