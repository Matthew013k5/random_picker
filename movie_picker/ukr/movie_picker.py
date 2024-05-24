import json
import os
import random

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_config(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def delete_movie(config, movie_name):
    movies = config['movies']
    for movie in movies:
        if movie['name'] == movie_name:
            movies.remove(movie)
            return True
    return False

def add_movie(config, movie):
    config['movies'].append(movie)

def main():
    # Отримання каталогу поточного скрипта
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Шлях до файлу config.json
    config_path = os.path.join(script_dir, 'config.json')
    
    config = load_config(config_path)
    movies = config['movies']
    selected_movies = []

    last_choice = None

    while True:
        if last_choice is None:
            choice = input("Бажаєте (1) вибрати випадковий фільм, (2) відфільтрувати за жанром, (3) видалити фільм, чи (4) додати фільм? Введіть 1, 2, 3 або 4: ")
        else:
            choice = last_choice

        if choice == '1':
            available_movies = [movie for movie in movies if movie not in selected_movies]
            if not available_movies:
                print("Більше варіантів немає.")
                break
            selected_movie = random.choice(available_movies)
            selected_movies.append(selected_movie)
            print(f"Обраний фільм: {selected_movie['name']}")
            print(f"Опис: {selected_movie['description']}")
            last_choice = '1'
        elif choice == '2':
            genre = input("Введіть жанр для фільтрації: ").strip().capitalize()
            
            available_movies = [movie for movie in movies if movie not in selected_movies]
            filtered_movies = [movie for movie in available_movies if genre in movie['genres']]
            
            if not filtered_movies:
                print("Не знайдено фільмів з вибраним жанром.")
                last_choice = None
            else:
                selected_movie = random.choice(filtered_movies)
                selected_movies.append(selected_movie)
                print(f"Обраний фільм: {selected_movie['name']}")
                print(f"Опис: {selected_movie['description']}")
                last_choice = '2'
        elif choice == '3':
            movie_name = input("Введіть назву фільму, який ви хочете видалити: ").strip()
            if delete_movie(config, movie_name):
                save_config(config_path, config)
                print(f"Фільм '{movie_name}' успішно видалено.")
            else:
                print(f"Фільм '{movie_name}' не знайдено.")
            last_choice = '3'
        elif choice == '4':
            movie_name = input("Введіть назву фільму, який ви хочете додати: ").strip()
            movie_description = input("Введіть опис фільму: ").strip()
            movie_genres = input("Введіть жанри фільму (розділені комами): ").strip().split(',')
            movie_genres = [genre.strip().capitalize() for genre in movie_genres]
            new_movie = {
                'name': movie_name,
                'description': movie_description,
                'genres': movie_genres
            }
            add_movie(config, new_movie)
            save_config(config_path, config)
            print(f"Фільм '{movie_name}' успішно додано.")
            last_choice = '4'
        else:
            print("Невірний вибір. Будь ласка, введіть 1, 2, 3 або 4.")
            last_choice = None
        
        continue_search = input("Бажаєте продовжити? (так/ні): ").strip().lower()
        if continue_search != 'так':
            break

if __name__ == '__main__':
    main()
