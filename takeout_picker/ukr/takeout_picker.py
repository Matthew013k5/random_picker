import json
import os
import random

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    # Отримання каталогу поточного скрипта
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Шлях до файлу конфігурації (config.json)
    config_path = os.path.join(script_dir, 'config.json')
    
    config = load_config(config_path)
    foods = config['foods']
    selected_foods = []

    last_choice = None

    while True:
        if last_choice is None:
            choice = input("Бажаєте (1) вибрати випадковий вид їжі чи (2) відфільтрувати за видом їжі? Введіть 1 або 2: ")
        else:
            choice = last_choice

        if choice == '1':
            available_foods = [food for food in foods if food not in selected_foods]
            if not available_foods:
                print("Більше варіантів немає.")
                break
            selected_food = random.choice(available_foods)
            selected_foods.append(selected_food)
            print(f"Обрана їжа: {selected_food['name']}")
            last_choice = '1'
        elif choice == '2':
            food_type = input("Введіть тип їжі для фільтрації: ").strip().lower()
            
            available_foods = [food for food in foods if food not in selected_foods]
            filtered_foods = [food for food in available_foods if isinstance(food['type'], list) and food_type in food['type'] or food_type == food['type']]
            
            if not filtered_foods:
                print("Не знайдено їжі з вибраним типом.")
                last_choice = None
            else:
                selected_food = random.choice(filtered_foods)
                selected_foods.append(selected_food)
                print(f"Обрана їжа: {selected_food['name']}")
                last_choice = '2'
        else:
            print("Невірний вибір. Будь ласка, введіть 1 або 2.")
            last_choice = None
        
        continue_search = input("Бажаєте продовжити пошук? (так/ні): ").strip().lower()
        if continue_search != 'так':
            break

if __name__ == '__main__':
    main()
