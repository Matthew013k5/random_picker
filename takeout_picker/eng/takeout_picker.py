import json
import os
import random

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

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
            choice = input("Would you like to (1) pick a random type of food or (2) filter by type of food? Enter 1 or 2: ")
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
        else:
            print("Invalid choice. Please enter 1 or 2.")
            last_choice = None
        
        continue_search = input("Do you want to continue searching? (yes/no): ").strip().lower()
        if continue_search != 'yes':
            break

if __name__ == '__main__':
    main()
