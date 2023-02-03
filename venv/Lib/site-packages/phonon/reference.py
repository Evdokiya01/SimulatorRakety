from phonon import get_logger, PHONON_NAMESPACE, TTL

import phonon.lock
import phonon.nodelist
import phonon.connections

logger = get_logger(__name__)


class Reference:
    """
    Represents a reference to some resource in the network. Handles reference
    counting, dereferencing, locking/ownership, and maintaining whether or not
    resources were externally modified.

    This class also provides a layer of abstraction on failover and cleanup. In
    the event of total process failure; a reference on that process will expire
    and be subsequently detected/recovered by this class to the extent updates
    overlap.

    More in-depth:

    When a process acquires a `Reference` to a resource it attempts to lock
    that resource. It will block by default for a total of Process.BLOCKING_TIMEOUT
    seconds (defaults to 500s) before raising a Reference.AlreadyLocked
    exception

    That process/reference will attempt to connect to the backend, and retry
    until either successful completion of the task or python's maximum
    recursion depth has been reached (100 retries), sleeping
    Process.RETRY_SLEEP seconds between each retry (defaults to 0.5s).

    Upon successfully locking; `Reference` will create a record with the key
    "{0}.reflist".format(pid) in redis where the key is the unique id for the
    process this code is running on and the value is the unix timestamp for the
    time the process last modified that entry. If a pid is in that list it is
    assumed they currently have an active session for whatever resource is
    locked. If the record was created longer ago than the session length it is
    assumed the process "fell over". It's reference will be cleaned up and the
    reference count will be decremented.

    Reference counts are calculated by the length of the json structure
    described above after process failures have been resolved.

    """

    def __init__(self, resource):
        """
        :param Process process: The Process to which this reference belongs
        :param str resource: An identifier for the resource. For example:
            Buzz.12345

        """
        self.resource_key = resource
        self.nodelist = phonon.nodelist.Nodelist(resource)
        self.times_modified_key = PHONON_NAMESPACE + b'_' + resource + b'.times_modified'
        self.refcount_key = PHONON_NAMESPACE + b'_' + resource + b'.refcount'
        self.force_expiry = False
        self.conn = phonon.connections.connection
        if self.resource_key not in self.conn.local_registry:
            self.conn.client.incr(self.refcount_key)
            self.conn.add_to_registry(self.resource_key)

        self.refresh_session()

    def lock(self):
        """
        Locks the resource managed by this reference.
        """
        return phonon.lock.Lock(self.resource_key)

    def refresh_session(self):
        """
        Update the session for this node. Specifically; lock on the reflist,
        then update the time  this node acquired the reference.

        This method should only be called while the reference is locked.
        """
        expired_nodes = self.nodelist.find_expired_nodes()
        if expired_nodes:
            self.nodelist.remove_expired_nodes(expired_nodes)
        self.nodelist.refresh_session()

    def increment_times_modified(self):
        """
        Increments the number of times this resource has been modified by all
        processes.
        """
        rc = self.conn.client.incr(self.times_modified_key)
        self.conn.client.pexpire(self.times_modified_key,
                                 phonon.s_to_ms(TTL))  # ttl is in ms

    def get_times_modified(self):
        """
        :returns: The total number of times increment_times_modified has been called for this resource by all processes.
        :rtype: int
        """
        times_modified = self.conn.client.get(self.times_modified_key)
        if times_modified is None:
            return 0
        return int(times_modified)

    def count(self):
        """
        :returns: The total number of elements in the reference list.
        :rtype: int
        """
        references = self.conn.client.get(self.refcount_key)
        if references is None:
            return 0
        return int(references)

    def dereference(self, callback=None, args=None, kwargs=None):
        """
        This method should only be called while the reference is locked.

        Decrements the reference count for the resource. If this process holds
        the only reference at the time we finish dereferencing it; True is
        returned. Operating on the resource after it has been dereferenced is
        undefined behavior.

        Dereference queries the value stored in the backend, if any, iff (if
        and only if) this instance is the last reference to that resource. e.g.
        self.count() == 0

        :param function callback: A function to execute iff it's determined
            this process holds the only reference to the resource. When there
            is a failure communicating with the backend in the cleanup step the
            callback function will be called an additional time for that
            failure and each subsequent one thereafter. Ensure your callback
            handles this properly.
        :param tuple args: Positional arguments to pass your callback.
        :param dict kwargs: keyword arguments to pass your callback.

        :returns: Whether or not there are no more references among all
            processes. True if this was the last reference. False otherwise.
        :rtype: bool
        """
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = {}

        client = self.conn.client

        should_execute = False
        if self.force_expiry:
            should_execute = True

        if not should_execute:
            self.nodelist.remove_node(self.conn.id)
            self.nodelist.remove_expired_nodes()

            updated_refcount = client.incr(self.refcount_key, -1)
            should_execute = (updated_refcount <= 0)  # When we force expiry this will be -1

        try:
            if callable(callback) and should_execute:
                callback(*args, **kwargs)
        finally:
            if should_execute:
                client.delete(self.resource_key,
                              self.nodelist.nodelist_key,
                              self.times_modified_key,
                              self.refcount_key)

            self.conn.remove_from_registry(self.resource_key)
        return should_execute
