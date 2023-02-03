import time

import uuid
import tornado.ioloop
import collections

from phonon import get_logger, PHONON_NAMESPACE
import phonon.client
import phonon.event


logger = get_logger(__name__)
connection = None


def get_ms():
    return int(time.time() * 1000.)


def s_to_ms(s):
    return int(s * 1000.)


class AsyncConn(phonon.event.EventMixin):

    HEARTBEAT_INTERVAL = 30  # Seconds
    HEARTBEAT_KEY = f'{PHONON_NAMESPACE}.heartbeat'.encode('utf8')
    PROCESS_TTL = phonon.TTL * 0.5

    def __init__(self, redis_hosts, port=6379, db=1, ioloop=None):
        super(AsyncConn, self).__init__()

        self.id = str(uuid.uuid4()).encode('utf8')

        self.client = phonon.client.ShardedClient(
            hosts=redis_hosts, port=port, db=db)
        self.client.ping()
        self.trigger(phonon.event.CONNECTED)

        self.ioloop = ioloop
        if ioloop is None:
            self.ioloop = tornado.ioloop.IOLoop.current()

        self.heart = tornado.ioloop.PeriodicCallback(
            self.send_heartbeat,
            callback_time=s_to_ms(self.HEARTBEAT_INTERVAL),
            io_loop=self.ioloop
        )
        self.registry_key = self.get_registry_key(self.id)
        self.local_registry = set()

        self.heart.start()
        self.ioloop.add_callback(self.send_heartbeat)

    def get_registry_key(self, id):
        return f"{PHONON_NAMESPACE}_{id}.registry".encode('utf8')

    def send_heartbeat(self):
        self.client.hset(self.HEARTBEAT_KEY, self.id, get_ms())
        self.recover_failed_processes()
        self.trigger(phonon.event.HEARTBEAT)

    def get_registry(self):
        return self.client.smembers(self.registry_key)

    def add_to_registry(self, member, registry_key=None):
        self.local_registry.add(member)
        return self.client.sadd(registry_key or self.registry_key, member)

    def remove_from_registry(self, member):
        if member in self.local_registry:  # force_expiry can cause this to be called twice.
            self.local_registry.remove(member)
        return self.client.srem(self.registry_key, member)

    def move_n_to_new_registry(self, old_registry, new_registry, n=0):
        if not n:
            return
        members = self.client.srandmember(old_registry, n)
        for member in members:
            self.client.sadd(new_registry, member)
            self.client.srem(old_registry, member)

    def list_failed_and_active_pids(self):
        failed = set()
        active = set()
        for pid, heartbeat_time in list(self.client.hgetall(self.HEARTBEAT_KEY).items()):
            if int(heartbeat_time) <= get_ms() - s_to_ms(3 * self.HEARTBEAT_INTERVAL):
                failed.add(pid)
            else:
                active.add(pid)
        return failed, active

    def recover_failed_processes(self):
        failed, active = self.list_failed_and_active_pids()
        if failed:
            logger.warning("Recovering {} failed processes!".format(len(failed)))

        for failed_pid in failed:
            registry_key = self.get_registry_key(failed_pid)
            if failed_pid == self.id:
                self.id = str(uuid.uuid4())
                self.registry_key = self.get_registry_key(self.id)
            elif active:
                orphan_count = self.client.scard(registry_key)
                claim_count = int(orphan_count / len(active)) or 1
                self.move_n_to_new_registry(registry_key, self.registry_key, claim_count)
                if claim_count == orphan_count:
                    self.client.hdel(self.HEARTBEAT_KEY, failed_pid)
            else:
                logger.error("There are no active processes to recover failed processes.")

    def close(self):
        self.heart.stop()
        self.client.hdel(self.HEARTBEAT_KEY, self.id)
        self.local_registry = set()


def connect(hosts=None, port=6379, db=1):
    global connection
    if connection is None:
        connection = AsyncConn(redis_hosts=hosts, port=port, db=db, ioloop=None)
    else:
        logger.warning("Connection already exists. Ignoring input parameters.")
    return connection
