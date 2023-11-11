# meal_and_dish.py
import requests

class Dish:
    def __init__(self):
        self.dish_id = 0
        self.dish_collection = dict()

    def get_dish_by_key(self, key):
        return self.dish_collection.get(key)

    def delete_dish_by_key(self, key):
        if key in self.dish_collection:
            return self.dish_collection.pop(key)
        return -5

    def get_dish_by_name(self, name):
        for dish in self.dish_collection.values():
            if name == dish['name']:
                return dish
        return -5

    def delete_dish_by_name(self, name):
        for key, dish in self.dish_collection.items():
            if name == dish['name']:
                return self.dish_collection.pop(key)
        return -5

    def add_dish(self, dish_data):
        if 'name' not in dish_data or not dish_data['name']:
            return -1

        dish_name = dish_data['name']
        if any(dish_name == curr_dish['name'] for curr_dish in self.dish_collection.values()):
            return -2

        query = dish_name
        api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
        response = requests.get(api_url, headers={'X-Api-Key': '5Vocvb2jhJTzHS2WVPNUeg==na0EAyw5FC9Tc7Us'})

        if response.status_code == requests.codes.ok and response.json():
            info = response.json()
            total_calories = sum(float(dish_info['calories']) for dish_info in info)
            total_serving_size = sum(float(dish_info['serving_size_g']) for dish_info in info)
            total_sodium = sum(float(dish_info['sodium_mg']) for dish_info in info)
            total_sugar = sum(float(dish_info['sugar_g']) for dish_info in info)

            self.dish_id += 1
            self.dish_collection[self.dish_id] = {
                'name': dish_name,
                'ID': self.dish_id,
                'cal': total_calories,
                'size': total_serving_size,
                'sodium': total_sodium,
                'sugar': total_sugar
            }
            return self.dish_id

        elif response.status_code != requests.codes.ok:
            return -4
        else:
            return -3


class Meal:
    def __init__(self, dish_instance):
        self.meal_id = 0
        self.meal_collection = dict()
        self.dish_instance = dish_instance

    def delete_meal_by_id(self, meal_id):
        if meal_id in self.meal_collection:
            return self.meal_collection.pop(meal_id)
        return -5

    def get_meal_by_name(self, m_name):
        for meal in self.meal_collection.values():
            if m_name == meal['name']:
                return meal
        return -5

    def delete_meal_by_name(self, m_name):
        for key, meal in self.meal_collection.items():
            if m_name == meal['name']:
                return self.meal_collection.pop(key)
        return -5

    def add_meal(self, meal_data):
        if not all(key in meal_data for key in ['name', 'appetizer', 'main', 'dessert']):
            return -1

        if any(meal_data[key] == '' for key in ['name', 'appetizer', 'main', 'dessert']):
            return -1

        if any(meal_data[key] not in self.dish_instance.dish_collection for key in ['appetizer', 'main', 'dessert']):
            return -5

        self.meal_id += 1
        meal_appetizer_id = meal_data['appetizer']
        meal_main_id = meal_data['main']
        meal_dessert_id = meal_data['dessert']

        sum_calories = sum(self.dish_instance.dish_collection[dish_id]['cal'] for dish_id in
                           [meal_appetizer_id, meal_main_id, meal_dessert_id])
        sum_sodium = sum(self.dish_instance.dish_collection[dish_id]['sodium'] for dish_id in
                         [meal_appetizer_id, meal_main_id, meal_dessert_id])
        sum_sugar = sum(self.dish_instance.dish_collection[dish_id]['sugar'] for dish_id in
                        [meal_appetizer_id, meal_main_id, meal_dessert_id])

        self.meal_collection[self.meal_id] = {
            'name': meal_data['name'],
            'ID': self.meal_id,
            'appetizer': meal_appetizer_id,
            'main': meal_main_id,
            'dessert': meal_dessert_id,
            'cal': sum_calories,
            'sodium': sum_sodium,
            'sugar': sum_sugar
        }
        return self.meal_id

    def update_meal(self, meal_id, meal_data):
        if meal_id not in self.meal_collection:
            return -5

        need_update = False
        if self.meal_collection[meal_id]['name'] != meal_data['name']:
            self.meal_collection[meal_id]['name'] = meal_data['name']
            need_update = True

        for key in ['appetizer', 'main', 'dessert']:
            if meal_data[key] != self.meal_collection[meal_id][key]:
                need_update = True
                self.meal_collection[meal_id][key] = meal_data[key]

        if need_update:
            sum_calories = sum(self.dish_instance.dish_collection[dish_id]['cal'] for dish_id in
                               [self.meal_collection[meal_id]['appetizer'],
                                self.meal_collection[meal_id]['main'],
                                self.meal_collection[meal_id]['dessert']])
            sum_sodium = sum(self.dish_instance.dish_collection[dish_id]['sodium'] for dish_id in
                             [self.meal_collection[meal_id]['appetizer'],
                              self.meal_collection[meal_id]['main'],
                              self.meal_collection[meal_id]['dessert']])
            sum_sugar = sum(self.dish_instance.dish_collection[dish_id]['sugar'] for dish_id in
                            [self.meal_collection[meal_id]['appetizer'],
                             self.meal_collection[meal_id]['main'],
                             self.meal_collection[meal_id]['dessert']])
            self.meal_collection[meal_id]['cal'] = sum_calories
            self.meal_collection[meal_id]['sodium'] = sum_sodium
            self.meal_collection[meal_id]['sugar'] = sum_sugar

        return meal_id

    def get_all_meals(self):
        return list(self.meal_collection.values())