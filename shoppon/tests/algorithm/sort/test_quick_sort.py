from unittest import TestCase

from shoppon.algorithm.sort import quick_sort


class TestSort(TestCase):
    def test_sort(self):
        nums = [12, 19, 2, 6, 79, 68]
        quick_sort.sort(nums, 0, len(nums) - 1)
        self.assertEquals([2, 6, 12, 19, 68, 79], nums)
