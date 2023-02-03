import time

import phonon
import phonon.connections
import phonon.exceptions


class Lock(object):

    def __init__(self, resource_key):
        self.lock_key = f"{resource_key}.lock".encode('utf8')
        self.conn = phonon.connections.connection

    def __enter__(self):
        acquired = self.conn.client.setnx(self.lock_key, self.conn.id)
        if not acquired:
            connection_id = self.conn.client.get(self.lock_key)
            if connection_id == self.conn.id:
                self.conn.client.pexpire(self.lock_key, phonon.TTL)
            else:
                raise phonon.exceptions.AlreadyLocked("Already locked")
        else:
            self.conn.client.pexpire(self.lock_key, phonon.TTL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.client.delete(self.lock_key)
