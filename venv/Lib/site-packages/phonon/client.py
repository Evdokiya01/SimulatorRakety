import redis
import zlib

from phonon import get_logger

logger = get_logger(__name__)

connection = None


class ShardedClient(object):

    def __init__(self, hosts=None, port=6379, db=0):
        self.hosts = sorted(hosts)
        self.clients = [redis.StrictRedis(host=host, port=port, db=db) for host in self.hosts]

    def route(self, key):
        if not isinstance(key, bytes):
            raise TypeError(f'Client expected routing key to be of type bytes. Got {type(key)}.')
        return self.clients[(zlib.crc32(key) & 0xffffffff) % len(self.clients)]

    def __flushall(self):
        return all([client.flushall() for client in self.clients])

    def __flushdb(self):
        return all([client.flushdb() for client in self.clients])

    def __getattr__(self, method):
        if method == 'flushall':
            return self.__flushall
        elif method == 'flushdb':
            return self.__flushdb

        def wrap(*args, **kwargs):
            if not args:
                return [getattr(client, method)(*args, **kwargs) for client in self.clients]

            client = self.route(args[0])
            return getattr(client, method)(*args, **kwargs)

        return wrap

    def using_key(self, key):
        return self.route(key)
