from app import db


class User(db.Model):
    lincoln_id = db.Column(db.Integer, primary_key=True)
    lincoln_email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(15), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_lincoln_id(self):
        try:
            return unicode(self.lincoln_id)  # python 2
        except NameError:
            return str(self.lincoln_id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.lincoln_email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    lincoln_id = db.Column(db.Integer, db.ForeignKey('user.lincoln_id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)