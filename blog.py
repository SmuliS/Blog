from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('posts.html')


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
            error_message = 1

    return render_template('login.html', error=error_message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run()
