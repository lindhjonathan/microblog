"""
Test routes for routes for authorizing users, app/main/routes
Adding to commit again
"""
from datetime import datetime, timedelta
import pytest
from app import db
#from app import bp
from app.models import User, Post

class UserModelCase():
    """
    Test class for containing tests related to User and follower functions
    """
    def setUp(self):
        """
        Set up database session
        """
        db.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        """
        Teardown the database session
        """
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        """
        Test password hashing
        """
        u = User(username='susan')
        u.set_password('cat')

        assert u.check_password('dog') is False
        assert u.check_password('cat') is True

    def test_avatar(self):
        """
        Assert that the gratavar is correct for user
        """
        u = User(username='john', email='john@example.com')
        # self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
        #                                  'd4c74594d841139328695756648b6bd6'
        #                                  '?d=identicon&s=128'))

        assert str(u.avatar(128)) == ('https://www.gravatar.com/avatar/'
                                      'd4c74594d841139328695756648b6bd6'
                                      '?d=identicon&s=128')

    def test_follow(self):
        """
        Test follow functionality
        """
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        assert u1.followed.all() == []
        assert u1.followers.all() == []

        u1.follow(u2)
        db.session.commit()

        assert u1.is_following(u2) is True
        assert u1.followed.count() == 1
        assert u1.followed.first().username == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().username == 'john'

        u1.unfollow(u2)
        db.session.commit()

        assert u1.is_following(u2) is False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        """
        Create users, posts and followers
        """
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        assert f1 == [p2, p4, p1]
        assert f2 == [p2, p3]
        assert f3 == [p3, p4]
        assert f4 == [p4]
