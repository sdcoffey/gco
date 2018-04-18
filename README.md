## Git-Coauthor

Git-coauthor is an easy way to take advantage of [Co-Authors](https://help.github.com/articles/creating-a-commit-with-multiple-authors/) on Github!

## Usage

### Add co-authors
```sh
$ gco add
```

### Make a commit

```sh
$ git add some-file.py
$ gco commit # or gco commit -m'added some-file.py'
```

### See who's riding along

```sh
$ gco show
```

### Go solo

```sh
$ gco clear
```

Git-coauthor uses your local git config to store authors, so make sure you re-add authors when switching between projects.

## Installation

Clone this repo, and then:

```sh
$ make install
```
