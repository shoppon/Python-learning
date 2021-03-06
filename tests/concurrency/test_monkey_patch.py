# coding: utf-8
import socket
import sys
from unittest import TestCase

from eventlet import monkey_patch
from eventlet.patcher import is_monkey_patched


class TestMonkeyPatch(TestCase):
    def test_function_replace(self):
        old_socket = sys.modules.get('socket')
        old_socket_id = id(old_socket.create_connection)

        monkey_patch(socket=True)

        new_socket = sys.modules.get('socket')
        new_socket_id = id(new_socket.create_connection)

        # patch前后create_connection函数被替换了
        self.assertNotEqual(old_socket_id, new_socket_id)
        self.assertEqual(True, is_monkey_patched(socket))
