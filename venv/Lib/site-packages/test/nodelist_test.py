import unittest
import time
import logging

from phonon import TTL
from phonon.nodelist import Nodelist
import phonon.connections

logging.disable(logging.CRITICAL)


def s_to_ms(s):
    return int(1000. * s)


class NodelistTest(unittest.TestCase):

    def setUp(self):
        self.conn = phonon.connections.connect(hosts=['localhost'])
        if hasattr(self.conn, "client"):
            self.conn.client.flushdb()

    def test_create_node_list(self):
        nodelist = Nodelist(b"key")
        assert nodelist.nodelist_key == b"phonon_key.nodelist"
        assert self.conn.client.hgetall(nodelist.nodelist_key) != {}

    def test_refresh_session_refreshes_time(self):
        nodelist = Nodelist(b"key")
        now = int(time.time() * 1000.)
        self.conn.client.hset(nodelist.nodelist_key, self.conn.id, now)
        time.sleep(0.01)
        nodelist.refresh_session()
        updated_now = nodelist.get_last_updated(self.conn.id)
        assert isinstance(updated_now, int)
        assert updated_now != now, "{} == {}".format(updated_now, now)

    def test_find_expired_nodes(self):
        now = int(time.time() * 1000.)
        expired = now - s_to_ms(2 * TTL + 1)

        nodelist = Nodelist(b"key")

        self.conn.client.hset(nodelist.nodelist_key, b'1', now)
        self.conn.client.hset(nodelist.nodelist_key, b'2', expired)

        target = nodelist.find_expired_nodes()
        assert b'2' in target, target
        assert b'1' not in target, target

    def test_remove_expired_nodes(self):
        now = int(time.time() * 1000.)
        expired = now - s_to_ms(2 * TTL + 1)

        nodelist = Nodelist(b"key")

        self.conn.client.hset(nodelist.nodelist_key, '1', expired)
        self.conn.client.hset(nodelist.nodelist_key, '2', expired)

        nodes = nodelist.get_all_nodes()
        assert b'1' in nodes
        assert b'2' in nodes

        nodelist.remove_expired_nodes()
        nodes = nodelist.get_all_nodes()
        assert b'1' not in nodes
        assert b'2' not in nodes

    def test_refreshed_node_not_deleted(self):
        now = int(time.time() * 1000.)
        expired = now - s_to_ms(2 * TTL + 1)

        nodelist = Nodelist(b'key')

        self.conn.client.hset(nodelist.nodelist_key, b'1', expired)
        self.conn.client.hset(nodelist.nodelist_key, b'2', expired)

        expired = nodelist.find_expired_nodes()
        assert b'2' in expired, expired
        assert b'1' in expired, expired
        self.conn.client.hset(nodelist.nodelist_key, b'1', now)

        nodelist.refresh_session(b'1')
        nodelist.remove_expired_nodes(expired)

        assert nodelist.get_last_updated(b'1') is not None, nodelist.get_last_updated(b'1')
        assert nodelist.get_last_updated(b'2') is None, nodelist.get_last_updated(b'2')

    def test_remove_node(self):
        nodelist = Nodelist(b'key')
        nodelist.refresh_session(b'1')

        nodes = nodelist.get_all_nodes()
        assert b'1' in nodes

        nodelist.remove_node('1')
        nodes = nodelist.get_all_nodes()
        assert b'1' not in nodes

    def test_clear_nodelist(self):
        nodelist = Nodelist(b'key')
        nodes = nodelist.clear_nodelist()
        nodes = nodelist.get_all_nodes()
        assert nodes == {}
