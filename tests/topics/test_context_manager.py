from unittest import TestCase
from shoppon.topics import context_manager as cm


class TestContextManager(TestCase):
    def test0(self):
        with cm.MyOpen(__file__) as f:
            print(f)

    def test_not_exist(self):
        with cm.MyOpen('fake') as f:
            print(f)

    def test1(self):
        with cm.my_open(__file__) as f:
            print(f)
