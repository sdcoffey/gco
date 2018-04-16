import argparse
import base64
import os
import tempfile

from subprocess import call, check_output

GIT_CONFIG_KEY = 'coauthor.authors'

class Coauthor(object):

    @staticmethod
    def parse(line):
        author_parts = line.split(':')
        return Coauthor(author_parts[0], author_parts[1])

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def str(self):
        return '{} <{}>'.format(self.name, self.email)


def commit(args):
    message = args.message or ''
    coauthors = _read_authors()

    if len(coauthors) > 0:
        message += '\n'
        message += '\n'.join(['Co-authored-by: {}'.format(coauthor.str()) for coauthor in coauthors])

    if args.message:
        sh('git commit -m "{}"'.format(message))
    elif len(coauthors) > 0:
        fd, path = tempfile.mkstemp()

        tmpfile = open(path, 'w')

        tmpfile.write('\n' + message)
        tmpfile.close()

        sh('git commit -t {}'.format(path))

        os.unlink(path)
    else:
        sh('git commit')


def show():
    print '\n'.join([ca.str() for ca in _read_authors()])


def clear():
    sh('git config --unset-all {}'.format(GIT_CONFIG_KEY))


def add():
    print 'Add your co-authors (press C-d to stop)'

    coauthors = []
    try:
        while True:
            name = raw_input("Co-author's name: ")
            email = raw_input("{}'s email: ".format(name))

            coauthors.append(Coauthor(name, email))
    except EOFError:
        pass

    if len(coauthors) > 0:
        coauthor_serialized = ','.join(['{}:{}'.format(coauthor.name, coauthor.email) for coauthor in coauthors])

        sh('git config --replace-all {} {}'.format(GIT_CONFIG_KEY, base64.b64encode(coauthor_serialized)))


def sh(command, return_output=False):
    command = command.split(' ')

    if return_output:
        return check_output(command).strip()

    call(command)


def _read_authors():
    authors = base64.b64decode(sh('git config {}'.format(GIT_CONFIG_KEY), return_output=True))
    return [Coauthor.parse(line) for line in authors.split(',')]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    commit_parser = subparsers.add_parser('commit')
    commit_parser.add_argument('-m', '--message', help='commit message')

    coauthor_parser = subparsers.add_parser('clear')
    coauthor_parser = subparsers.add_parser('add')
    coauthor_parser = subparsers.add_parser('show')

    args = parser.parse_args()

    if args.subcommand == 'commit':
        commit(args)
    elif args.subcommand == 'clear':
        clear()
    elif args.subcommand == 'show':
        show()
    elif args.subcommand == 'add':
        add()
    else:
        print 'command not supported: {}. Try again with --help for options'.format(args.subcommand)

