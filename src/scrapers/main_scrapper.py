import pandas as pd
import csv
from playwright.sync_api import sync_playwright
from scrapers.search_scraper import get_games
from scrapers.review_scrapper import get_reviews

def init():
    #Synchronized processing
    with sync_playwright() as p:
        #Creating browser and page object
        browser = p.chromium.launch(headless=True, channel="msedge")
        page = browser.new_page()
        ## Open games list CSV file and initialize writer with column headers
        with open("Output/games_list.csv", "w", newline="", encoding="utf-8") as game_list_file:
            game_list_writer = csv.DictWriter(game_list_file, fieldnames=["title", "price", "link", "id", "review"])
            game_list_writer.writeheader()
            page.goto("https://store.steampowered.com/search?specials=1&category1=998&hidef2p=1&ndl=1")
            print("program starting...")
            prev_count = 0
            for i in range(20):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)
                try:
                    page.wait_for_function(
                        f"document.querySelectorAll('.responsive_search_name_combined').length > {prev_count}",
                        timeout=5000
                    )
                except Exception:
                    print("No more games loaded")
                    page.evaluate("window.scrollTo(0, 0)")
                prev_count = page.locator(".responsive_search_name_combined").count()
            print("games:", prev_count)
            games = get_games(page, game_list_writer)

        print("Getting Reviews")
        df_games = pd.read_csv("games_list.csv")

        with open("Output/games_reviews.csv", "w", newline="", encoding="utf-8") as game_reviews_file:
            review_file_writer = csv.DictWriter(game_reviews_file, fieldnames=["title", "game_ID", "Hours Played", "Steam Sentiment", "Review Text"])
            review_file_writer.writeheader()
            for index, row in df_games.iterrows():
                get_reviews(page, row["title"], row["id"], review_file_writer)