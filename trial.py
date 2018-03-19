from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
import flask_login
import os
import datetime
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Article, ShopPhoto, ShopTag, Tags, Base, Shop, ArticlePhoto
from werkzeug.utils import secure_filename

#HTML TEMPLATE
#########################################################
nav = '''<nav class="navbar navbar-expand-lg navbar-dark fixed-top justify-content-between">
      <a href="/" class="navbar-brand" style="font-family: 'Farsan', cursive;"><img id="logo" src="/static/img/logo-trimmed.png" /></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link {}" href="/about">About Us</a>
          </li>
          <li class="nav-item">
            <a class="nav-link {}" href="/">Our Partner</a>
          </li>
          <li class="nav-item">
            <a class="nav-link {}" href="/category">Category</a>
          </li>
          <li class="nav-item">
            <a class="nav-link {}" href="/profile">Explore</a>
          </li>
          <li class="nav-item not-logged-in">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item mr-sm-2 not-logged-in">
            <a class="btn btn-nav" href="/sign_up">Sign Up!</a>
          </li>
          <div class="dropdown show logged-in">
            <a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><img style="height:30px;width:auto" src="https://cdn1.iconfinder.com/data/icons/mix-color-3/502/Untitled-7-512.png" class="img-responsive"/></a><span class="caret"></span>
            <div class="dropdown-menu dropdown-menu-right" role="menu" aria-labelledby="menu1">
              <a class="dropdown-item" href="/shop">Shop</a>
              <a class="dropdown-item" href="/logout">Logout</a>
            </div>
          </div>
        </ul>
      </div>
    </nav>'''    


#SQLALCHEMY initialization
#########################################################
engine = create_engine('sqlite:///main.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Login manager init
#########################################################
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class Users(flask_login.UserMixin):
	def __init__(self, U):
		self.id = U.username
		self.username = U.username
		self.password = U.password
		self.name = U.name
		self.email = U.email
		self.gender = U.gender
		self.birth_date = U.birth_date
		self.phone_number = U.phone_number
		self.address = U.address
		self.photodir = U.photodir
		self.verified = 0

#Upload setting initialization
#########################################################
UPLOAD_FOLDER = './static/img/photo_bucket'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Users class to handle login and session
#########################################################
@login_manager.user_loader
def user_loader(username):
	username = username
	U = session.query(User).filter_by(username=username).first()
	return U


#Route and implementation

#mainpage
#########################################################
@app.route('/', methods = ['GET','POST'])
def mainpage():
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	return render_template('main.html',logged_in=log_in,not_logged_in=not_log_in,nav=nav.format('','','',''))


#login page
#########################################################
@app.route('/login', methods=['GET','POST'])
def login():
	err = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		U = user_loader(username)
		if(U):
			if(U.verify_password(password)):
				user = Users(U)
				flask_login.login_user(user)
				return(redirect(url_for('mainpage')))
			else:
				err='<p style="color:red">wrong username/password</p>'
				return render_template('login.html',err_msg=err)
		else:
			err='<p style="color:red">wrong username/password</p>'
			return render_template('login.html',err_msg=err)
	else:
		return render_template('login.html',err_msg=err)

#logout page
#########################################################
@app.route('/logout', methods=['GET'])
def logout():
	flask_login.logout_user()
	return(redirect(url_for('mainpage')))

#about page
#########################################################
@app.route('/about', methods = ['GET','POST'])
def about():
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	return render_template('about.html',logged_in=log_in,not_logged_in=not_log_in, nav=nav.format('active','','',''))


#sign up page
#########################################################
@app.route('/sign_up', methods = ['GET','POST'])
def daftar():
	if request.method == 'POST':
		nama = request.form['nama']
		gender = request.form['gender']
		lahir = request.form['lahir']
		address = request.form['address']
		phone = request.form['phone']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		photo = request.files['photo']
		photoname = secure_filename(photo.filename)
		if(not allowed_file(photoname)):
			return ('photo type is not allowed')
		photodir =  os.path.join(app.config['UPLOAD_FOLDER'], photoname)
		i = 1
		while(session.query(ArticlePhoto).filter_by(dir=photodir).first() or session.query(ShopPhoto).filter_by(dir=photodir).first() or session.query(User).filter_by(photodir=photodir).first()):
			photoname = str(i) + photoname
			photodir =  os.path.join(app.config['UPLOAD_FOLDER'], photoname)
		new_user = User(username,password,nama,email,gender,lahir,phone,address,photodir)
		session.add(new_user)
		try:
			session.commit()
		except Exception as E:
			return 'Username has already taken'

		photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photoname))
		return('sign up success')
	else:
		if(flask_login.current_user.is_authenticated):
			return redirect(url_for('profile'))
		else:
			return render_template('sign_up.html')


