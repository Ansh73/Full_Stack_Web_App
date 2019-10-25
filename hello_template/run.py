#from templates import app
#from flask_socketio import SocketIO, emit
#Load this config object for development mode
#app.config.from_object('configurations.DevelopmentConfig')
#turn the flask app into a socketio app
#socketio = SocketIO(app)

#@socketio.on('connect', namespace='/test')
#def test_connect():
#    print('Client connected')
	
#@socketio.on('disconnect', namespace='/test')
#def test_disconnect():
#    print('Client disconnected')

#app.run()
#socketio.run(app)


from flask import Flask
from flask_socketio import SocketIO, emit
#from templates.hello.ServerLogic.Alignment_Check import *
from templates.hello.ServerLogic.Alignment_Check import *
from flask import render_template, request, redirect, url_for, session, Blueprint
import flask_login
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
import asyncio
import aiohttp
from quart import Quart, jsonify
#from quart import (
#     abort, redirect, render_template, request, session,
#     url_for,
# )
import async_timeout
#import redis

application = Flask(__name__, static_folder = './templates/public', template_folder="./templates/static")
#application = Quart(__name__, static_folder = './templates/public', template_folder="./templates/static")
application.config.from_object('configurations.DevelopmentConfig')
#app.config['SESSION_TYPE'] = 'super secret key'
#application.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
sess = Session()
sess.init_app(application)
socketio = SocketIO(application)
#db = SQLAlchemy()
login_manager = LoginManager()
loop = asyncio.get_event_loop()
loop.set_debug(1)
# Our mock database.
users = {'admin': {'password': 'admin'}}


#db.init_app(app)
login_manager.init_app(application)

#turn the flask app into a socketio app
#socketio = SocketIO(app)
#from templates.hello.views import hello_blueprint
# register the blueprints
#app.register_blueprint(hello_blueprint)
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
	email = request.form.get('email')
	if email not in users:
		return

	user = User()
	user.id = email
    #DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
	user.is_authenticated = request.form['password'] == users[email]['password']
	return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@application.route('/',methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		if "username" in session:
			return redirect(url_for('index'))
		else:	
			return '''
               <form action='/' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
	email = request.form['email']
	#users = {'admin': {'password': 'admin'}}
	if request.form['password'] == users[email]['password']:
		#session["user_email"] = {email : {'pv':[]}}
		#session["user_email"][email]['pv'].append ("123")
		#session["user_email"] = "anshul"
		session["username"] = email
		user = User()
		user.id = email
		flask_login.login_user(user)
		return redirect(url_for('index'))

@application.route('/logout')
def logout():
	session.pop('username', None)
	flask_login.logout_user()
	return 'Logged out'

@application.route('/search',methods = ['GET'])
@flask_login.login_required
def index():
    #only by sending this page first will the client be connected to the socketio instance
	#previousData = []
	#svt = session.get("user_email", "dummy").get(
	#sv = session["user_email"]
	#print("Anshul found email in session variable " + sv)
	return render_template('index.html', previousSearches = session.get('pv', " "))

@application.route('/search',methods = ['POST'])
@flask_login.login_required
def getQueryResult():
	q = request.form
	if 'pv' not in session:
		session['pv'] = []
	pv_list = session['pv']
	if len(pv_list)>10:
		pv_list.clear()
	pv_list.append(q.get("Name", "dummy"))
	session['pv'] = pv_list
	myObj = Alignment_Check()
	res_temp = {'nc_009899':[1]}
	mLocations_s = loop.create_future()
	mLocations_s.set_result(res_temp)
	#try:
	mLocations_s = loop.run_until_complete(myObj.getMatchingLocations(q.get("Name"), loop))
	#except Exception as e:
	#	print(e)
	#finally:
#		loop.close()
	socketio.emit('newnumber', {'start':'2', 'end':'3'}, namespace='/test')
	return render_template("index.html", result=mLocations_s.result(), previousSearches = pv_list, length = (len(q.get("Name")) - 1))
	#return render_template("result.html",result = mLocations)
	#return ' ', 204

@socketio.on('connect', namespace='/test')
def test_connect():
	print('Client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected')

async def my_main():
	application.run()
if __name__ == '__main__':
    socketio.run(application)
	#application.run()
	#asyncio.run(my_main())
	#loop = asyncio.get_event_loop()
	#loop.set_debug(1)
	#loop.run_until_complete(main())