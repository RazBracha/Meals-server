# resources.py
from flask import make_response, jsonify, request
from flask_restful import Resource
from meal_and_dish import Dish, Meal

dish_instance = Dish()
meal_instance = Meal(dish_instance)

class Key(Resource):
    def get(self, key):
        dish = dish_instance.get_dish_by_key(key)
        if dish:
            return make_response(jsonify(dish), 200)
        else:
            return make_response(jsonify(-5), 404)

    def delete(self, key):
        result = dish_instance.delete_dish_by_key(key)
        if result != -5:
            return make_response(jsonify(key), 200)
        else:
            return make_response(jsonify(result), 404)

class Name(Resource):
    def get(self, key_name):
        dish = dish_instance.get_dish_by_name(key_name)
        if dish:
            return make_response(jsonify(dish), 200)
        else:
            return make_response(jsonify(-5), 404)

    def delete(self, key_name):
        result = dish_instance.delete_dish_by_name(key_name)
        if result != -5:
            return make_response(jsonify(key_name), 200)
        else:
            return make_response(jsonify(result), 404)

class meal_name(Resource):
    def get(self, m_name):
        meal = meal_instance.get_meal_by_name(m_name)
        if meal:
            return make_response(jsonify(meal), 200)
        else:
            return make_response(jsonify(-5), 404)

    def delete(self, m_name):
        result = meal_instance.delete_meal_by_name(m_name)
        if result != -5:
            return make_response(jsonify(m_name), 200)
        else:
            return make_response(jsonify(result), 404)

class meal_id(Resource):
    def get(self, id):
        meal = meal_instance.get_meal_by_id(id)
        if meal:
            return make_response(jsonify(meal), 200)
        else:
            return make_response(jsonify(-5), 404)

    def delete(self, id):
        result = meal_instance.delete_meal_by_id(id)
        if result != -5:
            return make_response(jsonify(id), 200)
        else:
            return make_response(jsonify(result), 404)

class dishes(Resource):
    def get(self):
        all_dishes = dish_instance.get_all_dishes()
        if all_dishes:
            return make_response(jsonify(all_dishes), 200)
        else:
            return make_response(jsonify(), 400)

    def delete(self):
        result = dish_instance.delete_all_dishes()
        return make_response(jsonify(result), 400)

    def post(self):
        dish_data = request.get_json()
        response = dish_instance.add_dish(dish_data)
        return make_response(jsonify(response), 201)

class meals(Resource):
    def get(self):
        all_meals = meal_instance.get_all_meals()
        if all_meals:
            return make_response(jsonify(all_meals), 200)
        else:
            return make_response(jsonify(), 400)

    def delete(self):
        result = meal_instance.delete_all_meals()
        return make_response(jsonify(result), 400)

    def post(self):
        meal_data = request.get_json()
        response = meal_instance.add_meal(meal_data)
        return make_response(jsonify(response), 201)

class changes(Resource):
    def put(self, meal_id):
        meal_data = request.get_json()
        response = meal_instance.update_meal(meal_id, meal_data)
        return make_response(jsonify(response), 200)
