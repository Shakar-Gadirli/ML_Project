import bson
from flask import request, Flask, render_template, redirect
from flask_pymongo import PyMongo

import os
import requests
import validators
from bs4 import BeautifulSoup

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://mlproject:mlproject@cluster0.5uzjt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db

'''
def download_image(soup):
	UPLOAD_FOLDER = "./images"
	for image in soup.find_all("img"):
		source =  image["src"]
		img = Image.open(requests.get(image_url, stream = True).raw)
		filename = secure_filename(img.filename)
		img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return path #bu image pathi goturub db-ya ataq
'''		

@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == "GET"):
        return render_template("/pages/home.html")

    elif(request.method == "POST"):
        
        url = request.form['url']
		
        if not validators.url(url):
            error_msg = "You must provide a valid URL!"
            return render_template("/pages/home.html", error=error_msg)
        else:

            res = requests.get(url)
            res_html = res.content
            tags_soup = BeautifulSoup(res_html, 'html.parser')
            num_p_tags = len(tags_soup.find_all("p"))
            num_img_tags = len(tags_soup.find_all("img"))
            results = [num_p_tags, num_img_tags]
			
			
			# download paragraphs function -> will return paragraphs that will be stored on the db
			# download image function -> will return image path
			# 
			# after getting returns save results to db.

            return render_template("/pages/home.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)


# url="https://www.bbc.com/travel/article/20220228-italys-rare-surprisingly-bitter-honey"
