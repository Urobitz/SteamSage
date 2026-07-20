# SteamSage

SteamSage is a prototype tool to compile information about the latest 
Steam game deals and analyze their reviews to determine whether the 
buy is worth it.

## Features
- Scrapes current Steam  game deals
- Organized csv output for further analysis  
- AI powered review analysis

## How it works
1. Crawls the steam deals page to get game name, price, and general sentiment
2. Opens each games and pulls an equal amount of reviews for positive and negative analysis
3. Feeds reviews to an AI model through an API
4. Outputs positive and negative traits of the game based on the reviews and gives a veredict.

## Installation
```bash
git clone https://github.com/tuusuario/steamsage.git
cd steamsage
pip install -r requirements.txt
```

## Usage
- Install requirements using ```pip install -r requirements.txt```
- Run ```playwright install``` in your console
- Run main.py in the src/ directory
- Choose an option in the menu, scanning for new games will override the pre-existing file I uploaded
- If you simply want to check if a game is worth it, use option 2 and insert the title of the game. The AI will respond.

## Requirements
- Python 3.x
- Groq free API key

## Configuration
Create a ```.env``` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Roadmap / Known limitations
The plan is to keep improving the tool as I learn new skills but some goals are:
- [ ] Improve scrapping speed
- [ ] Fix problems with steam games that have age verification
- [ ] Make a UI that shows the games like a library and allows for easier user interaction

## Disclaimer
This is a personal project used to learn python skills, html, and AI capabilities.

## License
MIT, GPL, etc.
