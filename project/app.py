from flask import request, Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == "GET"):
        return render_template("/pages/home.html")

    elif(request.method == "POST"):
        url = request.form['url']
        # take url scrape and return result to home page
        # result = returned scraping result
        return render_template("/pages/home.html", result=result)
