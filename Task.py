import requests
from bs4 import BeautifulSoup
import time

# Function to fetch a Twitter page's HTML content
def fetch_twitter_page(url):
    headers = {
        'User-Agent': 'Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error if the request failed
    return response.text

# Function to parse the HTML content and count mentions of the ticker
def parse_mentions(html, ticker):
    soup = BeautifulSoup(html, 'html.parser')
    tweets = soup.find_all('div', {'data-testid': 'tweetText'})
    mentions = sum(tweet.get_text().count(ticker) for tweet in tweets)
    return mentions

# Main scraping function that runs in a loop with a specified interval
def scrape_twitter_accounts(accounts, ticker, interval):
    while True:
        total_mentions = 0  # Initialize total mentions count
        for account in accounts:
            url = f'https://twitter.com/{account}'
            html = fetch_twitter_page(url)
            mentions = parse_mentions(html, ticker)
            total_mentions += mentions  # Accumulate mentions count
            print(f"Checked {account}: {mentions} mentions")
        print(f"'{ticker}' was mentioned '{total_mentions}' times in the last '{interval}' minutes.")
        time.sleep(interval * 60)  # Wait for the specified interval before running again

if __name__ == "__main__":
    accounts = [
        "Mr_Derivatives",
        "warrior_0719",
        "ChartingProdigy",
        "allstarcharts",
        "yuriymatso",
        "TriggerTrades",
        "AdamMancini4",
        "CordovaTrades",
        "Barchart",
        "RoyLMattox"
    ]
    
    ticker = input("Enter the stock ticker (e.g., $TSLA): ")
    interval = int(input("Enter the time interval in minutes for scraping: "))
    
    scrape_twitter_accounts(accounts, ticker, interval)
