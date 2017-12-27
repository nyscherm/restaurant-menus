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

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def addRestaurant():
	if request.method == 'POST':
		restaurants = session.query(Restaurant).all()
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New restaurant created")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('add-restaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			restaurant.name = request.form['name']
		session.add(restaurant)
		session.commit()
		restaurants = session.query(Restaurant).all()
		flash("Restaurant name updated")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('edit-restaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		flash("Restaurant deleted")
		return redirect(url_for('showRestaurants'))
	else:	
		return render_template('delete-restaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menu.html', restaurant = restaurant, menu = menu)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('new-menu-item.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name'] 
		if request.form['description']:
			item.description = request.form['description']
		if request.form['price']: 
			item.price = request.form['price']
		session.add(item)
		session.commit()
		flash("Menu item updated")
		return redirect(url_for('showMenu', restaurant_id = restaurant.id))
	else:
		return render_template('edit-menu.html', restaurant = restaurant, item = item)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash("Menu item deleted")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('delete-menu.html', restaurant = restaurant, item = item)

@app.route('/restaurants/JSON')
def restaurantJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurant=[r.serialize for r in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=[item.serialize])

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True # server will auto-reload
	app.run(host = '0.0.0.0', port = 5000) # makes server public (necessary for Vagrant) - tells webserver to listen on all IP addresses