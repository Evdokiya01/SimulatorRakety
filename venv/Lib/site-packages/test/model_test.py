import unittest

import phonon.exceptions
import phonon.connections
import phonon.model
import phonon.fields




class ModelTest(unittest.TestCase):

    def setUp(self):
        if phonon.connections.connection:
            phonon.connections.connection.client.flushall()
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        self.conn = phonon.connections.connection

    def test_init(self):
        class BizBar(phonon.model.Model):
            id = phonon.fields.ID()
            a = phonon.fields.Sum()

        foo = BizBar(id=b'1', a=5)

        assert foo.id == b'1', foo.id
        assert foo.a == 5, foo.a

        with self.assertRaisesRegex(phonon.exceptions.ArgumentError, "id is a required field"):
            c = BizBar(a=6)

    def test_merge(self):
        class BizBar(phonon.model.Model):
            id = phonon.fields.ID()
            a = phonon.fields.Sum()

        a = BizBar(id=b'1', a=5)
        b = BizBar(id=b'1', a=3)
        a.merge(b)

        assert a.id == b'1'
        assert a.a == 8

    def test_cache(self):
        class BizBar(phonon.model.Model):
            id = phonon.fields.ID()
            a = phonon.fields.Sum()
        a = BizBar(id=b'1', a=5)
        a.cache()

        cached_value = self.conn.client.get(b'BizBar.1.a')
        assert cached_value == b'5', cached_value
