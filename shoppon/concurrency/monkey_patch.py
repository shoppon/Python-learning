# coding: utf-8
import socket
import sys

from eventlet import monkey_patch
from eventlet.patcher import is_monkey_patched

if __name__ == '__main__':
    old_socket = sys.modules.get('socket')
    old_socket_id = id(old_socket.create_connection)

    monkey_patch(socket=True)

    new_socket = sys.modules.get('socket')
    new_socket_id = id(new_socket.create_connection)

    # patch前后create_connection函数被替换了
    assert old_socket_id != new_socket_id

    # 无法取消patch
    monkey_patch(socket=False)
    assert is_monkey_patched(socket) is True
