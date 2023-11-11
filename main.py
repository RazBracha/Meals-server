from flask import Flask
from flask_restful import Api
from resources import Key, Name, meal_name, meal_id, dishes, meals, changes
from flask_pymongo import PyMongo

app = Flask(__name__)  # initialize Flask
api = Api(app)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mealsDB'
mongo = PyMongo(app)

if 'db' in mongo.__dict__:
    print(f"Connected to MongoDB database: {mongo.db}")
else:
    print("Failed to connect to MongoDB database.")

api.add_resource(changes, '/meals/<int:meal_id>')
api.add_resource(meal_name, '/meals/<string:m_name>')
api.add_resource(meal_id, '/meals/<int:id>')
api.add_resource(meals, '/meals')
api.add_resource(dishes, '/dishes')
api.add_resource(Key, '/dishes/<int:key>')
api.add_resource(Name, '/dishes/<string:key_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)