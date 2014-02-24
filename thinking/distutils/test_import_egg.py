import _hacking
from _test import init_func
from _test import test_entry

class ImportEggTestCase(_hacking.HackingTestCase):  
        def test_entry_func(self):
            test_entry.entry_func()
            
        def test_entry_cls(self):
            cls = test_entry.entry_cls()
            cls();
            
        def test_init_func(self):
            init_func()
            
