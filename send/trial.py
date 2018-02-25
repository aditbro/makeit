from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import RentList, Base

engine = create_engine('sqlite:///tabletennis.db')
Base.metadata.bind = engine

@app.route('/', methods = ['GET','POST'])
def mainpage():
	return render_template('main.html')

@app.route('/about', methods = ['GET','POST'])
def about():
	return render_template('about.html')

@app.route('/sign_up', methods = ['GET','POST'])
def daftar():
	if request.method == 'POST':
		pass
	else:
		return render_template('sign_up.html')

@app.route('/be_a_seller', methods = ['GET','POST'])
def daftar_seller():
	if request.method == 'POST':
		pass
	else:
		return render_template('be_a_seller.html')

@app.route('/profile', methods=['GET'])
def profile():
	return render_template('profile.html')

DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host ='0.0.0.0', port=80)