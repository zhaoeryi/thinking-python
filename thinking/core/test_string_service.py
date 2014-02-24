import _hacking

class StringTestCase(_hacking.HackingTestCase):
    def test_partition(self):
        log_levels = ['root=INFO',
                    'routes.middleware=DEBUG',
                    'boto=WARN'
                    ]
        for pair in log_levels:
            _key, _sep, _value = pair.partition('=')
            print "_key=" , _key, "_sep=" , _sep, "_value=" , _value

    def test_rpartition(self):
        binary = 'nova-scheduler'
        head, seperator, tail = binary.rpartition('nova-')
        print 'head=%s, seperator=%s, tail=%s' % (head, seperator, tail)
        manager_cls = ('%s_manager' % 
                           binary.rpartition('nova-')[2])
        print 'manager_cls=', manager_cls

    def test_in(self):
        print "hello" in "abchellodef"