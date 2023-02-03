import collections

"""
Event definitions
"""
# For the phonon.connections.AsyncConn
HEARTBEAT = 1
CONNECTED = 2


class EventMixin(object):

    def __init__(self):
        self.__listeners = collections.defaultdict(list)

    def on(self, name, callback):
        assert callback not in self.__listeners[name], "Duplicate listener"
        self.__listeners[name].append(callback)

    def trigger(self, name, *args, **kwargs):
        for callback in self.__listeners[name]:
            callback(*args, **kwargs)
