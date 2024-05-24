import json
import os
import random

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_config(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def delete_food(config, food_name):
    foods = config['foods']
    for food in foods:
        if food['name'] == food_name:
            foods.remove(food)
            return True
    return False

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
            choice = input("Would you like to (1) pick a random type of food, (2) filter by type of food, (3) delete a food, or (4) add a food? Enter 1, 2, 3, or 4: ")
        else:
            choice = last_choice

        if choice == '1':
            available_foods = [food for food in foods if food not in selected_foods]
            if not available_foods:
                print("No more options available.")
                break
            selected_food = random.choice(available_foods)
            selected_foods.append(selected_food)
            print(f"Selected food: {selected_food['name']}")
            last_choice = '1'
        elif choice == '2':
            food_type = input("Enter the type of food to filter by: ").strip().lower()
            
            available_foods = [food for food in foods if food not in selected_foods]
            filtered_foods = [food for food in available_foods if isinstance(food['type'], list) and food_type in food['type'] or food_type == food['type']]
            
            if not filtered_foods:
                print("No food found with the selected type.")
                last_choice = None
            else:
                selected_food = random.choice(filtered_foods)
                selected_foods.append(selected_food)
                print(f"Selected food: {selected_food['name']}")
                last_choice = '2'
        elif choice == '3':
            food_name = input("Enter the name of the food you want to delete: ").strip()
            if delete_food(config, food_name):
                save_config(config_path, config)
                print(f"Food '{food_name}' deleted successfully.")
            else:
                print(f"Food '{food_name}' not found.")
            last_choice = '3'
        elif choice == '4':
            food_name = input("Enter the name of the food you want to add: ").strip()
            food_type = input("Enter the type of the food: ").strip().lower()
            new_food = {
                'name': food_name,
                'type': food_type
            }
            add_food(config, new_food)
            save_config(config_path, config)
            print(f"Food '{food_name}' added successfully.")
            last_choice = '4'
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            last_choice = None
        
        continue_search = input("Do you want to continue? (yes/no): ").strip().lower()
        if continue_search != 'yes':
            break

if __name__ == '__main__':
    main()
