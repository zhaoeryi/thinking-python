import _hacking
import os

class PathNameTestCase(_hacking.HackingTestCase):
    def test_basename(self):
        basename = os.path.basename('c://a/b/c.txt')
        print 'basename=%s' % basename
