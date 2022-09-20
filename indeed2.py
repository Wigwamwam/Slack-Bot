from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import random

import logging
import os
import re

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Joke Bot")
logger = logging.getLogger(__name__)

@app.message(re.compile("^quote$"))  # type: ignore
def show_random_joke(message, say):
    """Send a random pyjoke back"""
    channel_type = message["channel_type"]
    if channel_type != "im":
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    authors = []
    quotes = []

    def scrape_website(page_number):
        page_num = str(page_number)
        url = "https://www.goodreads.com/quotes/tag/inspirational?page="+page_num
        webpage = requests.get(url)

        soup = BeautifulSoup(webpage.text, "html.parser")

        quoteText = soup.find_all('div', attrs={'class': 'quoteText'})

        for i in quoteText:
            quote = i.text.strip().split('\n')[0]
            author = i.find('span', attrs={'class':'authorOrTitle'}).text.strip()
            quotes.append(quote)
            authors.append(author)

    n = 3
    for num in range(0,n):
        scrape_website(num)

    combined_list = []
    for i in range(len(quotes)):
        combined_list.append(quotes[i]+'-'+authors[i])

    quote = random.choice(combined_list)

    logger.info(f"Sent joke < {quote} > to user {user_id}")

    say(text=quote, channel=dm_channel)


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
