from flask import jsonify, request, abort, render_template
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from models import Post
from initializer import db, app
from marshmallow import Schema


class PostSchema(Schema):
    """
    Post serializer
    """
    class Meta:
        fields = ('id', 'title', 'content', 'pub_date')

posts_schema = PostSchema(many=True)
post_schema = PostSchema()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/posts", methods=['GET', 'POST'])
def single_post():
    if request.method == 'POST':
        if not create_post(request.form['title'], request.form['content']):
            abort(400)

    posts = get_posts()
    return jsonify({'posts': posts_schema.dump(posts).data})


@app.route("/posts/<int:post_id>", methods=['GET', 'DELETE'])
def show_post(post_id):
    if request.method == 'DELETE':
        if delete_post(post_id):
            posts = get_posts()
            return jsonify({'posts': posts_schema.dump(posts).data})
        else:
            abort(400)
    else:
        post = get_posts(post_id)
        return jsonify(post_schema.dump(post).data)


def delete_post(post_id):
    try:
        Post.query.filter(Post.id == post_id).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def get_posts(post_id=None):
    if post_id:
        try:
            post = Post.query.filter(Post.id == post_id).one()
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
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


def init_db():
    db.create_all()
    posts = Post.query.all()
    if len(posts) == 0:
        post_1 = Post("Post #1", "Test for the **content** with markdown")
        db.session.add(post_1)
        post_2 = Post("Post #2", "# Great news\nThis should be the first"
                      "_post_ in the list")
        db.session.add(post_2)
        db.session.commit()

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=3500, debug=True)
