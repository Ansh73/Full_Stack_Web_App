from flask import Flask
from flask_socketio import SocketIO, emit
from templates.hello.ServerLogic.Alignment_Check import *
app = Flask(__name__, static_folder = './public', template_folder="./static")
#turn the flask app into a socketio app
socketio = SocketIO(app)
#from templates.hello.views import hello_blueprint
# register the blueprints
#app.register_blueprint(hello_blueprint)
@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')
@app.route('/result',methods = ['POST'])
def getQueryResult():
	q = request.form
	mLocations = Alignment_Check.getMatchingLocations(q)
	socketio.emit('newnumber', {'number': number}, namespace='/test')
	#return render_template("result.html",result = mLocations)

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
