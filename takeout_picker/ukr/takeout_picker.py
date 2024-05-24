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
            choice = input("Бажаєте (1) вибрати випадковий вид їжі, (2) відфільтрувати за видом їжі, (3) видалити їжу чи (4) додати їжу? Введіть 1, 2, 3 або 4: ")
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
        elif choice == '3':
            food_name = input("Введіть назву їжі, яку ви хочете видалити: ").strip()
            if delete_food(config, food_name):
                save_config(config_path, config)
                print(f"Їжу '{food_name}' успішно видалено.")
            else:
                print(f"Їжу '{food_name}' не знайдено.")
            last_choice = '3'
        elif choice == '4':
            food_name = input("Введіть назву їжі, яку ви хочете додати: ").strip()
            food_type = input("Введіть тип їжі: ").strip().lower()
            new_food = {
                'name': food_name,
                'type': food_type
            }
            add_food(config, new_food)
            save_config(config_path, config)
            print(f"Їжу '{food_name}' успішно додано.")
            last_choice = '4'
        else:
            print("Невірний вибір. Будь ласка, введіть 1, 2, 3 або 4.")
            last_choice = None
        
        continue_search = input("Бажаєте продовжити? (так/ні): ").strip().lower()
        if continue_search != 'так':
            break

if __name__ == '__main__':
    main()
