from flask import render_template, url_for, request, g, session, redirect, abort, flash, jsonify
from GreenMoon import app
from GreenMoon.db_init import dbSQL
from GreenMoon.models import Account, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from .models import allTupleFromDB, licenseFromZip
from .forms import inputZipForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            title='Home')

@app.route('/about')
def about():
    return render_template('about.html')

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
    title = request.form['title']
    body = request.form['text']
    post = Post(title=title, body=body)
    #
    # dbSQL.execute('insert into posts (id=title, body=text) values (?, ?)',
    #              [request.form['title'], request.form['text']])
    dbSQL.session.add(post)
    dbSQL.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('blog'))

@app.route('/dataprojects')
def dataprojects():
    return render_template('dataprojects.html',
                           title='Data Projects')

@app.route('/map1')
def map1():
    return render_template('leafletMap.html',
                           title='Data Map')

@app.route('/map')
def project2():
    return allTupleFromDB()

@app.route('/research')
def research():
    return render_template('research.html',
                           title='Research')

@app.route('/searchZip', methods=['GET', 'POST'])
def searchZip():
    form = inputZipForm()
    if form.validate_on_submit():
        #flash('Login requested for OpenID="%s" ' % (form.openid.data))
        session['selectedZip'] = form.inputZip.data
        return redirect('/licenseSearchResult')
    return render_template('searchZip.html', form=form)

@app.route('/licenseSearchResult')
def licenseSearchResult():
    selectedZip = session['selectedZip']
    if( selectedZip is None):
        return redirect('/licenseAnalysis.html')
    else:
        output = licenseFromZip(selectedZip)
        if (output == ""):
            searchResult = "Search result is null."
        else:
            searchResult = output

        return render_template('licenseSearchResult.html', title='Result',
          selectedZip = selectedZip, searchResult = searchResult)
