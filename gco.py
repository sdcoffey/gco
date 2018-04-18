#!/usr/bin/python

import argparse
import base64
import os
import subprocess
import tempfile


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

    coauthor_stanza = ''
    if len(coauthors) > 0:
        coauthor_stanza = '\n\n\n'
        coauthor_stanza += '\n'.join(['Co-authored-by: {}'.format(coauthor.str()) for coauthor in coauthors])

    path = None

    if args.message:
        with _tempfile() as tmpfile:
            path = tmpfile.name

            tmpfile.write(message)
            tmpfile.write(coauthor_stanza)

        sh('git commit -F {}'.format(path).split(' '))
    elif len(coauthors) > 0:
        with _tempfile() as tmpfile:
            path = tmpfile.name

            tmpfile.write(coauthor_stanza)

        sh('git commit -t {}'.format(path).split(' '))
    else:
        sh('git commit'.split(' '))

    if path:
        os.unlink(path)


def show():
    print '\n'.join([ca.str() for ca in _read_authors()])


def clear():
    sh('git config --unset-all {}'.format(GIT_CONFIG_KEY).split(' '))


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

        sh('git config --replace-all {} {}'.format(GIT_CONFIG_KEY, base64.b64encode(coauthor_serialized)).split(' '))


def shpipe(args, stdout=None, wd=None, stdin=None):
    cmd = _sp(args, stdout=stdout, stdin=stdin, wd=wd)
    cmd.wait()


def sh(args, wd=None, stdin=None):
    cmd = _sp(args, stdout=subprocess.PIPE, wd=wd, stdin=stdin)

    return cmd.communicate()[0].strip()


def _sp(args, stdout=None, stdin=None, wd=None):
    if not wd:
        wd = os.getcwd()

    return subprocess.Popen(args, cwd=wd, stdout=stdout, stdin=stdin)


def _read_authors():
    try:
        config = sh('git config {}'.format(GIT_CONFIG_KEY).split(' '))
        authors = base64.b64decode(config)

        if len(authors) == 0:
            return []

        return [Coauthor.parse(line) for line in authors.split(',')]
    except subprocess.CalledProcessError:
        return []


def _tempfile():
    fd, path = tempfile.mkstemp()
    return open(path, 'w')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    commit_parser = subparsers.add_parser('commit')
    commit_parser.add_argument('-m', '--message', help='commit message')

    subparsers.add_parser('clear')
    subparsers.add_parser('add')
    subparsers.add_parser('show')

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

