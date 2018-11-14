import os
from flask import Flask, session,render_template,request,redirect,url_for,jsonify
from flask_session import Session
from API.resource_fetch import get_all_shows, get_show_details

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Routing methods
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/shows",methods=['GET'])
def list_show():
    all_show_list = get_all_shows()
    return jsonify(all_show_list)

@app.route("/api/show/<show_name>/",methods=['GET'])
def display_show(show_name):
    tv_show_detail = get_show_details(show_name)
    return jsonify(tv_show_detail)
