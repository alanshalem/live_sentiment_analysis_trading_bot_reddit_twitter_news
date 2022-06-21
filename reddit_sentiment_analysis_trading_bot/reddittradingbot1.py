import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *

client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)
info = client.get_account()
print(info)

reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="USERAGENT",
    username=config.REDDIT_USER,
)

# print(reddit)
# for comment in reddit.subreddit("redditdev").comments(limit=25):
#     print(comment.author)

sentimentList = []
neededSentiments = 300

def Average(lst):
    if len(lst) == 0:
        return len(lst)
    else:
        return sum(lst[-neededSentiments:])/neededSentiments
    
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('sending order')
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print('an exception has ocurred ' + e)
        return False
    return True


for comment in reddit.subreddit("bitcoinmarkets").stream.comments():
    print(comment.body)
    redditComment = comment.body
    blob = TextBlob(redditComment)
    sentiment = blob.sentiment
    print("********** Sentiment is: " + str(sentiment.polarity))
    
    if sentiment.polarity != 0.0:
        
        sentimentList.append(sentiment)
        print("********** TOTAL SENTIMENT OF LIST IS: **********" + str(round(Average(sentimentList), 4)))
        
        if len(sentimentList) > neededSentiments and round(Average(sentimentList)) > 0.5:
            print("********** BUY **********")
            if in_position:
                print("********** BUY ORDER **********")
            else:
                print("********** BUY ORDER **********")
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = True
        elif len(sentimentList) > neededSentiments  and round(Average(sentimentList)) < -0.5:
            # print("********** SELL **********")
            if in_position:
                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = False
                else:
                    print("********** SELL ORDER BUT WE DONT OWN **********")