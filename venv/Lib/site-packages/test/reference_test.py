import unittest
import collections
import time
import redis
import threading

import phonon.connections
import phonon.reference


class ReferenceTest(unittest.TestCase):

    def setUp(self):
        self.client = redis.StrictRedis(host='localhost')
        self.client.flushall()
        self.conn = phonon.connections.connect(['localhost'])
        self.conn.local_registry = set()

    def tearDown(self):
        self.client = redis.StrictRedis(host='localhost')
        self.client.flushall()

    def test_init_creates_keys(self):
        a = phonon.reference.Reference(b'foo')
        assert a.nodelist.nodelist_key == b'phonon_foo.nodelist'
        assert a.resource_key == b'foo'
        assert a.times_modified_key == b'phonon_foo.times_modified'

    def test_lock_is_non_reentrant(self):
        a = phonon.reference.Reference(b'foo')

        with a.lock():
            try:
                lock = None
                with a.lock(block=False) as lock:
                    pass
            except:
                assert lock is None

    def test_lock_acquires_and_releases(self):
        a = phonon.reference.Reference(b'foo')
        with a.lock():
            try:
                lock = None
                with a.lock(block=False) as lock:
                    pass
            except:
                assert lock is None

        with a.lock():
            pass

    def test_nodelist_updates_multinodes(self):

        conns = collections.deque([
            phonon.connections.AsyncConn(redis_hosts=['localhost']),
            phonon.connections.AsyncConn(redis_hosts=['localhost'])
        ])

        def ref():
            conn = conns.popleft()
            phonon.connections.connection = conn
            phonon.reference.Reference(b'foo')
            conns.append(conn)

        t = threading.Thread(target=ref)
        t2 = threading.Thread(target=ref)

        t.start()
        t2.start()

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        a = phonon.reference.Reference(b"foo")

        t.join()
        t2.join()

        nodes = a.nodelist.get_all_nodes()
        while conns:
            conn = conns.popleft()
            assert conn.id in nodes

        assert phonon.connections.connection.id in nodes

    def test_nodelist_dereferences_multinodes(self):
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        a = phonon.reference.Reference(b'foo')
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')

        t = threading.Thread(target=a.dereference)
        t2 = threading.Thread(target=b.dereference)

        t.start()
        t2.start()

        t.join()
        t2.join()

        nodes = a.nodelist.get_all_nodes()
        assert nodes == {}

    def test_refresh_session_sets_time_initially(self):
        a = phonon.reference.Reference(b'foo')
        a.refresh_session()
        nodes = a.nodelist.get_all_nodes()
        assert a.nodelist.count() == 1, "{0}: {1}".format(nodes, len(nodes))
        assert isinstance(a.nodelist.get_last_updated(phonon.connections.connection.id), int)

    def test_refresh_session_resets_time(self):
        a = phonon.reference.Reference(b'foo')
        conn_id = phonon.connections.connection.id
        start = a.nodelist.get_last_updated(conn_id)
        time.sleep(0.01)
        a.refresh_session()
        end = a.nodelist.get_last_updated(conn_id)
        assert end > start
        assert isinstance(end, int)
        assert isinstance(start, int)

    def test_get_and_increment_times_modified(self):
        a = phonon.reference.Reference(b'foo')
        assert a.get_times_modified() == 0
        a.increment_times_modified()
        assert a.get_times_modified() == 1, a.get_times_modified()
        a.increment_times_modified()
        a.increment_times_modified()
        assert a.get_times_modified() == 3
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')
        b.increment_times_modified()
        assert b.get_times_modified() == 4

    def test_count_for_one_reference(self):
        a = phonon.reference.Reference(b'foo')
        assert a.count() == 1, a.count()

    def test_count_for_multiple_references(self):
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        a = phonon.reference.Reference(b'foo')

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        c = phonon.reference.Reference(b'foo')

        assert a.count() == b.count()
        assert b.count() == c.count()
        assert c.count() == 3

    def test_count_decrements_when_dereferenced(self):
        import phonon.connections

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        a = phonon.reference.Reference(b'foo')
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        c = phonon.reference.Reference(b'foo')

        assert a.count() == b.count()
        assert b.count() == c.count()
        assert c.count() == 3, c.count()
        a.dereference()
        assert a.count() == 2, b.count()
        b.dereference()
        assert a.count() == 1, a.count()
        c.dereference()
        assert a.count() == 0, a.nodelist.get_all_nodes()

    def test_dereference_removes_pid_from_pids(self):
        a = phonon.reference.Reference(b'foo')

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')

        pids = a.nodelist.get_all_nodes()
        assert a.conn.id in pids
        assert b.conn.id in pids
        a.dereference()
        pids = a.nodelist.get_all_nodes()
        assert a.conn.id not in pids
        b.dereference()
        pids = a.nodelist.get_all_nodes()
        assert b.conn.id not in pids
        assert len(pids) == 0

    def test_dereference_cleans_up(self):
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        a = phonon.reference.Reference(b'foo')

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')

        conn = phonon.connections.connection

        pids = a.nodelist.get_all_nodes()
        assert a.conn.id in pids
        assert b.conn.id in pids
        a.dereference()
        pids = a.nodelist.get_all_nodes()
        assert a.conn.id not in pids
        b.dereference()
        pids = a.nodelist.get_all_nodes()
        assert b.conn.id not in pids
        assert len(pids) == 0
        assert a.nodelist.get_all_nodes() == {}, a.nodelist.get_all_nodes()
        assert conn.client.get(a.resource_key) is None, conn.client.get(a.resource_key)
        assert conn.client.get(a.times_modified_key) is None, conn.client.get(a.times_modified_key)

    def test_dereference_handles_when_never_modified(self):
        a = phonon.reference.Reference(b'foo')
        pids = a.nodelist.get_all_nodes()
        assert len(pids) == 1, pids

        a.dereference()
        pids = a.nodelist.get_all_nodes()
        assert len(pids) == 0, pids

    def test_dereference_calls_callback(self):
        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        a = phonon.reference.Reference(b'foo')

        phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        b = phonon.reference.Reference(b'foo')
        foo = [1]

        def callback(*args, **kwargs):
            foo.pop()

        b.dereference(callback, args=('first',))
        assert len(foo) == 1
        a.dereference(callback, args=('second',))
        assert len(foo) == 0
