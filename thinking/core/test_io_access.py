import thinking
import os

class PathNameTestCase(thinking.HackingTestCase):
    def test_basename(self):
        basename = os.path.basename('c://a/b/c.txt')
        print 'basename=%s' % basename
