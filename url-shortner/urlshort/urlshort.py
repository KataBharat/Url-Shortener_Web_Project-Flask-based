# this file is originally called app.py but name is changed since the app is created and returned from __init__.py

from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename 
#render_template is used to render html files or templates
#request is the get arguments from the request
# flash is used for displaying messages to the user

#app = Flask(__name__) #used to create the flask app 
#app.secret_key = 'jhjgrdytjbbjkhbcrsrdiiplknbc'  # random string which is a secret key for securing messages between website and user
#The above two lines are moved to __init__.py


bp = Blueprint('urlshort', __name__) # creating a blue print

# initially it was @app.route() but after introducing blue print it is @bp.route

@bp.route('/') # base url(home page)
def home():

    #return 'hello flask!'
    #return render_template('home.html')
    return render_template('home.html', codes = session.keys()) 
                                                

#@app.route('/about')
#def about():
#    return 'This is a url shortner'

@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls={}

        if os.path.exists('urls.json'):       # checking if already a json file is created
            with open('urls.json') as urls_file:
                urls=json.load(urls_file)
        
        if request.form['code'] in urls.keys():      # checking for duplicate entries
            flash('That short is already been taken. Please select another name') # this is message is to the template which is specified in the next line
            return redirect(url_for('urlshort.home'))  # the message is received and dispalyed in home.html using jinja format

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C://Users//bharat//projects//url-shortner//urlshort//static//user_files//' + full_name)
            urls[request.form['code']] = {'file': full_name}

        #urls[request.form['code']] = {'url':request.form['url']}  # code as key and url as value
        with open('urls.json','w') as url_file: # w stands for writing mode
            json.dump(urls,url_file)
            session[request.form['code']] = True  # instead of true we can even use a time stamp
        #return render_template('your_url.html', code=request.args['code'])  #args is a dictionary(should be used only for get request)
        return render_template('your_url.html', code=request.form['code']) #form is used to extract data from post request
    else:
        # return render_template('home.html') #when user directly opens your-url without going through home.html but
        # it shows your-url in the address bar but the user is shown home.html so we need to change the url 
        # return redirect('/') # used to redirect user to home page and the url is also changed
        # we may change the url so instead of specifying '/' we may redirect to the home function
        return redirect(url_for('urlshort.home')) 

@bp.route('/<string:code>') # any string after first / is brought into variable code
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files//' + urls[code]['file']))
    return abort(404) # to show no file or  url is found

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')  # creating api
def session_api():
    return jsonify(list(session.keys()))
