# Fixtures for MongoEngine


Lets you create fixtures based on python dicts. Supports string references between documents.
Has been inspired by [yii2 fixtures](https://github.com/yiisoft/yii2/tree/master/framework/test).


* Free software: MIT license

## Usage

As an example, I'm going to assume we have a application with the following directory structure.

```
/myapp
    __init__.py
    models.py
    /tests
        /data
            users.py
            posts.py
        fixtures.py
        test_something.py
```

Simple mongoengine documents in models.py

```python
from mongoengine import Document, fields


class User(Document):
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=True)
    email = fields.StringField(required=True)
    birthday = fields.DateTimeField()


class Post(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ObjectIdField(required=True)
    created_at = fields.DateTimeField()

```


### Add fixtures

#### First way
Models data are stored inside fixture class (added in 1.3.0)

```python
from fixtures_mongoengine import Fixture
from myapp.models import User, Post


class FixtureUser(Fixture):

    document_class = User

    data = {
        'user1': {
            'first_name': 'Joyce',
            'last_name': 'Ray',
            'email': 'jray0@quantcast.com',
            'birthday': datetime.date(1983, 7, 12)
        },
        'user2': {
            'first_name': 'Amy',
            'last_name': 'Myers',
            'email': 'amyers1@live.com',
            'birthday': datetime.date(1987, 11, 27)
        }
    }


class FixturePost(Fixture):

    document_class = Post

    depends = {
        'users': FixtureUser
    }

    data = {
        'post1': {
            'title': 'Sherlock Gets A Musical Parody',
            'text': 'Sherlock fans still have a way to go before Season 4 of the BBC drama finally arrives.',
            'author': '{users.user1}'
        },
        'post2': {
            'title': 'NASA prepares to sample an asteroid',
            'text': 'On September 8, NASA will launch its first sample return mission to an asteroid.',
            'author': '{users.user2}',
        }
    }

```


#### Second way
Models data are stored in separate files.

```python
from fixtures_mongoengine import Fixture
from myapp.models import User, Post


class FixtureUser(Fixture):

    document_class = User

    data_file = 'myapp.tests.data.users'


class FixturePost(Fixture):

    document_class = Post

    depends = {
        'users': FixtureUser
    }

    data_file = 'myapp.tests.data.posts'
```

Add fixtures data

users.py
```python
import datetime as datetime

fixture_data = {
    'user1': {
        'first_name': 'Joyce',
        'last_name': 'Ray',
        'email': 'jray0@quantcast.com',
        'birthday': datetime.date(1983, 7, 12)
    },
    'user2': {
        'first_name': 'Amy',
        'last_name': 'Myers',
        'email': 'amyers1@live.com',
        'birthday': datetime.date(1987, 11, 27)
    }
}
```

posts.py
```python
fixture_data = {
    'post1': {
        'title': 'Sherlock Gets A Musical Parody',
        'text': 'Sherlock fans still have a way to go before Season 4 of the BBC drama finally arrives.',
        'author': '{users.user1}'
    },
    'post2': {
        'title': 'NASA prepares to sample an asteroid',
        'text': 'On September 8, NASA will launch its first sample return mission to an asteroid.',
        'author': '{users.user2}',
    }
}
```

### Create testcase.
Make sure the app that you're testing is initialized with the proper configuration (including db connection).

```python
import unittest
from myapp.tests.fixtures import FixturePost


class SomeTestCase(unittest.TestCase, FixturesMixin):

    fixtures_conf = {
        'posts': FixturePost
    }

    def test_something(self):

        assert len(Post.objects()) == 2
        assert len(User.objects()) == 2

        assert self.posts['post1'].title == 'Sherlock Gets A Musical Parody'

        author = User.objects(pk=self.posts['post1'].author).first()
        assert author.last_name == 'Ray'
```