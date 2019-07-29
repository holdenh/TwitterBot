from bs4 import BeautifulSoup as Bsoup
from urllib.request import urlopen 
import random

#store the url of the page holding the quotes. 
        # 1st website https://www.teenvogue.com/gallery/best-harry-potter-quotes
        # 2nd website https://www.goodreads.com/quotes/tag

# function that srapes the given webpage for quotes.
        #returns a list.
def scrape_page() :
        
    page_URL = "https://www.teenvogue.com/gallery/best-harry-potter-quotes"

    #open connection and get content.
    #   scraper is not universal
    page_client = urlopen(page_URL)
    page_html = page_client.read()
    #close 
    page_client.close()
    #parse data to html
    soup = Bsoup(page_html, "html.parser")
    #access the data on the page.

    outer_container = soup.findAll("div", {"class":"gallery-slide-caption__dek"})
    quote_list = []

    #loop through all quote containers to get the actual quote.
    for container in outer_container :
        #inside first div the the text. Text needs to be formatted. 
        quote = (container.div.text)
        quote = quote.strip().replace("\n"," ")
        if len(quote) <= 264 :
            quote_list.append(quote)
    return quote_list

def getRandomQuote() :
    #scrape the page and get quotes first.
    quotes = scrape_page()
    # get rand index and return quote at the index.
    rand_index = random.randint(0, (len(quotes)-1))
    output_qoute = quotes[rand_index]
    
    return output_qoute