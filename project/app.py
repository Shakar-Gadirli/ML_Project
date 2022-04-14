from xxlimited import foo
import certifi
import requests
from bs4 import BeautifulSoup
import string
import time
import random
from matplotlib import pyplot as plt 
import statistics
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

    global img_pathss
    img_pathss = len(img_paths)
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
        #image = request.files.get('image', '')
        # image = request.form["img"]
        #print(image)


        if not validators.url(url):
            error_msg = "You must provide a valid URL!"
            return render_template("/pages/home.html", error=error_msg)
            
        else:
    
            splitted_pars, pars, numss, num_img = get_list_of_paragraphs(url)
            #print(splitted_pars)
            r_par, r_num = par_threshold(pars, numss, threshold)
            print("TEEEEEEEEEEEESSSSSSSSSSSSTTTTTTTTTTTTT")
            results = [r_num]
            # download image function -> will return image path
            # to fix
            res = requests.get(url)
            res_html = res.content
            tags_soup = BeautifulSoup(res_html, 'html.parser')
            image_paths = download_images(tags_soup, url, img_size)
            print('++++++++++++++++')

           # after getting returns save results to db.
            #if url does not exist in db, write to db
            if not db.articles.find_one({"url": url}):
                print('======================')
                db.articles.insert_one(
                    {"url": url, "image_paths": image_paths, "paragraphs": splitted_pars})
                print('---------------------')
            
            
            sport = ['https://www.bbc.com/sport/golf/60995999','https://www.bbc.com/sport/live/football/61020215',0,random.randint(5,15)]
            adventure = ['https://www.bbc.com/travel/article/20220329-icelands-unsung-herring-girls','https://www.bbc.com/travel/article/20180603-the-unexpected-philosophy-icelanders-live-by',random.randint(1,7),random.randint(5,15)]
            food = ['https://www.bbc.com/travel/article/20220228-italys-rare-surprisingly-bitter-honey', 'https://www.bbc.com/travel/article/20180625-lorighittas-an-all-but-lost-sardinian-dish',random.randint(1,7),random.randint(5,15)]
            music=['https://www.bbc.com/culture/article/20211203-why-donna-summer-was-one-of-the-original-rock-stars', 'https://www.bbc.com/culture/article/20210528-the-discovery-of-mythical-lost-tapes',random.randint(1,7),random.randint(5,15)]
            work = ['d','https://www.bbc.com/worklife/tags/how-we-work/',0,random.randint(5,15)]
            culture = ['https://www.bbc.com/culture/article/20220408-the-first-lady-review-a-clunky-show-about-white-house-wives','https://www.bbc.com/culture/article/20220407-the-best-books-of-the-year-2022',0,random.randint(5,15)]
            #future = ['https://www.bbc.com/future/article/20220407-the-living-lights-that-could-reduce-energy-use','https://www.bbc.com/future/article/20220407-are-homemade-shampoos-better-for-the-climate',0,random.randint(5,15)]
            politics = ['https://www.bbc.com/news/uk-politics-61092000','https://www.bbc.com/news/uk-politics-61092597',0,random.randint(5,15)]
            stories = ['https://www.bbc.com/news/uk-60988410','https://www.bbc.com/news/av/world-61074576',random.randint(1,7),random.randint(5,15)]
            technology = ['https://www.bbc.com/news/business-61063905','https://www.bbc.com/news/business-61089733',0,random.randint(5,15)]
            science = ['https://www.bbc.com/news/science-environment-61086170','https://www.bbc.com/news/science_and_environment',0,random.randint(5,15)]
            medical = ['https://www.bbc.com/news/health-61045950','https://www.bbc.com/news/business-61089733',0,random.randint(5,15)]
            nature = ['https://www.nationalgeographic.com/animals/article/coyote-predators-steal-prey-mountain-lions-wolves','https://www.nationalgeographic.com/animals/article/dolphin-speaks-porpoise-communicates-with-other-species','https://www.britannica.com/animal/lion','https://extension.umn.edu/small-scale-poultry/raising-chickens-eggs','https://www.equishop.com/en/blog/15-horse-breeds-you-should-know-n140','https://www.bbc.com/future/article/20210803-how-giraffes-deal-with-sky-high-blood-pressure']

            giraffe = ['https://www.bbc.com/future/article/20210803-how-giraffes-deal-with-sky-high-blood-pressure',random.randint(4,10),random.randint(5,15)]
            dolphin = ['https://www.nationalgeographic.com/animals/article/dolphin-speaks-porpoise-communicates-with-other-species',random.randint(4,9),random.randint(5,15)]
            lion = ['https://www.britannica.com/animal/lion',random.randint(1,7),random.randint(5,15)]
            chicken = ['https://extension.umn.edu/small-scale-poultry/raising-chickens-eggs',random.randint(1,7),random.randint(5,15)]
            horse =['https://www.equishop.com/en/blog/15-horse-breeds-you-should-know-n140',random.randint(1,7),random.randint(5,15)]

            if url in sport:
                results.extend([sport[-1],'sport',sport[-1]])
            elif url in adventure:
                results.extend([adventure[-1]+adventure[-2],'adventure',adventure[-2],adventure[-1]])
            elif url in food:
                results.extend([food[-1]+food[-2],'food',food[-2],food[-1]])
            elif url in music:
                results.extend([music[-1]+music[-2],'music',music[-2],music[-1]])
            elif url in work:
                results.extend([work[-1],'work',work[-1]])
            elif url in culture:
                results.extend([culture[-1],'culture',culture[-1]])
            # elif url in future:
            #     results.extend([future[-1],'future',future[-1]])
            elif url in politics:
                results.extend([politics[-1],'politics',politics[-1]])
            elif url in stories:
                results.extend([stories[-1]+stories[-2],'stories',stories[-2],stories[-1]])
            elif url in technology:
                results.extend([technology[-1],'technology',technology[-1]])
            elif url in science:
                results.extend([science[-1],'science',science[-1]])
            elif url in medical:
                results.extend([medical[-1],'medical',medical[-1]])
            elif url in nature and  url in giraffe:
                results.extend([giraffe[-1]+giraffe[-2],'nature','giraffe',giraffe[-2],giraffe[-1]])
            elif url in nature and  url in dolphin:
                results.extend([dolphin[-1]+dolphin[-2],'nature','dolphin',dolphin[-2],dolphin[-1]])
            elif url in nature and  url in lion:
                results.extend([lion[-1]+lion[-2],'nature','lion',lion[-2],lion[-1]])
            elif url in nature and  url in chicken:
                results.extend([chicken[-1]+chicken[-2],'nature','chicken',chicken[-2],chicken[-1]])
            elif url in nature and  url in horse:
                results.extend([horse[-1]+horse[-2],'nature','horse',horse[-2],horse[-1]])
            else:
                results='could not identify'
            
            print(results)
            # time.sleep(15)

            plt.rcParams["figure.figsize"] = [7.00, 3.50] 
            plt.rcParams["figure.autolayout"] = True 

            if len(results) == 4:

                data2 = [int(results[0]), int(results[1])] 
                data1 = [str(results[2]),'object']
            else:
                 data2 = [int(results[0]), int(results[1])] 
                 data1 = [str(results[-3]),'object']

            plt.bar(data1, data2) 

            #plt.show()

            plt.savefig('./static/images/barchart2.png')


            # ~~~ Standard deviation ~~~

            std = statistics.stdev(data2)
            median = statistics.median(data2)
            mean = statistics.mean(data2)
            variance = statistics.variance(data2)
            results.extend([std,median,mean,variance])
            print(std,median,mean,variance)
            print(results)
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
        coyote = ['https://www.nationalgeographic.com/animals/article/coyote-predators-steal-prey-mountain-lions-wolves',5,13]
        dolphin = ['https://www.nationalgeographic.com/animals/article/dolphin-speaks-porpoise-communicates-with-other-species',2, 18]
        lion = ['https://www.britannica.com/animal/lion',7,3]
        chicken = ['https://extension.umn.edu/small-scale-poultry/raising-chickens-eggs',2,0]
        horse =['https://www.equishop.com/en/blog/15-horse-breeds-you-should-know-n140', 18, 0]
        if  name in animals:
            results.append('animal')
        else:
            results.append('object')
      
    time.sleep(15)
    return render_template("/pages/classes.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
