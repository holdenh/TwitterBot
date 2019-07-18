from bs4 import BeautifulSoup as Bsoup
from urllib.request import urlopen 
import random


# function that scrapes the page and returns and list of quotes with person. 
def scrape_page(input_tag) :

    #store the url of the page holding the quotes. 
        # website https://www.goodreads.com/quotes/tag
    page_URL = "https://www.goodreads.com/quotes/tag/" + str(input_tag)

    #open connection and get content.
    page_client = urlopen(page_URL)
    page_html = page_client.read()
    #close 
    page_client.close()
    #parse data to html
    soup = Bsoup(page_html, "html.parser")
    #access the data on the page.

    outer_container = soup.findAll("div", {"class":"quoteDetails"})
    quote_list = []

    #loop through all quote containers to get the actual quote.
    for container in outer_container :
        #inside first div the the text. Text needs to be formatted. 
        quote = (container.div.text)
        quote = quote.split("//", maxsplit = 1)[0].strip().replace("\n"," ")
        if len(quote) <= 264 :
            quote_list.append(quote)
    return quote_list

#function that scrapes the page for quotes and returns a random quote.
    # arguements : input_tag - user must input a specific tag or topic for the quote.
def getRandomQuote(input_tag) :
    #scrape the page and get quotes first.
    quotes = scrape_page(input_tag)
    # get rand index and return quote at the index.
    rand_index = random.randint(0, (len(quotes)-1))
    output_quote = quotes[rand_index]
    
    return output_quote