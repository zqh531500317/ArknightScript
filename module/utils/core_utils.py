import random
import socket

from adbutils import _AdbStreamConnection, AdbTimeout


def recv_all(stream, chunk_size=4096) -> bytes:
    if isinstance(stream, _AdbStreamConnection):
        stream = stream.conn

    try:
        fragments = []
        while 1:
            chunk = stream.recv(chunk_size)
            if chunk:
                fragments.append(chunk)
            else:
                break
        return b''.join(fragments)
    except socket.timeout:
        raise AdbTimeout('adb read timeout')


def random_port(port_range):
    """ get a random port from port set """
    new_port = random.choice(list(range(*port_range)))
    if is_port_using(new_port):
        return random_port(port_range)
    else:
        return new_port


def is_port_using(port_num):
    """ if port is using by others, return True. else return False """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        result = s.connect_ex(('127.0.0.1', port_num))
        # if port is using, return code should be 0. (can be connected)
        return result == 0
    finally:
        s.close()
