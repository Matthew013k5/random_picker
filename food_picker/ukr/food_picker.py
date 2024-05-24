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
    # Отримання каталогу поточного скрипта
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Шлях до файлу config.json
    config_path = os.path.join(script_dir, 'config.json')
    
    config = load_config(config_path)
    foods = config['foods']
    selected_foods = []

    last_choice = None

    while True:
        if last_choice is None:
            choice = input("Бажаєте (1) вибрати випадкову страву, (2) відфільтрувати за інгредієнтами, чи (3) додати страву? Введіть 1, 2 або 3: ")
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
                print(f"Опис: {'; '.join(selected_food['description'])}")
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
                print(f"Опис: {'; '.join(selected_food['description'])}")
                last_choice = '2'
        elif choice == '3':
            food_name = input("Введіть назву страви, яку ви хочете додати: ").strip()
            food_ingredients = input("Введіть інгредієнти страви (через кому): ").strip().split(',')
            food_ingredients = [ingredient.strip().lower() for ingredient in food_ingredients]
            food_description = input("Введіть опис страви (кроки через крапку з комою): ").strip().split(';')
            food_description = [step.strip() for step in food_description]
            new_food = {
                'name': food_name,
                'ingredients': food_ingredients,
                'description': food_description
            }
            add_food(config, new_food)
            save_config(config_path, config)
            print(f"Страву '{food_name}' успішно додано.")
            last_choice = '3'
        else:
            print("Невірний вибір. Будь ласка, введіть 1, 2 або 3.")
            last_choice = None
        
        continue_search = input("Бажаєте продовжити пошук чи додавання? (так/ні): ").strip().lower()
        if continue_search != 'так':
            break

if __name__ == '__main__':
    main()
