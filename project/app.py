import bson
from flask import request, Flask, render_template, redirect
from flask_pymongo import PyMongo

from PIL import Image
import os
import requests
import validators
from bs4 import BeautifulSoup

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://mlproject:mlproject@cluster0.5uzjt.mongodb.net/MLPROJECT?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db


def download_images(soup,url):
    size = 28, 28    
    dir_name = url.split("//")[1].replace('.', '_').replace("/","_")
    cwd = os.getcwd()
    full_path = os.path.join("./static/images/",dir_name)
    print("FULL PATH", full_path)

    img_paths = []

    if not os.path.exists(full_path):
        os.mkdir(full_path)

    c = 1
    for image in soup.find_all("img"):
        source =  image["src"]
        if "http" in source:
            img = Image.open(requests.get(source, stream = True).raw) #.convert("RGB")
            img.thumbnail(size)
            ext = str(img.format).lower()
            filename = f"image_{c}.{ext}"
            c = c + 1
            img.save(os.path.join(full_path, filename))
            img_paths.append(f"{full_path}/{filename}")
    
    return img_paths


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
            image_paths = download_images(tags_soup,url)

            # after getting returns save results to db.
            # if url does not exist in db, write to db
            if not db.articles.find_one({"url": url}):
                db.articles.insert_one({"url":url,"image_paths":image_paths,"paragraphs":["p1","p2","p3"]})

            return render_template("/pages/home.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)


# url="https://www.bbc.com/travel/article/20220228-italys-rare-surprisingly-bitter-honey"
