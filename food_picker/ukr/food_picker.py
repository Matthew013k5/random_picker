import json
import os
import random

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def filter_foods_by_ingredients(foods, selected_ingredients):
    filtered_foods = []
    for food in foods:
        if all(ingredient in food['ingredients'] for ingredient in selected_ingredients):
            filtered_foods.append(food)
    return filtered_foods

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
            choice = input("Бажаєте (1) вибрати випадкову страву чи (2) відфільтрувати за інгредієнтами? Введіть 1 або 2: ")
        else:
            choice = last_choice

        if choice == '1':
            available_foods = [food for food in foods if food not in selected_foods]
            if not available_foods:
                print("Більше страв немає.")
            else:
                selected_food = random.choice(available_foods)
                selected_foods.append(selected_food)
                print(f"Обрана страва: {selected_food['name']}")
                print(f"Основні інгредієнти: {', '.join(selected_food['ingredients'])}")
            last_choice = '1'
        elif choice == '2':
            selected_ingredients = input("Введіть інгредієнти для фільтрації (через кому): ").split(',')
            selected_ingredients = [ingredient.strip().lower() for ingredient in selected_ingredients]
            
            available_foods = [food for food in foods if food not in selected_foods]
            filtered_foods = filter_foods_by_ingredients(available_foods, selected_ingredients)
            
            if not filtered_foods:
                print("Не знайдено страв з вибраними інгредієнтами.")
                last_choice = None
            else:
                selected_food = random.choice(filtered_foods)
                selected_foods.append(selected_food)
                print(f"Обрана страва: {selected_food['name']}")
                print(f"Основні інгредієнти: {', '.join(selected_food['ingredients'])}")
                last_choice = '2'
        else:
            print("Невірний вибір. Будь ласка, введіть 1 або 2.")
            last_choice = None
        
        continue_search = input("Бажаєте продовжити пошук? (так/ні): ").strip().lower()
        if continue_search != 'так':
            break

if __name__ == '__main__':
    main()
