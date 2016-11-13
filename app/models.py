from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def convert_date_to_string(date_time):
    if isinstance(date_time, datetime.datetime):
        return date_time.strftime('%Y-%m-%d %H:%M:%S')
    return 'Null'


def get_current_time():
    return datetime.datetime.now()


class Base(db.Model):
    '''Base Mapper Class'''
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created = db.Column(db.DateTime(), default=db.func.now)
    date_modified = db.Column(db.DateTime(), default=db.func.now,
                              onupdate=db.func.now)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, resultset):
        formated_return_all_data = []
        for result in resultset:
            formated_return_all_data.append(result.get())
        return formated_return_all_data


class Item(Base):
    '''Class mapper for the items in the bucketlist '''
    __tablename__ = 'items'
    name = db.Column(db.String(50))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    done = db.Column(db.Boolean, default=False)

    def get(self):
        return {
            'id': self.id if self.id else 'Null',
            'name': self.name if self.name else 'Null',
            'bucketlist_id':
            self.bucketlist_id if self.bucketlist_id else 'Null',
            'date_created': convert_date_to_string(self.date_created),
            'date_modified': convert_date_to_string(self.date_modified),
            'done': self.done if self.done else False
        }

    def __str__(self):
        return 'ITEM :: Id:%s\n Name:%s\n Date Created:%s\n'\
            ' Date Modified:%s ' % (self.id, self.name,
                                    convert_date_to_string(
                                        self.date_created),
                                    convert_date_to_string(
                                        self.date_modified))


class BucketList(Base):
    ''' Class mapper with Bucketlists details '''
    __tablename__ = 'bucketlist'
    name = db.Column(db.String(20))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get(self):
        user_name = User.query.filter_by(id=self.created_by).first()
        user_name = {} if not user_name else user_name.get()
        return {
            'id': self.id if self.id else 'Null',
            'name': self.name if self.name else 'Null',
            'item': [],
            'date_created': convert_date_to_string(self.date_created),
            'date_modified': convert_date_to_string(self.date_modified),
            'created_by': user_name.get('username', 'Null')
        }

    def __str__(self):
        return 'BUCKETLIST :: Id:%s\n Name:%s\n Date Created:%s\n'\
            ' Date Modified:%s ' % (self.id, self.name,
                                    convert_date_to_string(
                                        self.date_created),
                                    convert_date_to_string(
                                        self.date_modified))


class User(Base):
    ''' Class mapper with User details'''
    __tablename__ = 'user'
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))

    def get(self):
        return {
            'id': self.id if self.id else 'Null',
            'username': self.username if self.username else 'Null',
            'password': self.password if self.password else 'Null',
            'date_created': convert_date_to_string(self.date_created),
            'date_modified': convert_date_to_string(self.date_modified)
        }

    def __str__(self):
        return 'USER :: Id:%s\n Username:%s\n Date Created:%s\n'\
            ' Date Modified:%s ' % (self.id, self.username,
                                    convert_date_to_string(
                                        self.date_created),
                                    convert_date_to_string(
                                        self.date_modified))
