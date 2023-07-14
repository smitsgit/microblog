from datetime import datetime
from hashlib import md5
from time import time

import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from flask_app import db, login, app
from flask_login import UserMixin

followers_association = db.Table("followers",
                                 db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                                 db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # This is just like, how one user has many posts , one user can follow many users and just like
    # posts, those are called followed_users
    followed_users = db.relationship('User', secondary=followers_association,
                                     primaryjoin=(followers_association.c.follower_id == id),
                                     secondaryjoin=(followers_association.c.followed_id == id),
                                     backref=db.backref('my_followers', lazy='dynamic'),
                                     lazy='dynamic')

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed_users.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed_users.remove(user)

    def is_following(self, user):
        '''
        The condition that I'm using in is_following() looks for items in the association table
        that have the left side foreign key set to the self user, and the right side set to the user argument.
        '''
        return self.followed_users.filter(followers_association.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers_association, (followers_association.c.followed_id == Post.user_id)).filter(
            followers_association.c.follower_id == self.id)

        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
