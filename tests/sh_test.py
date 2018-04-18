import gco

import os
import unittest
import tempfile


class ShTest(unittest.TestCase):

    def testSh_returnOutput(self):
        output = gco.sh(['echo', 'hello'])
        self.assertEqual('hello', output)

    def testSh_withCwd(self):
        tmpdir = tempfile.mkdtemp()
        gco.sh(['touch', 'temp.txt'], wd=tmpdir)
        self.assertTrue(os.path.isfile(os.path.join(tmpdir, 'temp.txt')))
