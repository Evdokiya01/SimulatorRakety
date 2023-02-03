import unittest
import unittest.mock as mock
import datetime
import time
import logging
import uuid

import tornado.ioloop

import phonon
import phonon.event
import phonon.connections
import phonon.reference
import phonon.lock

logging.disable(logging.CRITICAL)


def get_milliseconds_timestamp():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


class ProcessTest(unittest.TestCase):

    def setUp(self):
        phonon.connections.connect(hosts=['localhost'])
        phonon.connections.connection.client.flushall()
        phonon.connections.connection = None

    def tearDown(self):
        phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 30
        if phonon.connections.connection is not None:
            phonon.connections.connection.client.flushall()

    def test_connect_establishes_connection_once(self):
        conn = phonon.connections.connect(hosts=['localhost'])
        assert phonon.connections.connect(hosts=['localhost']) is phonon.connections.connection
        assert phonon.connections.connection is conn

    def test_init_ignores_differing_connection_setting(self):
        conn1 = phonon.connections.connect(hosts=['localhost'])
        conn2 = phonon.connections.connect(hosts=['notlocalhost'])

        assert conn1 is conn2

    def test_init_create_heartbeat_data(self):
        phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
        conn = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        conn.on(phonon.event.HEARTBEAT, lambda: tornado.ioloop.IOLoop.current().stop())

        tornado.ioloop.IOLoop.current().start()

        heartbeat = conn.client.hgetall(conn.HEARTBEAT_KEY)
        assert conn.id in heartbeat
        time.sleep(0.001)
        observed = heartbeat[conn.id]
        should_be_greater = phonon.get_ms()
        assert int(observed) < int(should_be_greater), "{} is (unexpectedly) >= {}".format(observed, should_be_greater)

    def test_heartbeat_updates(self):
        try:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
            phonon.connections.connection = None

            def on_heartbeat():
                tornado.ioloop.IOLoop.current().stop()

            conn = phonon.connections.connect(hosts=['localhost'])
            conn.on(phonon.event.HEARTBEAT, on_heartbeat)
            tornado.ioloop.IOLoop.current().start()

            current_time = conn.client.hget(conn.HEARTBEAT_KEY, conn.id)
            time.sleep(0.2)

            tornado.ioloop.IOLoop.current().add_callback(conn.send_heartbeat)
            tornado.ioloop.IOLoop.current().start()

            new_time = conn.client.hget(conn.HEARTBEAT_KEY, conn.id)

            assert int(new_time) >= int(current_time) + (conn.HEARTBEAT_INTERVAL * 1000)
        finally:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 30
            conn.close()

    def test_multiple_heartbeats_update(self):
        phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
        conn1 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        conn2 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
        try:
            def on_heartbeat():
                tornado.ioloop.IOLoop.current().stop()

            conn2.on(phonon.event.HEARTBEAT, lambda: tornado.ioloop.IOLoop.current().stop())
            tornado.ioloop.IOLoop.current().start()

            current_time_1 = conn1.client.hget(conn1.HEARTBEAT_KEY, conn1.id)
            current_time_2 = conn2.client.hget(conn2.HEARTBEAT_KEY, conn2.id)

            time.sleep(0.3)

            tornado.ioloop.IOLoop.current().start()
            new_time_1 = conn1.client.hget(conn1.HEARTBEAT_KEY, conn1.id)
            new_time_2 = conn2.client.hget(conn2.HEARTBEAT_KEY, conn2.id)

            assert int(new_time_1) >= int(current_time_1) + (conn1.HEARTBEAT_INTERVAL * 1000)
            assert int(new_time_2) >= int(current_time_2) + (conn2.HEARTBEAT_INTERVAL * 1000)
        finally:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 30
            conn1.close()
            conn2.close()

    @mock.patch('time.time', side_effect=get_milliseconds_timestamp)
    def test_stop_cleans_up(self, time_time_patched):
        try:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
            conn1 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
            conn2 = phonon.connections.AsyncConn(redis_hosts=['localhost'])

            current_time_1 = conn1.client.hget(conn1.HEARTBEAT_KEY, conn1.id)
            conn1.close()
            time.sleep(.5)
            new_time_2 = conn1.client.hget(conn1.HEARTBEAT_KEY, conn1.id)
            assert new_time_2 == current_time_1
            conn2.close()
        finally:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 30

    def test_process_registry_tracks_references(self):
        conn = phonon.connections.connect(hosts=['localhost'])
        ref = phonon.reference.Reference(b"foo")

        assert conn.client.sismember(conn.registry_key, ref.resource_key)

        ref.dereference()

        assert conn.client.sismember(conn.registry_key, ref.resource_key) is False
        conn.close()

    def test_lock_wrapper(self):
        phonon.connections.connect(hosts=['localhost'])
        with phonon.lock.Lock("foo") as acquired_lock:
            phonon.connections.connection = phonon.connections.AsyncConn(redis_hosts=['localhost'])
            with self.assertRaisesRegex(phonon.exceptions.AlreadyLocked, "Already locked"):
                with phonon.lock.Lock("foo") as lock2:
                    pass

    def test_remove_from_registry(self):
        conn = phonon.connections.connect(hosts=['localhost'])
        assert len(conn.get_registry()) == 0

        ref = phonon.reference.Reference(b"test")
        assert len(conn.get_registry()) == 1

        conn.remove_from_registry(b"test")
        assert len(conn.get_registry()) == 0

    def test_process_recovery(self):
        try:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
            conn1 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
            conn1.heart.stop()
            conn1.send_heartbeat()

            assert len(conn1.get_registry()) == 0

            dead_process_registry = conn1.get_registry_key(b"12345")
            conn1.add_to_registry(b"r1", dead_process_registry)
            conn1.add_to_registry(b"r2", dead_process_registry)
            conn1.client.hset(conn1.HEARTBEAT_KEY, b"12345", 0)

            conn1.recover_failed_processes()

            assert len(conn1.get_registry()) == 2
            assert b"12345" not in conn1.client.hgetall(conn1.HEARTBEAT_KEY), conn1.client.hgetall(conn1.HEARTBEAT_KEY)

            phonon.connections.connection = conn1
            ref = phonon.reference.Reference(b"r1")
            ref_list = ref.nodelist.get_all_nodes()
            assert b"12345" not in ref_list
            assert conn1.id in ref_list

            ref = phonon.reference.Reference(b"r2")
            ref_list = ref.nodelist.get_all_nodes()
            assert b"12345" not in ref_list
            assert conn1.id in ref_list
        finally:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 30
            conn1.close()

    def test_process_self_recovery(self):
        try:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
            conn1 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
            phonon.connections.connection = conn1

            ref = phonon.reference.Reference(b"test")
            conn1.heart.stop()

            original_id = conn1.id
            conn1.client.hset(conn1.HEARTBEAT_KEY, original_id, int(int(time.time()) - 6 * conn1.HEARTBEAT_INTERVAL))

            conn1.recover_failed_processes()

            assert conn1.id != original_id
            assert len(conn1.get_registry()) == 0

            conn1.send_heartbeat()

            assert len(conn1.get_registry()) == 1
        finally:
            conn1.close()

    def test_no_active_process(self):
        try:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
            conn1 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
            phonon.connections.connection = conn1

            ref = phonon.reference.Reference(b"test")
            conn1.heart.stop()

            original_id = conn1.id
            conn1.client.hset(conn1.HEARTBEAT_KEY, conn1.id, int(int(time.time()) - 6 * conn1.HEARTBEAT_INTERVAL))

            conn1.id = str(uuid.uuid4()).encode('utf8')
            conn1.recover_failed_processes()

            assert original_id in conn1.client.hgetall(conn1.HEARTBEAT_KEY)

            # Proces comes back alive
            conn1.id = original_id
            conn1.recover_failed_processes()
            conn1.send_heartbeat()

            assert original_id not in conn1.client.hgetall(conn1.HEARTBEAT_KEY)
        finally:
            conn1.close()

    def test_failed_process_locked(self):
        try:
            phonon.connections.AsyncConn.HEARTBEAT_INTERVAL = 0.1
            conn1 = phonon.connections.AsyncConn(redis_hosts=['localhost'])
            phonon.connections.connection = conn1

            assert len(conn1.get_registry()) == 0

            dead_process_registry = conn1.get_registry_key(b"12345")
            conn1.add_to_registry(b"r1", dead_process_registry)
            conn1.add_to_registry(b"r2", dead_process_registry)
            conn1.client.hset(conn1.HEARTBEAT_KEY, b"12345", int(int(time.time()) - 6 * conn1.HEARTBEAT_INTERVAL))

            with phonon.lock.Lock(conn1.get_registry_key(b"12345")):
                conn1.recover_failed_processes()
        finally:
            conn1.close()
