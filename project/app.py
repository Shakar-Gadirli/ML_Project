import certifi
import requests
from bs4 import BeautifulSoup
import string


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


mongodb_client = PyMongo(app, tlsCAFile=certifi.where())
db = mongodb_client.db


def download_images(soup, url, img_size):
    dir_name = url.split("//")[1].replace('.', '_').replace("/", "_")
    cwd = os.getcwd()
    full_path = os.path.join("./static/images/", dir_name)
    # print("FULL PATH", full_path)

    size = (img_size, img_size)

    img_paths = []

    if not os.path.exists(full_path):
        os.mkdir(full_path)

    c = 1
    for image in soup.find_all("img"):
        source = image["src"]
        if "http" in source:
            # .convert("RGB")
            img = Image.open(requests.get(source, stream=True).raw)
            img.thumbnail(size)
            ext = str(img.format).lower()
            filename = f"image_{c}.{ext}"
            c = c + 1
            img.save(os.path.join(full_path, filename))
            img_paths.append(f"{full_path}/{filename}")

    return img_paths


def get_list_of_paragraphs(url):
    res = requests.get(url)
    res_html = res.content

    tags_soup = BeautifulSoup(res_html, 'html.parser')
    num_img_tags = len(tags_soup.find_all("img"))
    url_content = tags_soup.get_text()

    splat = url_content.split("\n")

    paragraphs = []
    all_splitted_paragraphs = []
    word_counts = []
    for i in splat:
        if i not in ('', ' ', '\r', '\n', '\r\n', '\n\r'):
            paragraphs.append(i)
            one_sanitized_p = i.translate(
                str.maketrans('', '', string.punctuation))
            all_splitted_paragraphs.append(
                [e for e in one_sanitized_p.split()])
            word_counts.append(len(i.split()))

    # print("~"*50)
    # print(all_splitted_paragraphs)
    # print("~"*50)
    return all_splitted_paragraphs, paragraphs, word_counts, num_img_tags


def par_threshold(pars, numss, threshold):

    len_numss = len(numss)
    # print(numss)

    numss.append(threshold)
    pars.append('')
    new_paragraphs = []

    i = 0
    while i < len_numss:
        if numss[i] >= threshold:
            new_paragraphs.append(pars[i])
            i += 1
        else:
            new_num = numss[i]
            new_p = pars[i]

            while new_num < threshold:
                i += 1
                new_num += numss[i]
                new_p = new_p + ' ' + pars[i]

            new_paragraphs.append(new_p)
            i += 1

    new_word_count = []
    for i in new_paragraphs:
        new_word_count.append(len(i.split()))

    # print(new_word_count)
    # print(len(new_word_count))
    # print(len(new_paragraphs))

    if (new_word_count[-1] < threshold):
        new_word_count[-2] = new_word_count[-2] + new_word_count[-1]
        new_word_count.pop()
        new_paragraphs[-2] = new_paragraphs[-2] + ' ' + new_paragraphs[-1]
        new_paragraphs.pop()

    return new_paragraphs, len(new_word_count)


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == "GET"):
        return render_template("/pages/home.html")

    elif(request.method == "POST"):

        url = request.form['url']
        threshold = int(request.form['threshold'])
        img_size = int(request.form['img_size'])
        image = request.files.get('image', '')
        image = request.form["image"]
        print(image)


        if not validators.url(url):
            error_msg = "You must provide a valid URL!"
            return render_template("/pages/home.html", error=error_msg)
        else:
            splitted_pars, pars, numss, num_img_tags = get_list_of_paragraphs(
                url)
            print(splitted_pars)
            r_par, r_num = par_threshold(pars, numss, threshold)
            results = [r_num, num_img_tags]
            # download image function -> will return image path
            # to fix
            res = requests.get(url)
            res_html = res.content
            tags_soup = BeautifulSoup(res_html, 'html.parser')
            image_paths = download_images(tags_soup, url, img_size)
            print('++++++++++++++++')

            # after getting returns save results to db.
            # if url does not exist in db, write to db
            if not db.articles.find_one({"url": url}):
                print('======================')
                db.articles.insert_one(
                    {"url": url, "image_paths": image_paths, "paragraphs": splitted_pars})
                print('---------------------')

            return render_template("/pages/home.html", results=results)


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if(request.method == "POST"):
        results = []
        image = request.files['image']
        full_name = f"../static/images/{image.filename}"
        results.append(full_name)
        name = image.filename.split("_")[0]
        animals = ['cat','dog','chicken','horse','goose','cow','camel','elephant','lion','giraffe','zebra']
        object = ['mountain','car','house','pen','tree']

        if  name in animals:
            results.append('animal')
        else:
            results.append('object')
      
    return render_template("/pages/classes.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
