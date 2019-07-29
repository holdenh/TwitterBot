import random, tweepy
import goodreads_scraper, hp_scraper1

# variables.

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
fileName = "my_quotes.txt"
last_mention_file = "lastMention.txt"
mentions = []

#1151753922069114880            first mention ID
#1152263154006712322            NEXT TEST ID
#-            next id     ~~~


# setup connection to twitter. 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
# create oject for twiiter.
twitter = tweepy.API(auth)

#function that opens a file containing the last mention id that was responded to.
# it will return this ID as an int.
def getLastMention(file_name) :
    f = open(file_name, 'r')
    last_mention_id = int(f.read())
    f.close()
    return last_mention_id

#funtion that will write that last seen mention id to the mentionID file.
# returns no value.
def setLastMention(file_name, last_mention_id) :
    f = open(file_name, 'w')
    f.write(last_mention_id)
    f.close()
    return

#function that will return a set of mentions from twtter.
# return a python like list.
def getMentions(input_id) :
    print("... gathering mentions\n...\n...")
    mentions = twitter.mentions_timeline(input_id)
    print("... mentions gathered")
    if len(mentions) == 0 :
        print("... No new Mentions to gather since tweet ID :" + str(getLastMention(last_mention_file)))
    return mentions

#function that will respond to the mentions since the last documented mentions.
# needs to access the lastMentions.txt file.
# returns to the calling funciton.
def respondToMentions() :
    #get the last mentions id from the file.
    last_ment_id = getLastMention(last_mention_file)
    newMentions = getMentions(last_ment_id)
    #loop most recent mentions from the twitter timeline.
    for mention in reversed(newMentions) :
        #store tweet ID.
        last_ment_id = mention.id_str
        setLastMention(last_mention_file, last_ment_id)
        #store tweet text.
        last_ment_text = mention.text
        print(last_ment_id + "\t\t"+ last_ment_text)
        #store tweet sender
        at_name = "@" + mention.user.screen_name
        if "#quote" in (last_ment_text).lower() :
            search_tag = ""
            split_list = last_ment_text.split(" ")
            for word in split_list :
                if "@" in word or word.lower() == "#quote" :
                    continue
                if "#" in word :
                    word = word.strip("#")
                search_tag = search_tag + word + "+"
            print('... responding')
            print(search_tag)
            quote = goodreads_scraper.getRandomQuote(str(search_tag))
            if quote == "NONE" :
                status = at_name + " No tweets found on goodreads.com//quotes with tag of : " + search_tag
                twitter.update_status(status, int(last_ment_id))
                print(status)
            else :
                quote = at_name +" "+ quote 
                twitter.update_status(quote, int(last_ment_id))
                #print(quote)
            #print(quote)
    print("\n... done")
    return

#call function to get the random quote.
# function will get a random quote from one of the two scrapers randomly.
# then it will post the quote to twitter.
# function will need an input from the user to search good reads for.
def sendQuote(input_tag) :
    # try except to catch any errors then retry to post. 
    try :
        # call function and tweet.
        #   function needs an input from the user regarding a quote topic/tag
        #   for testing its Harry Potter.
        randomGR_quote = goodreads_scraper.getRandomQuote(str(input_tag))
        twitter.update_status(randomGR_quote+"\n#QuickQuote#Bot")
        print("... Random Quote Sent.")
        #print("Just posted a tweet, GR!")
        #print(randomGR_quote)
    except tweepy.TweepError :
        sendQuote(input_tag)


#def sendHPQuote() :
    #randomHP_quote = hp_scraper1.getRandomQuote()
    #twitter.update_status(randomHP_quote+"\n#QuickQuote#Bot")
    #print("Just posted a tweet! HP")
    #print(randomHP_quote)

# send a HP quote tweet out!
sendQuote("Inspiration")

# gather most recent menions.
respondToMentions()
