# Author: ShadowSaint (Keerthan Bhat)
# This the the backend program for Travelore, web application written using Flask micro web framework using Python.

# imports
import os
import sqlite3
#from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
        
# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# get object for using the database
conn = sqlite3.connect('places.db')
c = conn.cursor()

# configure CS50 Library to use SQLite database
#c = SQL("sqlite:///places.db")

# home route
@app.route("/")
def home():
    return render_template("home.html")
    
# about route
@app.route("/about")
def about():
    return render_template("about.html")

# search route    
@app.route("/search", methods=["GET", "POST"])
def search():
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get the data from the html form
        place = request.form.get("place")
        dist = request.form.get("dist")
        ptype = request.form.get("type")
        
        
        # data from the dropdown
        if ptype == '1':
            ptype = "Hill station"
        elif ptype == '2':
            ptype = "Birds sanctuary"
        elif ptype == '3':
            ptype = "Piligrim"
        elif ptype == '4':
            ptype = "River"
        elif ptype == '5':
            ptype = "Water fall"
        elif ptype == '6':
            ptype = "Archeology"
        elif ptype == '7':
            ptype = "Dam"
        elif ptype == '8':
            ptype = "Landscape"
        elif ptype == '9':
            ptype = "Others"
        
        
        # Errors messages
        if not place and not dist and not ptype:
            return apology("Nothing was entered!")

        elif place and dist:
            return apology("Enter either place or distance limit, not both!")
        
        elif dist and ptype:
            return apology("Enter either distance limit or place type, not both!")
        
        elif place and ptype:
            return apology("Enter either place or place type, not both!")
            
        
        # search by place name or id no.
        if not dist and not ptype:
            
            # for places with similar spellings  
            place1 = place + "%"

            data = c.execute("SELECT * FROM place WHERE place LIKE :place OR no = :no", place = place1, no = place)
            
            if not data:
                return apology("Sorry! %s not found in the database." %place)
            
            # if multiple places are found
            if len(data) > 1:
                return render_template("list.html", datas = data)
            
            
            # get the detailed info
            info = c.execute("SELECT * FROM info WHERE no = :no", no = data[0]["no"])
            extras = c.execute("SELECT * FROM extras WHERE no = :no", no = data[0]["no"])
            
            # and send it to the html page
            return render_template("place.html", datas = data, infos = info, extras = extras)
        
        # search by distance limit
        if not ptype and not place:
        
            data = c.execute("SELECT * FROM place WHERE distance <= :dist", dist = dist)
            
            if not data:
                return apology("Sorry! Distance limit is too small.")
            
            return render_template("list.html", datas = data) 
            
        # search by place type
        if not place and not dist:
            
            if ptype == "Others":
                data = c.execute("SELECT * FROM place WHERE type = 'Hill' OR type = 'Wildlife' OR type = 'Ravine' OR type = 'Temple Paintings' OR type = 'Historical' OR type = 'Barrage' OR type = 'Beach' OR type = 'Caves'")
            else:
                data = c.execute("SELECT * FROM place WHERE type = :ptype", ptype = ptype)
            
            if not data:
                return apology("Sorry! No place of %s type found in the database." %ptype)
            
            return render_template("list.html", datas = data)
    
    # if the method is GET
    else:    
        return render_template("search.html")
