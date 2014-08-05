import thinking
import os
from thinking.tests import base
class PathNameTestCase(base.ThinkingTestCase):
    def test_basename(self):
        basename = os.path.basename('c://a/b/c.txt')
        print 'basename=%s' % basename
