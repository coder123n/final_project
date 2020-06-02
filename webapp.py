from flask import Flask, redirect, url_for, session, request, jsonify, Markup
from flask_oauthlib.client import OAuth
from flask import render_template
from flask import flash

import pprint
import os
import sys

username_list=[]
user_follow=[]

app = Flask(__name__)

app.debug = False #Change this to False for production

app.secret_key = os.environ['SECRET_KEY'] 
oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], 
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
	
)

@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))

@app.route('/logout')
def logout():
    session.clear()
    return render_template('message.html', message='You were logged out')

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            #save user data and set log in message
            session['github_token'] = (resp['access_token'], '')
            session['user_data'] = github.get('user').data
            message = 'You were successfully logged in as ' + session['user_data']['login'] + '.'

        except Exception as inst:
            #clear the session and give error message
            session.clear()
            print(inst)
            message = 'Unable to login. Please try again.'
    return render_template('message.html', message=message)


@app.route('/france1', methods=['GET','POST'])
def renderPage1():
	if session['github_token'] = (resp['access_token'], ''):
	return render_template('france1.html')

@app.route('/japan2', methods=['GET','POST'])
def renderPage2():
	return render_template('japan2.html')

@app.route('/zimbabwe3', methods=['GET','POST'])
def renderPage3():
	return render_template('zimbabwe3.html')


@github.tokengetter
def get_github_oauth_token():
    return session['github_token']


if __name__ == '__main__':
    app.run()
