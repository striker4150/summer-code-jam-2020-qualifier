"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import re
import typing


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        self.values = {}
        self.field_type = field_type

    # Store the name of the set attribute
    def __set_name__(self, owner, name):
        self.name = name

    # Use instance ids to separate values
    def __get__(self, instance, owner):
        return self.values[id(instance)]

    def __set__(self, instance, value):
        if isinstance(value, self.field_type):
            self.values[id(instance)] = value
        else:
            raise TypeError('expected an instance of type {} for attribute {}, got {} instead'.format(repr(self.field_type.__name__), repr(self.name), repr(type(value).__name__)))


class Article:
    """The `Article` class you need to write for the qualifier."""

    id = 0

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        self.id = Article.id
        Article.id += 1

        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.content = content
        self.last_edited = None

    def __repr__(self):
        args = (repr(self.title), repr(self.author), repr(self.publication_date.isoformat()))
        return "<Article title={} author={} publication_date={}>".format(*args)

    def __len__(self):
        return len(self.content)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == "content":
            self.last_edited = datetime.datetime.now()

    # Sort functions use __lt__(self, other)
    def __lt__(self, other):
        return self.publication_date < other.publication_date

    def short_introduction(self, n_characters: int):
        cutoff = n_characters
        while self.content[cutoff] != " " and self.content[cutoff] != "\n":
            cutoff = cutoff - 1
        return self.content[0:cutoff]

    def most_common_words(self, n_words: int):
        words = re.findall('[a-z]+', self.content.lower())
        wordcount = {}
        for word in words:
            # Updating an OrderedDict does not change order
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] = wordcount[word] + 1
        # sorted() is guaranteed to be stable
        return dict(sorted(wordcount.items(), key=lambda x: x[1], reverse=True)[0:n_words])
