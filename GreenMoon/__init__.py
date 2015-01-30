from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
from pymongo import Connection

app = Flask(__name__)
con = Connection()
db = con.businessDB

from GreenMoon import views
