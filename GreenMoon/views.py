from datetime import datetime

from flask import render_template, url_for, request, session, redirect, abort, flash, jsonify, json
from werkzeug.security import check_password_hash

from GreenMoon import app, dbSQL
from GreenMoon.models import Account, Post, licenseFromZip, licenseRecommender


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            title='Home')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    id = 'page-top'
    return render_template('index.html',id='portfolio')

@app.route('/projects/blog')
def blog():
    posts = dbSQL.session.query(Post).all()
    return render_template('blog.html', posts = posts)

# define login
@app.route('/projects/blog/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        nickname = request.form['nickname']
        pwd = request.form['password']
        user = Account.query.filter_by(nickname=nickname).first()
        print(nickname)
        if user is None:
            error = 'Invalid nickname'
        elif check_password_hash(user.password_hash, pwd)==False:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['nickname'] = nickname
            flash('You were logged in')
            return redirect('/projects/blog')
    if error:
        flash(error)

    return render_template('login.html', error=error)

# define logout
@app.route('/projects/blog/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('nickname', None)
    flash('You were logged out')
    return redirect(url_for('blog'))

# define sign up page
@app.route('/sign')
def sign():
    return render_template('sign.html')

# define a page to add post after log-in
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    body = request.form['text']
    timestamp = datetime.now()
    nickname = session['nickname']
    post = Post(title=title, body=body, timestamp=timestamp, nickname=nickname)
    dbSQL.session.add(post)
    dbSQL.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('blog'))

@app.route('/projects/license', methods=['GET', 'POST'])
def license():
    if request.method == 'POST':
        post_zip = request.form['post_zip']
        searchResult = licenseFromZip(post_zip)
        recommendedLicense = licenseRecommender(post_zip)
        if recommendedLicense == []:
            recommendedLicense = 'Yay, our current tagging strategy suggests that business licenses are well balanced!'
        print(searchResult)
        print(recommendedLicense)

        if searchResult == "":
            searchResult = "No result found for ZIP: "+post_zip+" !"

        # jsonify recently started accepting list obj, require jsonify(items=[your list])
        return jsonify(searchResult=[searchResult],recommendedLicense=[recommendedLicense])

    return render_template('license.html')

@app.route('/projects/bikes')
def bikes():
    return render_template('bikes.html')

@app.route('/projects/twitter')
def twitter():
    return render_template('twitter.html')

@app.route('/research')
def research():
    return render_template('research.html',
                           title='Research')

# add a route to make zipcodeBoundaryChicago.geojson available
@app.route('/zipcodeBoundaryChicago.geojson')
def zipBoundary():
    return render_template('zipcodes.geojson',
                           title='Zip Boundary')
