 
def get_games(page, file_writer): 
    #Get every single game to process individually
        print("Getting games....")
        game_elements = page.locator("a[data-ds-appid]")
        videogames = []
        for i in range(game_elements.count()):
            #individual game
            game = game_elements.nth(i)
            
            try:
                #locate title,price, and reviewss
                title = game.locator(".title").inner_text()
                price = game.locator(".discount_final_price").inner_text()
                link = game.get_attribute("href")
                appID = game.get_attribute("data-ds-appid")
                #review is splitted since in steam class is search_review_summary [positive,mixed, negative]
                review_class = game.locator(".search_review_summary").get_attribute("class")
                review = review_class.split(' ')[1] # type: ignore
            except:
                #If either is not found put default value
                title = game.locator(".title").inner_text()
                price = "0.00"
                review = "Unknown"
                continue
            file_writer.writerow({"title" : title, "price" : price, "link" : link, "id" : appID, "review": review})
