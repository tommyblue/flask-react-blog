from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
import os.path

app = Flask(__name__)
db_file = "./test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(db_file)
db = SQLAlchemy(app)

def init_db():
    db.create_all()
    post_1 = Post("Post #1", "Test for the **content** with markdown")
    db.session.add(post_1)
    post_2 = Post("Post #2", "# Great news\nThis should be the first _post_ in the list")
    db.session.add(post_2)
    db.session.commit()

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
        return {'id': self.id, 'title': self.title, 'content': self.content, 'pub_date': self.pub_date}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/posts", methods=['GET', 'POST'])
def single_post():
    if request.method == 'POST':
        if create_post(request.form['title'], request.form['content']):
            posts = get_posts()
            return jsonify({'posts': [post.serialize() for post in posts]})
        else:
            abort(400)
    else:
        posts = get_posts()
        return jsonify({'posts': [post.serialize() for post in posts]})

@app.route("/posts/<int:post_id>", methods=['GET', 'DELETE'])
def show_post(post_id):
    if request.method == 'DELETE':
        if delete_post(post_id):
            posts = get_posts()
            return jsonify({'posts': [post.serialize() for post in posts]})
        else:
            abort(400)
    else:
        post = get_posts(post_id)
        return jsonify(post.serialize())

def delete_post(post_id):
    try:
        Post.query.filter(Post.id==post_id).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def get_posts(post_id = None):
    if post_id:
        try:
            post = Post.query.filter(Post.id==post_id).one()
            return post
        except NoResultFound:
            abort(404)
    else:
        posts = Post.query.order_by(desc(Post.pub_date))
        return posts

def create_post(title, content):
    try:
        post = Post(title, content)
        db.session.add(post)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

@app.errorhandler(400)
def not_found(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

if not os.path.isfile(db_file):
    init_db()

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0')
