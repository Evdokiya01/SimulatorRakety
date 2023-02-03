import unittest

import tornado.ioloop

import phonon.model
import phonon.registry
import phonon.connections


class TestRegistry(unittest.TestCase):

    def setUp(self):
        self.conn = phonon.connections.connect(hosts=['localhost'])
        self.conn.client.flushall()

    def test_registry_stores_new_models(self):
        class Bar(phonon.model.Model):
            pass
        model = Bar(id=b'1')
        phonon.registry.register(model)
        assert phonon.registry.registry.models[b'Bar.1'] is model

    def test_registry_stores_timeout(self):
        class Bar(phonon.model.Model):
            pass
        model = Bar(id=b'1')
        phonon.registry.register(model)
        assert isinstance(phonon.registry.registry.timeouts[b'Bar.1'], tornado.ioloop._Timeout)

    def test_on_expire_gets_called_as_well_as_dereference(self):
        class DerefTest(phonon.model.Model):
            TTL = 0.1

            def __init__(self, *args, **kwargs):
                class Reference(object):

                    def __init__(self):
                        self.called = False

                    def dereference(self, *args, **kwargs):
                        tornado.ioloop.IOLoop.current().stop()
                        self.called = True

                super(DerefTest, self).__init__(*args, **kwargs)
                self.reference = Reference()
                self.completed = False
        model = DerefTest(id=b'1')
        phonon.registry.register(model)
        tornado.ioloop.IOLoop.current().start()
        assert model.reference.called

    def test_on_complete_gets_called(self):
        class OnCompleteTest(phonon.model.Model):
            TTL = 0.1

            def __init__(self, *args, **kwargs):
                super(OnCompleteTest, self).__init__(*args, **kwargs)
                self.completed = False

            def on_complete(self):
                self.completed = True
                tornado.ioloop.IOLoop.current().stop()

        model = OnCompleteTest(id=b'1')
        phonon.registry.register(model)
        tornado.ioloop.IOLoop.current().start()
        assert model.completed

    def test_configure_sets_max_entries(self):
        phonon.registry.configure(max_entries=12)
        assert phonon.registry.registry.max_entries == 12
