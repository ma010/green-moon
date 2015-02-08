from datetime import datetime

from flask import render_template, url_for, request, session, redirect, abort, flash
from werkzeug.security import check_password_hash

from GreenMoon import app
from db_init import dbSQL
from GreenMoon.models import Account, Post, allTupleFromDB, licenseFromZip
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
@app.route('/projects/blog')
def blog():
    posts = dbSQL.session.query(Post).all()
    return render_template('blog.html', posts = posts)

@app.route('/projects/license', methods=['GET', 'POST'])
def license():
    form = inputZipForm()
    if form.validate_on_submit():
        #flash('Login requested for OpenID="%s" ' % (form.openid.data))
        session['selectedZip'] = form.inputZip.data
        return redirect('/projects/license/licenseSearchResult')
    return render_template('license.html', title='Data Map', form=form)

@app.route('/projects/license/licenseSearchResult')
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

@app.route('/projects/twitter')
def twitter():
    return render_template('twitter.html')

# define sign up page
@app.route('/sign')
def sign():
    return render_template('sign.html')

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
            session['nickname'] = nickname
            flash('You were logged in')
            return redirect(url_for('blog'))
    return render_template('login.html', error=error)

# define logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('nickname', None)
    flash('You were logged out')
    return redirect(url_for('blog'))


# define a page to add post after log-in
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    body = request.form['text']
    timestamp = datetime.now()
    nickname = session['nickname']
    post = Post(title=title, body=body, timestamp = timestamp, nickname = nickname)
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


@app.route('/map')
def project2():
    return allTupleFromDB()

@app.route('/divvyBikeProject')
def divvyBikeProject():
    return render_template('divvyBikeProject.html')

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

# add a route to make zipcodeBoundaryChicago.geojson available
@app.route('/zipcodeBoundaryChicago.geojson')
def zipBoundary():
    return render_template('zipcodes.geojson',
                           title='Zip Boundary')
