from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Base(db.Model):
    '''Base Mapper Class'''
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Item(Base):
    '''Class mapper for the items in the bucketlist '''
    __tablename__ = 'items'
    name = db.Column(db.String(50))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime(), default=datetime.now())
    date_modified = db.Column(db.DateTime(), default=datetime.now())
    done = db.Column(db.Boolean, default=False)

    def get(self):
        return {
            'id': self.id,
            'name': self.title,
            'bucketlist_id': self.bucketlist_id,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': self.done
        }


class BucketList(Base):
    ''' Class mapper with Bucketlists details '''
    __tablename__ = 'bucketlist'
    name = db.Column(db.String(20))
    date_created = db.Column(db.DateTime(), default=datetime.now())
    date_modified = db.Column(db.DateTime(), default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get(self):
        return {
            'id': id,
            'name': self.name,
            'item': [],
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }


class User(Base):
    ''' Class mapper with User details'''
    __tablename__ = 'user'
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def get(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
