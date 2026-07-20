import os 
from dotenv import load_dotenv
from groq import Groq

#function to interact with the model, and return the response
def model_interaction(reviews, game_price, avg_hours):
    load_dotenv()
    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Follow these steps: 1) List exactly 5 positive traits as '|1-2 word description|: %' (sum=100%)."
           "2) List exactly 5 negative traits same format (sum=100%). "
           "3) One line starting with 'Verdict:' saying if it's worth buying, based on price and the "
           "average hours reviewers played (this is how much reviewers played BEFORE reviewing, "
           "not a suggestion of how long the user must play)."
        },
        {
            "role": "user",
            "content": f"Reviews: {reviews}\nPrice: {game_price}\nAverage hours played by reviewers: {avg_hours}"
        }
    ],
    model="llama-3.1-8b-instant"
)

    print(chat_response.choices[0].message.content)