#seller sign up
#########################################################
@app.route('/be_a_seller', methods = ['GET','POST'])
def daftar_seller():
	if request.method == 'POST':
		nama = request.form['nama']
		gender = request.form['gender']
		lahir = request.form['lahir']
		address = request.form['address']
		phone = request.form['phone']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		photo = request.files['photo']
		category = request.form['category']
		company = request.form['company']
		photoname = secure_filename(photo.filename)
		if(not allowed_file(photoname)):
			return ('photo type is not allowed')
		photodir =  os.path.join(app.config['UPLOAD_FOLDER'], photoname)
		while(session.query(ArticlePhoto).filter_by(dir=photodir).first() or session.query(ShopPhoto).filter_by(dir=photodir).first() or session.query(User).filter_by(photodir=photodir).first()):
			photoname = str(1) + photoname
			photodir =  os.path.join(app.config['UPLOAD_FOLDER'], photoname)
		new_user = User(username,password,nama,email,gender,lahir,phone,address,photodir)
		new_shop = Shop(name=company,user=username)
		new_shoptag = ShopTag(name=company, tag=category)
		new_shopphoto = ShopPhoto(shopname=company,dir=photodir)
		session.add(new_user)
		session.add(new_shop)
		session.add(new_shoptag)
		session.add(new_shopphoto)
		session.commit()
		photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photoname))
		return(redirect(url_for('login')))
	else:
		return render_template('be_a_seller.html')


#profile
#########################################################
@app.route('/profile', methods=['GET'])
def profile():
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	shops = session.query(Shop,Article,ArticlePhoto,ShopTag).join(Article).join(ArticlePhoto).join(ShopTag).all()
	shop = ''
	if(shops):
		curr_shop = shops[0][1].title
		shop = [shops[0]]
		i = 1
		for comp in shops:
			if(curr_shop == comp[1].title):
				pass
			else:
				curr_shop = comp[1].title
				shop.append([comp[0],comp[1],comp[2],comp[3]])
			i += 1
	return render_template('shoplisted_profile.html',company="Explore",shops=shop,nav=nav.format('','','active',''),logged_in=log_in,not_logged_in=not_log_in,category=category)


#category
#########################################################
@app.route('/category', methods=['GET'])
def category():
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	return render_template('category.html',logged_in=log_in,not_logged_in=not_log_in, nav=nav.format('','','active',''))

@app.route('/category/<category>', methods=['GET'])
def shoplist(category):
	shopname = session.query(Shop,ShopTag,ShopPhoto).join(ShopTag).filter_by(tag=category).join(ShopPhoto).all()
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	return render_template('shoplist_template.html', category=category, shops = shopname,logged_in=log_in,not_logged_in=not_log_in, nav=nav.format('','','active',''))

@app.route('/category/<category>/<shopss>', methods=['GET'])
def showshop(category, shopss):
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	shops = session.query(Shop,Article,ArticlePhoto).filter_by(name=shopss).join(Article).join(ArticlePhoto).all()
	shop = ''
	if(shops):
		curr_shop = shops[0][1].title
		shop = [shops[0]]
		i = 1
		for comp in shops:
			if(curr_shop == comp[1].title):
				pass
			else:
				curr_shop = comp[1].title
				shop.append([comp[0],comp[1],comp[2]])
			i += 1
	return render_template('shoplisted.html',company=shops,shops=shop,nav=nav.format('','','active',''),logged_in=log_in,not_logged_in=not_log_in,category=category)

