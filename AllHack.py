#!flask/bin/python

import sys
sys.path.append("C:\User\Admin\Desktop\HACKMIT\RAKE-tutorial")
import rake
import operator
import requests
from urllib2 import Request, urlopen, URLError
import pprint
from flask import Flask, render_template, request, url_for, json, redirect
from bs4 import BeautifulSoup
import re
import scraper
import urllib

# EXAMPLE ONE - SIMPLE
stoppath = "SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 2, 2, 1)

# 2. run on RAKE on a given text
#sample_file = open("HackMit.txt", 'r')
#text = sample_file.read()

#keywords = rake_object.run(text)
# 3. print results
#print "Keywords:", keywords

app = Flask(__name__)

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

def get_image_url(keyword):
    print keyword
    common_url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=images&format=json"
    r = requests.get(common_url.format(keyword))
    wiki = r.json()
    images = wiki["query"]["pages"].values()[0]["images"]
    urls = list()
    for image in images:
        title = image["title"]
        wiki_url = "https://commons.wikimedia.org/wiki/{}"
        r = urllib.urlopen(wiki_url.format(title)).read()
        soup = BeautifulSoup(r, "html.parser")
        try:
            full_image_div = soup.find_all("div", class_="fullImageLink")[0]
            url = full_image_div.a["href"]
            if url.split(".")[-1] in ["jpeg", "jpg", "png"]:
                return url
        except IndexError:
            pass
    raise Exception("No image found")


"""
sentenceList = rake.split_sentences(text)
keywordInSent=[]
print sentenceList[0]
for i1 in range(len(sentenceList)-1):
    #print i1
    #print sentenceList[i1]
    keywords1 = rake_object.run(sentenceList[i1])
    #pprint.pprint(keywords)
    #print len(keywords)
    
    for i2 in range(len(keywords1)):
        ss1= keywords1[i2][0]
        print ss1
        url_image=get_image_url(ss1)
        #print ss1
"""          
    

@app.route('/')
def index():
    print("Yayyyy")
    return render_template('index.html')

@app.route('/right-sidebar', methods=["GET", "POST"])
def side_index():
    if request.method == "GET": 
	return render_template("right-sidebar.html")
    else:
	fileField = request.form['fileField'].strip()
	print(fileField)
	sample_file = open(fileField, 'r')
	text = sample_file.read()
	sentenceList = rake.split_sentences(text)
	keywordInSent=[]
	print sentenceList[0]
	for i1 in range(len(sentenceList)-1):
    	#print i1
    	#print sentenceList[i1]
    		keywords1 = rake_object.run(sentenceList[i1])
    	#pprint.pprint(keywords)
    	#print len(keywords)
    
    	'''for i2 in range(len(keywords1)):
        	ss1= keywords1[i2][0]
        	print ss1'''
        	
        ss1=keywords1[1][0]
	url_image=get_image_url(ss1)
	print url_image
	return redirect(url_image)
	#return render_template('right-sidebar.html')
    

@app.route('/home')
def home():
    print "Rendering"
    return render_template('left-sidebar.html')

@app.route('/wePage')
def intro():
    print "Inside Intro"
    return render_template('no-sidebar.html')


@app.route('/wePage', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        print "POST Request Successful"
        name=request.form['fname']
        request.files['file'].save('file.txt')
        points=processImage()
        #width, height= points.shape
        print "returned"
        #data=json.dumps(points)
        #data=json.dumps(points)
        #data=map(json.dumps, points)
        #return render_template('canvas.html',points=points,row = row, col = col,width=width,height=height)
        return"Success"
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
        print 'saving'
        save(request.files['upload'])
        return redirect(url_for('wePage.html'))
    return (
        u'<form method="POST" enctype="multipart/form-data">'
        u'  <input name="upload" type="file">'
        u'  <button type="submit">Upload</button>'
        u'</form>'
    )

if __name__ == "__main__":
    app.run()