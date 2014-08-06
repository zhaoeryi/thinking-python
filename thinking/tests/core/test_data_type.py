from __future__ import print_function

import collections

from thinking.tests import base


class CollectionsTestCase(base.ThinkingTestCase):
    def test_deque(self):
        # double-ended queue
        DUP_MSG_CHECK_SIZE = 16
        deque = collections.deque([1, 2, 3], maxlen=DUP_MSG_CHECK_SIZE)

        # pop left
        self.assertEqual(deque.popleft(), 1)

        # append and pop
        deque.append(4)
        self.assertEqual(deque.pop(), 4)

        for i in deque:
            print(i)


class DictTestCase(base.ThinkingTestCase):
    def test_setdefault(self):
        key = "mykey"
        default_value = "default value"

        _MAPS = {}

        # test default value
        _MAPS.setdefault(key, default_value)
        self.assertEqual(_MAPS.get(key), default_value)

        # test new value
        new_value = "new values"
        _MAPS[key] = new_value
        self.assertNotEqual(_MAPS.get(key), default_value)
        self.assertEqual(_MAPS.get(key), new_value)


class ArrayTestCase(base.ThinkingTestCase):
    def test_append(self):
        arr = [1, 2, 3]
        arr.append("4")
        self.assertEqual(len(arr), 4)

    def test_extend(self):
        arr1 = [1, 2, 3]
        arr2 = [4, 5, 6]
        arr1.extend(arr2)
        self.assertEqual(len(arr1), 6)

    def test_index(self):
        arr = [0, 1, 2, 3, 4, 5]
        newarr = ['a', 'b', 'c', 'd', 'e']
        arr[1:1] = newarr
        print(arr)

    def test_enumerate(self):
        new_filter = ['a', 'b', 'c']
        new_filter = [s for s in new_filter if 'b' not in s.strip()]
        print(new_filter)
