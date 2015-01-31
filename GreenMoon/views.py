from flask import render_template, url_for, request, g, jsonify
from GreenMoon import app
from .models import allTupleFromDB

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            title='Home')

# define a blog tab to show blog entries
@app.route('/blog')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('blog.html', entries=entries)

@app.route('/about')
def about():
    return 'Congrata! U have landed on the fancy moon in Chicago!'

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
