from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Item(db.Model):
    '''Class mapper for the items in the bucketlist '''

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())
    done = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(self):
        return {
            'id': self.id,
            'name': self.title,
            'bucketlist_id': self.bucketlist_id,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': self.done
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BucketList(db.Model):
    ''' Class mapper with Bucketlists details '''

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20))
    date_created = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(self):
        return {
            'id': id,
            'name': self.name,
            'item': [],
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.delete(self)
        db.commit()


class User(db.Model):
    ''' Class mapper with User details'''

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    def update(self):
        db.session()

    def delete(self):
        db.session(self)
        db.commit()
