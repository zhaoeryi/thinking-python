from __future__ import print_function

from thinking.tests import base


class StringTestCase(base.ThinkingTestCase):
    def test_partition(self):
        log_levels = ['root=INFO',
                    'routes.middleware=DEBUG',
                    'boto=WARN']

        for pair in log_levels:
            _key, _sep, _value = pair.partition('=')

    def test_rpartition(self):
        binary = 'nova-scheduler'
        head, seperator, tail = binary.rpartition('nova-')
        manager_cls = ('%s_manager' % binary.rpartition('nova-')[2])

