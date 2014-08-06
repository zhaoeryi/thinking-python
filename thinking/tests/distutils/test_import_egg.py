from _test import init_func
from _test import test_entry
from thinking.tests import base


class ImportEggTestCase(base.ThinkingTestCase):
        def test_entry_func(self):
            test_entry.entry_func()

        def test_entry_cls(self):
            cls = test_entry.entry_cls()
            cls()

        def test_init_func(self):
            init_func()
