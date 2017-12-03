import os
import re
from flask import Flask, render_template, url_for, send_from_directory, redirect

app = Flask(__name__)

#home page, only page for now lol
@app.route('/')
def home():
	apps_list = []
	for app in os.listdir("apps"):
		apps_list.append(app_info(app))
	return render_template("home.html",apps=apps_list)


#all redirect to home for now, ceebs adding
@app.route('/top')
def top():
	return redirect(url_for('home'))

@app.route('/new')
def new():
	return redirect(url_for('home'))

#given an app name, it returns the app icon
#idea taken from a stackoverflow post (:
@app.route('/uploads/<path:app_name>')
def download_file(app_name):
    dir = os.path.join(app_name,"icon.jpg")
    return send_from_directory("apps",dir)

#all functions that don't route to a webpage are below this
#(so basically helper functions)

#wrapper function to put all app details in a list
def app_info(app_name):
	app_info_list = [app_name]
	app_info_list.append(limit_desc(return_app_desc(app_name)))
	app_info_list.append(return_avg_rating(app_name))
	app_info_list.append(return_url(app_name))
	return app_info_list

#get app descritpion from file
def return_app_desc(app_name):
	app_desc_dir = os.path.join("apps",app_name,"description")
	try:
		f = open(app_desc_dir)
		return f.read()
	except IOError: #description doestn exist
		return "No App Description"

#limit the descrption length for boxes
def limit_desc(desc):
	if(len(desc) > 150):
		return desc[:147] + "..."
	else:
		return desc

#get average rating from list of ratings in txt document
def return_avg_rating(app_name):
	app_rating_dir = os.path.join("apps",app_name,"ratings")
	try:
		f = open(app_rating_dir)
		rating_sum = 0
		num_ratings = 0
		for line in f:
			if(re.match("^[0-5]$",line)):
				num_ratings += 1
				rating_sum += int(line)
		if(num_ratings == 0):#empty ratings file
			return "0/5(0)"
		avg = rating_sum/num_ratings 
		string = str(round(avg,2)) + "/5  (" + str(num_ratings) + ")"
		return string
	except IOError:
		return "0/5(0)"

#get url from file 
def return_url(app_name):
	app_url_dir = os.path.join("apps",app_name,"url")
	try:
		f = open(app_url_dir)
		url = f.readline()#should only be 1 line long on first line, so read only that
		return url
	except IOError:
		return "" #SHOULD NEVER GET HERE, THERE SHOULD ALWAYS BE A URL AT MINIMUM


if(__name__ == '__main__'):
	app.run(debug=True)
