from flask import render_template, request, Blueprint
from templates.hello.ServerLogic.Alignment_Check import *
from hello_template import socketIo
hello_blueprint = Blueprint('hello',__name__)
@hello_blueprint.route('/')
@hello_blueprint.route('/hello')
def index():
 return render_template("index.html")
@hello_blueprint.route('/result',methods = ['POST'])
def getQueryResult():
	q = request.form
	mLocations = Alignment_Check.getMatchingLocations(q)
	return render_template("result.html",result = mLocations)