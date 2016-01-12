
from initializer import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, content, pub_date=None):
        self.title = title

        self.content = content
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'pub_date': self.pub_date
        }
