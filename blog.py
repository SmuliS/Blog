from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from database import db_session
from flask.ext.sqlalchemy import SQLAlchemy
from models import Post
import database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


@app.route('/')
def index():
    results = []
    tags = []
    temp = []
    counter = 0
    results = Post.query.all()
    for post in results:
        if(len(post.text) > 150):
            post.text = post.text[:150] + "..."
        post.tags = post.tags.split(",")
    return render_template('posts.html', result = results)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post = post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if(request.method == 'GET'):
        post = Post.query.get(post_id)
        return render_template('edit.html', post = post)
    else:
        new_title = request.form['title']
        new_text = request.form['text']
        new_tags = request.form['tags']
        post = Post.query.get(post_id)
        post.title = new_title
        post.text = new_text
        post.tags = new_tags
        db_session.commit()
        return redirect(url_for('index'))


@app.route('/tag/<tag_name>')
def search_by_tag(tag_name):
    hits = []
    posts = Post.query.all()
    for post in posts:
        try:
            if post.tags.count(tag_name) != 0:
                post.tags = post.tags.split(",")
                hits.append(post)
        except ValueError:
            print ("Voi Voi")
    return render_template('posts.html', result = hits)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if (request.method == 'POST'):
        if (request.form['password'] == 'kayttaja') and (request.form['username'] == 'testi'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error_message = "Invalid username / password !"

    return render_template('login.html', error=error_message)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/add_new_post', methods=['GET', 'POST'])
def add_new_post():
    try:
        session['username']
    except KeyError:
        error_message = "Log in before posting"
        return render_template('login.html', error=error_message)
    if request.method == 'GET':
            return render_template('add_new_post.html')
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        tags = request.form['tags']
        post = Post(title, text, tags)
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('index'))


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


def parse_tags(tags):
    parsed_tags = tags.split(",");
    return parsed_tags

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run()
