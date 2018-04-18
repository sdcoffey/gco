import gco

import os
import shutil
import tempfile
import unittest


class IntegrationTest(unittest.TestCase):

    PYTHON = gco.sh(['which', 'python'])

    def setUp(self):
        self.startingdir = os.getcwd()

        if self.startingdir.endswith('tests'):
            self.gcopath = os.path.join(os.path.dirname(self.startingdir), 'gco.py')
        else:
            self.gcopath = os.path.join(self.startingdir, 'gco.py')

        temppath = tempfile.mkdtemp()
        os.chdir(temppath)

        IntegrationTest.initGit()

    def tearDown(self):
        temppath = os.getcwd()

        os.chdir(self.startingdir)
        shutil.rmtree(temppath)

    def testAdd_setsCoauthorsInGitConfig(self):
        with gco._tempfile() as stdin:
            stdin.write('Example Programmer\n')
            stdin.write('programmer@example.com\n')
            stdin.write('Example Programmer 2\n')
            stdin.write('programmer2@example.com\n')
            path = stdin.name

        stdin = open(path, 'r')

        self.goshpipe(['add'], stdin=stdin)

        output = self.gosh(['show'])
        self.assertEqual('Example Programmer <programmer@example.com>\nExample Programmer 2 <programmer2@example.com>',
                         output)

    def testAdd_partialInput_addsNoAuthors(self):
        with gco._tempfile() as stdin:
            stdin.write('Example Programmer\n')
            path = stdin.name

        stdin = open(path, 'r')

        self.gosh(['add'], stdin=stdin)

        output = self.gosh(['show'])
        self.assertEqual('', output)

    def testClear_clearsCoauthorsFromConfig(self):
        stub = 'RXhhbXBsZSBQcm9ncmFtbWVyOnByb2dyYW1tZXJAZXhhbXBsZS5jb20='

        gco.sh(['git', 'config', '--replace-all', 'coauthor.authors', stub])

        self.gosh(['clear'])
        output = self.gosh(['show'])

        self.assertEqual('', output)

    def testShow_showsCoauthors(self):
        stub = 'RXhhbXBsZSBQcm9ncmFtbWVyOnByb2dyYW1tZXJAZXhhbXBsZS5jb20='
        
        gco.sh(['git', 'config', '--replace-all', 'coauthor.authors', stub])

        output = self.gosh(['show'])
        self.assertEqual('Example Programmer <programmer@example.com>', output)

    def testCommit_withNoCoauthors_makesNormalCommit(self):
        gco.sh(['touch', 'one.txt'])
        gco.sh(['git', 'add', 'one.txt'])

        self.goshpipe(['commit', '-m', 'initial commit'])
        lastmessage = gco.sh(['git', 'log', '-1', '--pretty=%B'])

        self.assertEqual('initial commit', lastmessage)

    def testCommit_withCoauthor_usesTemplate(self):
        self.fail('not implemented')
        pass

    def testCommit_withMFlag_usesProperMessage(self):
        stub = 'RXhhbXBsZSBQcm9ncmFtbWVyOnByb2dyYW1tZXJAZXhhbXBsZS5jb20='

        gco.sh(['git', 'config', '--replace-all', 'coauthor.authors', stub])

        gco.sh(['touch', 'one.txt'])
        gco.sh(['git', 'add', 'one.txt'])

        self.goshpipe(['commit', '-m', 'initial commit'])
        lastmessage = gco.sh(['git', 'log', '-1', '--pretty=%B'])

        self.assertEqual('initial commit\n\nCo-authored-by: Example Programmer <programmer@example.com>', lastmessage)

    def gosh(self, args, stdin=None):
        cargs = [IntegrationTest.PYTHON, self.gcopath]
        cargs.extend(args)

        return gco.sh(cargs, stdin=stdin)

    def goshpipe(self, args, stdin=None):
        cargs = [IntegrationTest.PYTHON, self.gcopath]
        cargs.extend(args)

        return gco.shpipe(cargs, stdin=stdin)

    @staticmethod
    def initGit():
        gco.sh(['git', 'init'])
        gco.sh(['git', 'config', 'user.name', 'tech_lead'])
        gco.sh(['git', 'config', 'user.email', 'techlead@example.com'])



class Fakeargs(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == '__main__':
    unittest.main()
