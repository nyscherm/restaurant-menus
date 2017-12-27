from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new/')
def addRestaurant():
	return render_template('add-restaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	return render_template('edit-restaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	return render_template('delete-restaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = restaurant, menu = menu)

@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def addMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	return render_template('new-menu-item.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return render_template('edit-menu.html', restaurant = restaurant, item = item)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return render_template('delete-menu.html', restaurant = restaurant, item = item)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True # server will auto-reload
	app.run(host = '0.0.0.0', port = 5000) # makes server public (necessary for Vagrant) - tells webserver to listen on all IP addresses