@app.route('/category/<category>/<shopss>/<item>', methods=['GET'])
def showitem(category,shopss,item):
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	item = session.query(Article,ArticlePhoto).filter_by(title=item).join(ArticlePhoto).all()
	photos = ''
	i = 0
	for it in item:
		if i != 0:
			photos += ','
		else:
			i = 1
		photos += str('[\"'+url_for('static',filename=it[1].dir[9:])+'\"]')
	return render_template('item.html',photos=photos,content=item[0][0].content,title=item[0][0].title,nav=nav,logged_in=log_in,not_logged_in=not_log_in)

#Shop Item Function
#########################################################
@app.route('/shop',methods=['GET'])
@flask_login.login_required
def shop():
	log_in = ''
	not_log_in = ''
	if(flask_login.current_user.is_authenticated):
		log_in = ''
		not_log_in = 'none'
	else:
		log_in = 'none'
		not_log_in = ''
	shops = session.query(User,Shop,Article,ArticlePhoto).filter_by(username=flask_login.current_user.username).join(Shop).join(Article).join(ArticlePhoto).all()
	company = session.query(User,Shop).filter_by(username=flask_login.current_user.username).join(Shop).all()
	shop = ''
	if(shops):
		curr_shop = shops[0][2].title
		shop = [shops[0]]
		i = 1
		for comp in shops:
			if(curr_shop == comp[2].title):
				pass
			else:
				curr_shop = comp[2].title
				shop.append([comp[0],comp[1],comp[2],comp[3]])
			i += 1
	return render_template('shoplist.html',company=company,shops=shop,nav=nav.format('','','active',''),logged_in=log_in,not_logged_in=not_log_in)

@app.route('/shop/add',methods=['GET','POST'])
@flask_login.login_required
def add_shop():
	if flask_login.current_user.is_authenticated:
		if request.method == 'POST':
			title = request.form['name']
			description = request.form['description']
			photos = request.files.getlist('photo')
			shop = session.query(Shop).filter_by(user=flask_login.current_user.username).first().name
			new_article = Article(title=title,content=description,date_created=datetime.datetime.now().strftime("%Y-%m-%d"),shop=shop)
			session.add(new_article)
			for photo in photos:
				photoname = secure_filename(photo.filename)
				if(not allowed_file(photoname)):
					return ('photo type is not allowed')
				photodir =  os.path.join(app.config['UPLOAD_FOLDER'], photoname)
				i = 1
				while(session.query(ArticlePhoto).filter_by(dir=photodir).first() or session.query(ShopPhoto).filter_by(dir=photodir).first() or session.query(User).filter_by(photodir=photodir).first()):
					photoname = str(i) + photoname
					photodir =  os.path.join(app.config['UPLOAD_FOLDER'], photoname)	
				new_photo = ArticlePhoto(dir=photodir,articlename=title)
				session.add(new_photo)
				photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photoname))
			session.commit()
			return(redirect(url_for('shop')))
		else:
			return render_template('addshop.html')

@app.route('/shop/delete/<title>', methods=['GET','POST'])
@flask_login.login_required
def del_shop(title):
	if flask_login.current_user.is_authenticated:
		if request.method == 'POST':
			article = session.query(Article,ArticlePhoto).filter_by(title=title).join(ArticlePhoto).all()
			for photo in article:
				os.remove(photo[1].dir)
				session.delete(photo[0])
				session.delete(photo[1])
			session.commit()
			return redirect(url_for('shop'))
		else:
			return render_template('delshop.html',title=title)	

@app.route('/shop/edit/<title>', methods=['GET','POST'])
@flask_login.login_required
def edit_shop(title):
	if flask_login.current_user.is_authenticated:
		if request.method == 'POST':
			content = request.form['description']
			item = session.query(Article).filter_by(title=title).first()
			item.content = content
			session.commit()
			return(redirect(url_for('shop')))
		else:
			item = session.query(Article).filter_by(title=title).first()
			description = item.content
			return render_template('editshop.html',title=title,description=description)

#main
#########################################################
app.secret_key = str(os.urandom(10))
app.debug = False
login_manager.init_app(app)
app.run(host ='0.0.0.0', port=80)
