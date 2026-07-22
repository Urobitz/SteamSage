from ML.model import model_interaction
from scrapers.main_scrapper import init
import pandas as pd
page_link = "https://store.steampowered.com/search?specials=1&category1=998&hidef2p=1&ndl=1"

games_output_file = "game_list_v2.csv"
review_output_file = "game_reviews_v2.csv"

def menu():
    global page_link
    while True:
        print("\n--- Menu ---")
        print("1. Scan games")
        print("2. Review game")
        print("3. Change scan link")
        print("4. Exit")

        choice = input("Choose an option: ").strip()
        #Either scan the deals page or the main steam shop page
        if choice == "1":
            print("\n--- Scan games ---")
            print("1. Scan game deals")
            print("2. Scan popular games")
            scan_choice = input("Choose an option: ").strip()
            #Link editor
            if scan_choice == "1":
                scan_link = "https://store.steampowered.com/search?specials=1&category1=998&hidef2p=1&ndl=1"
            elif scan_choice == "2":
                scan_link = "https://store.steampowered.com/search?term="
            else:
                print("Invalid option, returning to main menu.")
                continue
                #Confirmation because scanning will ovewrite the file and it takes a while
            confirm = input("Scanning for new games will take a while, are you sure? (y/n): ").strip().lower()
            if confirm == "y":
                print("Scanning...")
                init(scan_link,games_output_file,review_output_file)
            else:
                print("Cancelled.")
        #Review option to read from the scanned files
        elif choice == "2":
            try: 
                #Try to read the file and wry to it, if it fails, say the file doesnt exist
                df_games = pd.read_csv("Output/"+games_output_file)
                df_reviews = pd.read_csv("Output/"+review_output_file)

                game_name = input("Enter the name of the game: ").strip()
                if game_name in df_games["title"].values:
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
                    #Call the AI model to get a response based on the price, reviews and average hours
                    model_interaction(reviews, price, avg_hours)
                else:
                    print("Game not found")
            except:
                print("File does not exist")
        #Option made for future flexibility, this allows for others steam page link specifications
        elif choice == "3":
            new_link = input("Paste the new Steam search URL: ").strip()
            if new_link:
                page_link = new_link
                print("Link updated.")
            else:
                print("No link entered, keeping the previous one.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

menu()