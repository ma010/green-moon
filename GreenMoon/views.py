"""
    This is the View module to
    control all the view functions
"""

from datetime import datetime
from flask import render_template, url_for, request, session, redirect, abort, flash, jsonify
from werkzeug.security import check_password_hash

from GreenMoon import app, dbSQL
from GreenMoon.models import Account, Post, license_from_zip, license_recommender


@app.route('/')
@app.route('/index')
def index():
    """
    This function defines the index page to be the Home page
    :return: index.html
    """
    return render_template('index.html', title='Home')


@app.route('/about')
def about():
    """
    This function defines the about page to
    introduce the website
    :return: about.html
    """
    return render_template('about.html')


@app.route('/projects')
def projects():
    """
    This function defines the projects page to
    show our portfolio of projects
    :return: portfolio section in index.html
    """
    id = 'page-top'
    return render_template('index.html', id='portfolio')


@app.route('/projects/blog')
def blog():
    """
    This function defines the blog page.
    Initial feature includes presenting all the posts.
    :return: return blog.html
    """
    posts = dbSQL.session.query(Post).all()
    return render_template('blog.html', posts=posts)


@app.route('/projects/blog/login', methods=['GET', 'POST'])
def login():
    """
    This function defines the login page
    :return: login.html
    """
    error = None

    if request.method == 'POST':
        nickname = request.form['nickname']
        pwd = request.form['password']
        user = Account.query.filter_by(nickname=nickname).first()
        print(nickname)
        if user is None:
            error = 'Invalid nickname'
        elif not check_password_hash(user.password_hash, pwd):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['nickname'] = nickname
            flash('You were logged in')
            return redirect('/projects/blog')
    if error:
        flash(error)

    return render_template('login.html', error=error)


@app.route('/projects/blog/logout')
def logout():
    """
    This functions defines the logout feature.
    Once logged out, user is redirected to the blog page.
    :return: blog.html
    """
    session.pop('logged_in', None)
    session.pop('nickname', None)
    flash('You were logged out')
    return redirect(url_for('blog'))


@app.route('/sign')
def sign():
    """
    This function defines the sign up page
    :return: sign.html
    """
    return render_template('sign.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """
    This function defines the add_entry feature for logged-in users.
    Once an entry is added, user is redirected to the blog page
    :return: blog.html
    """
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
    """
    This function defines the license page to
    show the analysis of business license information
    from City of Chicago data portal
    :return: license.html
    """
    if request.method == 'POST':
        post_zip = request.form['post_zip']
        searchResult = license_from_zip(post_zip)
        recommendedLicense = license_recommender(post_zip)
        if recommendedLicense == []:
            recommendedLicense = 'Yay, our current tagging strategy suggests ' \
                                 'that business licenses are well balanced!'
        print(searchResult)
        print(recommendedLicense)

        if searchResult == "":
            searchResult = "No result found for ZIP: "+post_zip+" !"

        # jsonify recently started accepting list obj, require jsonify(items=[your list])
        return jsonify(searchResult=[searchResult], recommendedLicense=[recommendedLicense])

    return render_template('license.html')


@app.route('/projects/bikes')
def bikes():
    """
    This functions defines a bikes page to
    show the analysis and visualization of
    divvy bike data
    :return: bikes.html
    """
    return render_template('bikes.html')


@app.route('/projects/twitter')
def twitter():
    """
    This function defines a twitter page to
    show the analysis and visualization of
    twitter data
    :return: twitter.html
    """
    return render_template('twitter.html')


@app.route('/research')
def research():
    """
    This function defines a research page to
    show the research projects our team members
    have done in the past. This page is still
    under development
    :return: research.html
    """
    return render_template('research.html', title='Research')


@app.route('/ChicagoZipcodeBoundary.geojson')
def zip_boundary():
    """
    This function adds a route to provide Chicago zip code boundary data,
    which primarily involves the latitude and longitude pairs.
    The data file is named as zipcodes.geojson.
    This makes the data readily available for javascript variables in license.js
    :return: zipcodes.geojson
    """
    return render_template('zipcodes.geojson', title='Zip Boundary')
