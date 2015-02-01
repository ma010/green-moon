from flask import render_template, url_for, request, g, session, redirect, abort, flash, jsonify
from GreenMoon import app
from .models import dbSQL, Account, Post
from werkzeug.security import generate_password_hash, check_password_hash
from .models import allTupleFromDB

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            title='Home')

@app.route('/about')
def about():
    return 'Congrata! U have landed on the fancy moon in Chicago!'

# define a blog tab to show blog entries
@app.route('/blog')
def blog():
    #cur = g.db.execute('select postTitle, postBody from User order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('blog.html')#, entries=entries)

# define login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        nickname = request.form['nickname']
        pwd = request.form['password']
        user = Account.query.filter_by(nickname=nickname).first()
        if user is None:
            error = 'Invalid nickname'
        elif check_password_hash(user.password_hash, pwd)==False:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('blog'))
    return render_template('login.html', error=error)

# define logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('blog'))


# define a page to add post after log-in
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    dbSQL.execute('insert into User (postTitle, postBody) values (?, ?)',
                 [request.form['postTitle'], request.form['postBody']])
    dbSQL.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('blog'))

@app.route('/project1')
def project1():
    return render_template('project1.html',
                           title='Project')

@app.route('/project2')
def project2():
    return allTupleFromDB()

@app.route('/research')
def research():
    return render_template('research.html',
                           title='Research')

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
