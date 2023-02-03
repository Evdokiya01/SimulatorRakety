import time
import logging
import sys

PHONON_NAMESPACE = b"phonon"
TTL = 30 * 60

SYSLOG_LEVEL = logging.WARNING


def get_logger(name, log_level=SYSLOG_LEVEL):
    l = logging.getLogger(name)

    formatter = logging.Formatter(fmt='PHONON %(levelname)s - ( %(pathname)s ):%(funcName)s:L%(lineno)d %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    l.addHandler(handler)
    l.propagate = True
    l.setLevel(log_level)

    return l


def get_ms():
    return int(time.time() * 1000.)


def s_to_ms(s):
    return int(s * 1000.)
