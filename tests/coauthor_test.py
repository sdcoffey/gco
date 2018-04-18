import unittest

from gco import Coauthor


class CoauthorTest(unittest.TestCase):

    def testStr(self):
        ca = Coauthor('bob commiter', 'bob@gmail.com')
        self.assertEqual('bob commiter <bob@gmail.com>', ca.str())
