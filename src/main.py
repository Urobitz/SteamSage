from ML.model import model_interaction
from scrapers.main_scrapper import init
import pandas as pd

df_reviews = pd.read_csv("Output/games_reviews.csv")
df_games = pd.read_csv("Output/games_list.csv")

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Scan for new deals")
        print("2. Review game")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            confirm = input("Scanning for new games will take a while, are you sure? (y/n): ").strip().lower()
            if confirm == "y":
                print("Scanning...")
                init()
            else:
                print("Cancelled.")
        elif choice == "2":
            game_name = input("Enter the name of the game: ").strip()
            reviews = ", ".join(df_reviews[df_reviews['title'] == game_name]['Review Text'].dropna().astype(str))
            hours_played_series = (
            df_reviews[df_reviews['title'] == game_name]['Hours Played']
            .dropna()
            .astype(str)
            .str.replace(',', '', regex=False)
            .astype(float)
            )
            avg_hours = round(hours_played_series.mean(), 1)
            price = df_games[df_games['title'] == game_name]['price'].iloc[0]
            model_interaction(reviews, price, avg_hours) 
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

menu()
    