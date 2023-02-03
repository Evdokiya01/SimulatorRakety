import unittest
import unittest.mock as mock

from phonon.client import ShardedClient


class TestShardedClient(unittest.TestCase):

    def setUp(self):
        self.client = ShardedClient(hosts=['localhost1', 'localhost2'])

    def test_route(self):
        assert self.client.route(b'd') is self.client.clients[0]
        assert self.client.route(b'b') is self.client.clients[1]

    def test_correct_client_get_called(self):
        for client in self.client.clients:
            client.get = mock.MagicMock()

        assert self.client.clients[0].get.called is False
        assert self.client.clients[1].get.called is False

        self.client.get(b'4')
        assert self.client.clients[0].get.called is True
        assert self.client.clients[1].get.called is False

        self.client.get(b'1')
        assert self.client.clients[0].get.called is True
        assert self.client.clients[1].get.called is True

    def test_flushall_called_everywhere(self):
        for client in self.client.clients:
            client.flushall = mock.MagicMock()

        for client in self.client.clients:
            assert client.flushall.called is False

        self.client.flushall()

        for client in self.client.clients:
            assert client.flushall.called is True

    def test_flushdb_called_everywhere(self):
        for client in self.client.clients:
            client.flushdb = mock.MagicMock()

        for client in self.client.clients:
            assert client.flushdb.called is False

        self.client.flushdb()

        for client in self.client.clients:
            assert client.flushdb.called is True
