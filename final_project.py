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
def showRestaurants():
	return "the landing page with all the restaurants"

@app.route('/restaurants/new')
def addRestaurant():
	return "Add a new restaurant"

@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return "Edit restaurant %s" % restaurant_id

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return "Delete restaurant"

@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	return "Restaurant menu"

@app.route('/restaurants/<int:restaurant_id>/menu/new')
def addMenuItem(restaurant_id):
	return "Add menu item"

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	return "Edit menu item"

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	return "Delete menu item"


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True # server will auto-reload
	app.run(host = '0.0.0.0', port = 5000) # makes server public (necessary for Vagrant) - tells webserver to listen on all IP addresses