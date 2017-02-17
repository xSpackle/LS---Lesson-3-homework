from flask import Flask, render_template, request, jsonify
import sqlite3
app = Flask(__name__)


#connection=sqlite3.connect('database.db')
#print('Database opened successfully')

#connection.execute('CREATE TABLE IF NOT EXISTS posts(name TEXT, calories TEXT, cuisine TEXT, is_vegetarian TEXT, is_gluten_free TEXT)')
#print('Table created successfully')
#connection.close()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/addnew')
def enternew():
	return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
	connection=sqlite3.connect('database.db')
	cursor=connection.cursor()

	try:
		food_name = request.form['name']
		food_cuisine = request.form['cuisine']
		food_calories = request.form['calories']
		food_is_vegan = request.form['is_vegetarian']
		food_is_gluten_free = request.form['is_gluten_free']
		cursor.execute('INSERT INTO posts (name, cuisine, calories, is_vegetarian, is_gluten_free) VALUES(?,?,?,?,?)',(food_name,food_cuisine,food_calories,food_is_vegan,food_is_gluten_free))
		connection.commit()
		message = 'Record successfully added'
	except:
		connection.rollback()
		message = 'Something fukt up'
	finally:
		return render_template('result.html', message = message)
		connection.close()

#1

@app.route('/favorite', methods = ['GET'])
def favorite():
		connection=sqlite3.connect('database.db')
		cursor=connection.cursor()

		try:
			cursor.execute('SELECT * FROM posts WHERE name = "MmmYea"')
		except:
			result = ["Something got screwed up."]
		finally:
			result = cursor.fetchone()
			connection.close()

		return jsonify(result)

#2
@app.route('/search', methods = ['GET'])
def search():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	name = (request.args.get('name'),)
	try:
		cursor.execute('SELECT * FROM posts WHERE name = ?', name)
		result = jsonify(results=cursor.fetchall())
	except:
		result = "Database error"
	finally:
		connection.close()
		return result

#3
@app.route('/drop')
def drop():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()
	try:
		cursor.execute('DROP TABLE posts')
		result = 'Dropped'
	except:
		result = 'lol nah im here to stay'
	finally:
		connection.close()
		return result
app.run(debug = True)