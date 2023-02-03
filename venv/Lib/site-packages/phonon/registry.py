import sys
import collections
import tornado


class Registry(object):

    def __init__(self, max_entries=10000, ioloop=None):
        self.models = collections.OrderedDict()
        self.timeouts = {}
        self.ioloop = ioloop or tornado.ioloop.IOLoop.current()
        self.max_entries = max_entries

    def register(self, model, *args, **kwargs):
        if model.registry_key() in self.models:
            self.models[model.registry_key()].merge(model)
            self.ioloop.remove_timeout(self.timeouts[model.registry_key()])
        else:
            self.models[model.registry_key()] = model

        self.timeouts[model.registry_key()] = self.ioloop.add_timeout(
            model.TTL, self.on_expire, model, *args, **kwargs
        )

    def on_expire(self, model, *args, **kwargs):
        del self.models[model.registry_key()]
        del self.timeouts[model.registry_key()]

        if not model.reference.dereference(callback=model.on_complete,
                                           args=args,
                                           kwargs=kwargs):
            model.cache()


registry = Registry()


def configure(max_entries=10000):
    global registry
    registry = Registry(max_entries=max_entries)


def register(model):
    registry.register(model)
