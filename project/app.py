from flask import request, Flask, render_template, redirect
from flask_pymongo import PyMongo

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["MONGO_URI"] = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == "GET"):
        return render_template("/pages/home.html")

    elif(request.method == "POST"):
        url = request.form['url']
        res = requests.get(url)
        res_html = res.content
        tags_soup = BeautifulSoup(res_html, 'html.parser')
        num_p_tags = len(tags_soup.find_all("p"))
        num_img_tags = len(tags_soup.find_all("img"))
        results = [num_p_tags, num_img_tags]
        return render_template("/pages/home.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)


# url="https://www.bbc.com/travel/article/20220228-italys-rare-surprisingly-bitter-honey"
