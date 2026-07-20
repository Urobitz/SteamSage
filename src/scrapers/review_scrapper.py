import time

def get_reviews(page, title, game_id,file_writer):
    limit = 25
    reviews = []
    
    js_extract_text = """
    (element) => {
        const textContainer = element.querySelector('.apphub_CardTextContent');
        if (!textContainer) return element.innerText; // Respaldo si no encuentra la clase interna
        
        const nodes = Array.from(textContainer.childNodes);
        const lastTextNode = nodes.reverse().find(node => node.nodeType === 3);
        return lastTextNode ? lastTextNode.textContent.trim() : '';
    }
    """

    def get_all_reviews(review_blocks):
        while review_blocks.count() < limit:
            current_count = review_blocks.count()
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)

            try:
                # Espera hasta 3s a que aparezcan MÁS tarjetas que current_count
                page.wait_for_function(
                    f"document.querySelectorAll('.apphub_UserReviewCardContent').length > {current_count}",
                    timeout=3000
                )
            except Exception:
                # No llegó nada nuevo en 3s -> asumimos que ya no hay más reviews
                break

        return review_blocks.count()
    
    def get_review_text():
        review_content = review_blocks.nth(i)
        review_text = review_content.evaluate(js_extract_text)
        if(review_content.locator(".hours").count() > 0):
            hours = review_content.locator(".hours").inner_text().split(" ")[0]
        else:
             hours = None
        return review_text,hours

    twenty_five_years_ago = int(time.time() - (25 * 365 * 24 * 60 * 60))

    page.context.add_cookies([
        {
            "name": "wants_mature_content",
            "value": "1",
            "domain": "steamcommunity.com",
            "path": "/"
        },
        {
            "name": "birthtime",
            "value": str(twenty_five_years_ago),
            "domain": "steamcommunity.com",
            "path": "/"
        },
    ])
        
    review_blocks = page.locator(".apphub_UserReviewCardContent")

    #   GET POSITIVE REVIEWS ---
    page.goto(f"https://steamcommunity.com/app/{game_id}/positivereviews/?browsefilter=toprated", wait_until="domcontentloaded", timeout=30000)


    get_all_reviews(review_blocks)
    count = review_blocks.count()
    for i in range(min(count, limit)):
        review_text, hours = get_review_text()
        file_writer.writerow({"title": title, "game_ID" : game_id, "Hours Played" : hours, "Steam Sentiment" : "positive", "Review Text" : review_text})  


    # --- GET NEGATIVE REVIEWS ---
    page.goto(f"https://steamcommunity.com/app/{game_id}/negativereviews/?browsefilter=toprated", wait_until="domcontentloaded", timeout=30000)
    count = get_all_reviews(review_blocks)

    for i in range(min(count, limit)):
        review_text, hours = get_review_text()
        file_writer.writerow({"title": title, "game_ID" : game_id, "Hours Played" : hours, "Steam Sentiment" : "negative", "Review Text" : review_text})