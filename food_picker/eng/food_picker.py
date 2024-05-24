import json
import os
import random

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_config(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def filter_foods_by_ingredients(foods, selected_ingredients):
    filtered_foods = []
    for food in foods:
        if all(ingredient in food['ingredients'] for ingredient in selected_ingredients):
            filtered_foods.append(food)
    return filtered_foods

def add_food(config, food):
    config['foods'].append(food)

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Path to the config.json file
    config_path = os.path.join(script_dir, 'config.json')
    
    config = load_config(config_path)
    foods = config['foods']
    selected_foods = []

    last_choice = None

    while True:
        if last_choice is None:
            choice = input("Would you like to (1) get a random food, (2) filter by ingredients, or (3) add a food? Enter 1, 2, or 3: ")
        else:
            choice = last_choice

        if choice == '1':
            available_foods = [food for food in foods if food not in selected_foods]
            if not available_foods:
                print("No more foods available.")
                break
            selected_food = random.choice(available_foods)
            selected_foods.append(selected_food)
            print(f"Selected Food: {selected_food['name']}")
            print(f"Main Ingredients: {', '.join(selected_food['ingredients'])}")
            print(f"Description: {'; '.join(selected_food['description'])}")
            last_choice = '1'
        elif choice == '2':
            selected_ingredients = input("Enter ingredients to filter by (comma separated): ").split(',')
            selected_ingredients = [ingredient.strip().lower() for ingredient in selected_ingredients]
            
            available_foods = [food for food in foods if food not in selected_foods]
            filtered_foods = filter_foods_by_ingredients(available_foods, selected_ingredients)
            
            if not filtered_foods:
                print("No foods found with the selected ingredients.")
                last_choice = None
            else:
                selected_food = random.choice(filtered_foods)
                selected_foods.append(selected_food)
                print(f"Selected Food: {selected_food['name']}")
                print(f"Main Ingredients: {', '.join(selected_food['ingredients'])}")
                print(f"Description: {'; '.join(selected_food['description'])}")
                last_choice = '2'
        elif choice == '3':
            food_name = input("Enter the name of the food you want to add: ").strip()
            food_ingredients = input("Enter the ingredients of the food (comma-separated): ").strip().split(',')
            food_ingredients = [ingredient.strip().lower() for ingredient in food_ingredients]
            food_description = input("Enter the description of the food (steps separated by semicolons): ").strip().split(';')
            food_description = [step.strip() for step in food_description]
            new_food = {
                'name': food_name,
                'ingredients': food_ingredients,
                'description': food_description
            }
            add_food(config, new_food)
            save_config(config_path, config)
            print(f"Food '{food_name}' added successfully.")
            last_choice = '3'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            last_choice = None
        
        continue_search = input("Do you want to continue searching or adding? (yes/no): ").strip().lower()
        if continue_search != 'yes':
            break
        
        # Check if there are no more available foods
        if all(food in selected_foods for food in foods):
            print("No options left.")
            break

if __name__ == '__main__':
    main()
