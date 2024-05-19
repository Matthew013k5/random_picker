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

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Path to the config.json file
    config_path = os.path.join(script_dir, 'config.json')
    
    config = load_config(config_path)
    movies = config['movies']
    selected_movies = []

    last_choice = None

    while True:
        if last_choice is None:
            choice = input("Would you like to (1) pick a random movie, (2) filter by genre, or (3) delete a movie? Enter 1, 2, or 3: ")
        else:
            choice = last_choice

        if choice == '1':
            available_movies = [movie for movie in movies if movie not in selected_movies]
            if not available_movies:
                print("No more options available.")
                break
            selected_movie = random.choice(available_movies)
            selected_movies.append(selected_movie)
            print(f"Selected movie: {selected_movie['name']}")
            print(f"Description: {selected_movie['description']}")
            last_choice = '1'
        elif choice == '2':
            genre = input("Enter the genre to filter by: ").strip().capitalize()
            
            available_movies = [movie for movie in movies if movie not in selected_movies]
            filtered_movies = [movie for movie in available_movies if genre in movie['genres']]
            
            if not filtered_movies:
                print("No movies found with the selected genre.")
                last_choice = None
            else:
                selected_movie = random.choice(filtered_movies)
                selected_movies.append(selected_movie)
                print(f"Selected movie: {selected_movie['name']}")
                print(f"Description: {selected_movie['description']}")
                last_choice = '2'
        elif choice == '3':
            movie_name = input("Enter the name of the movie you want to delete: ").strip()
            if delete_movie(config, movie_name):
                save_config(config_path, config)
                print(f"Movie '{movie_name}' deleted successfully.")
            else:
                print(f"Movie '{movie_name}' not found.")
            last_choice = '3'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            last_choice = None
        
        continue_search = input("Do you want to continue searching or deleting? (yes/no): ").strip().lower()
        if continue_search != 'yes':
            break

if __name__ == '__main__':
    main()
