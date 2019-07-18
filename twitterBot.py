import random, tweepy
import goodreads_scraper, hp_scraper1

# variables.

consumer_key = "sQvpjTbD1s1RPUzjXFrYKMsxt"
consumer_secret = "elimJPXjKylYtDy5ZacQK6CzhYrUPBzirPZq1G9Qum9Q2trA0R"
access_key = "1150862762425430018-lw2mQubqUhowICHsVWOKhwMppIoczx"
access_secret = "0JHF9aKWRpET5Dl0bvCLdGdEFhEo4cD9lYoJqBpc0oYeT"
fileName = "my_quotes.txt"
last_mention_file = "lastMention.txt"
mentions = []

#1151753922069114880            first mention ID

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

#
def getMentions(input_id) :
    print("... gathering mentions\n...\n...")
    mentions = twitter.mentions_timeline(input_id)
    print("... mentions gathered")
    if len(mentions) == 0 :
        print("... No new Mentions to gather since tweet ID :" + str(getLastMention(last_mention_file)))
    return mentions

def respondToMentions() :
    last_ment_id = getLastMention(last_mention_file)
    newMentions = getMentions(last_ment_id)
    for mention in reversed(newMentions) :
        last_ment_id = mention.id_str
        setLastMention(last_mention_file, last_ment_id)
        print(last_ment_id + "\t\t"+ mention.text)
        print('responded too')

# function that will take the size of the quotes text file. from given filename above
#   returns a random line of text from the file.
#   quotes in the file are seperated by line.
def getHPFileQuote() :
    #open file, get Number of lines, then get random line from the range.
    print_line = ''
    size = 1
    with open(fileName, "r", encoding = "utf-8") as f :
        #get line number of file, and then a random line number.
        lines = f.readlines()
        size = len(lines)
        rand_line_no = random.randint(0, size-1)
        print_line = lines[rand_line_no]
    return print_line

#call function to get the random quote.
# function will get a random quote from one of the two scrapers randomly.
# then it will post the quote to twitter.
def sendTweet() :
    #select method
    selection = random.randrange(1,3)
    try :
        if selection == 1 :
            # call function and tweet.
            #   function needs an input from the user regarding a quote topic/tag
            #   for testing its Harry Potter.
            randomGR_quote = goodreads_scraper.getRandomQuote("Harry Potter")
            twitter.update_status(randomGR_quote+"\n#QuickQuote#Bot")
            #print("Just posted a tweet, GR!")
            #print(randomGR_quote)
        else :
            randomHP_quote = hp_scraper1.getRandomQuote()
            twitter.update_status(randomHP_quote+"\n#QuickQuote#Bot")
            #print("Just posted a tweet! HP")
            #print(randomHP_quote)
    except tweepy.TweepError :
        sendTweet()


# send a tweet out!
#sendTweet()

respondToMentions()
