import time

import phonon.client
import phonon.connections
from phonon import PHONON_NAMESPACE


class Nodelist(object):
    """
    Keeps track of the nodes currently holding a reference to a particular
    resource by maintaining a hash in redis with the node ids and time the
    session was last refreshed.
    """

    def __init__(self, resource_key):
        """
        :param phonon.connections.AsyncConn conn: The Process to which the instantiating
            reference belongs
        :param string resource_key: An identifier for the instantiating
            reference
        """
        if not isinstance(resource_key, bytes):
            raise TypeError(f'NodeList got a resource_key of type {type(resource_key)}. Expected bytes.')

        self.resource_key = resource_key
        self.nodelist_key = PHONON_NAMESPACE + b'_' + resource_key + b'.nodelist'
        self.conn = phonon.connections.connection
        self.refresh_session()

    def refresh_session(self, node_id=None):
        """
        Adds or refreshes a particular node in the nodelist, attributing the
        current time with the node_id.

        :param string node_id: optional, the connection id of the node whose
        session should be refreshed
        """
        if not node_id:
            node_id = self.conn.id
        if not isinstance(node_id, bytes):
            raise TypeError(f'`refresh_session` expected bytes. Got {type(node_id)}')

        self.conn.client.hset(self.nodelist_key, node_id, int(time.time() * 1000.))

    def find_expired_nodes(self, node_ids=None):
        """
        Detects connections that have held a reference for longer than its
        process_ttl without refreshing its session. This function does not
        actually removed them from the hash. (See remove_expired_nodes.)

        :param list node_ids: optional, a list of ids to check to see if they
            have expired.  If node_ids is not passed in, all nodes in the hash
            will be checked.
        """
        if node_ids:
            nodes = list(zip(node_ids, [int(t) for t in self.conn.client.hmget(self.nodelist_key, node_ids)]))
        else:
            nodes = list(self.get_all_nodes().items())

        expiration_delta = self.conn.PROCESS_TTL * 1000.
        now = int(time.time() * 1000.)
        return [node_id for (node_id, last_updated) in nodes if (now - last_updated) > expiration_delta]

    def remove_expired_nodes(self, node_ids=None):
        """
        Removes all expired nodes from the nodelist.  If a set of node_ids is
        passed in, those ids are checked to ensure they haven't been refreshed
        prior to a lock being acquired.

        Should only be run with a lock.

        :param list node_ids: optional, a list of node_ids to remove.  They
            will be verified to ensure they haven't been refreshed.

        """
        nodes = self.find_expired_nodes(node_ids)
        if nodes:
            self.conn.client.hdel(self.nodelist_key, *nodes)

    def remove_node(self, node_id=None):
        """
        Removes a particular node from the nodelist.

        :param string node_id: optional, the process id of the node to remove
        """
        if not node_id:
            node_id = self.conn.id

        self.conn.client.hdel(self.nodelist_key, node_id)

    def clear_nodelist(self):
        """
        Removes all nodes from a nodelist.

        Should only be run with a lock.
        """
        self.conn.client.delete(self.nodelist_key)

    def get_last_updated(self, node_id=None):
        """
        Returns the time a particular node has been last refreshed.

        :param string node_id: optional, the connection id of the node to retrieve

        :rtype: int
        :returns: Returns a unix timestamp if it exists, otherwise None
        """
        if not node_id:
            node_id = self.conn.id
        if not isinstance(node_id, bytes):
            raise TypeError(f'`get_last_updated` expected `node_id` to be bytes. Got {type(node_id)}')

        dt = self.conn.client.hget(self.nodelist_key, node_id)
        return int(dt) if dt else None

    def get_all_nodes(self):
        """
        Returns all nodes in the hash with the time they were last refreshed
        as a dictionary.

        :rtype: dict(string, int)
        :returns: A dictionary of strings and corresponding timestamps

        """
        nodes = self.conn.client.hgetall(self.nodelist_key)
        return {node_id: int(dt) for (node_id, dt) in list(nodes.items())}

    def count(self):
        """
        :rtype: int
        :returns: The number of nodes in the nodelist
        """
        return self.conn.client.hlen(self.nodelist_key)
