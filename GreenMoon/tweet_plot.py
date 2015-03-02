import sys
from bokeh.plotting import *
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from pymongo import Connection
import pandas as pd

mongo_connection = Connection()
tweet_db = mongo_connection.tweetDB
tweet_collections = tweet_db.tweetTextStats
all_tweet_batches = tweet_collections.find()
number_all_tweet_batches = all_tweet_batches.count()

# make a pandas dataframe called tweets
# tweets.columns = ['time', 'sentiment score', 'color']
# if pos counts / neg counts > 1, sentiment score = positive
# if pos counts / neg counts = 1, sentiment score = neutral
# if pos counts / neg counts > 1, sentiment score = negative
tweets = pd.DataFrame(data=None, index=range(number_all_tweet_batches), columns=['time', 'sentiment score', 'color'])

for tweet_batch_number in range(number_all_tweet_batches):
    tweet_batch = all_tweet_batches[tweet_batch_number]
    tweets.loc[tweet_batch_number, 'time'] = tweet_batch['timeStampDHM']
    # typo in tweetDB needs to be corrected: SetimentScores
    sentiment_score = tweet_batch['SetimentScores'].count('pos') / tweet_batch['SetimentScores'].count('neg')
    if sentiment_score > 1:
        tweets.loc[tweet_batch_number, 'sentiment score'] = 'pos'
        tweets.loc[tweet_batch_number, 'color'] = 'green'
    elif sentiment_score == 1:
        tweets.loc[tweet_batch_number, 'sentiment score'] = 'neu'
        tweets.loc[tweet_batch_number, 'color'] = 'yellow'
    else:
        tweets.loc[tweet_batch_number, 'sentiment score'] = 'neg'
        tweets.loc[tweet_batch_number, 'color'] = 'red'

print(tweets)


colormap = {'pos': 'green', 'neu': 'yellow', 'neg': 'red'}
tweets['color'] = tweets['sentiment score'].map(lambda x: colormap[x])

p = figure(title = "Sentiment change over time")
print(type(p))
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Sentiment Counts'

p.circle(tweets["time"], tweets["sentiment score"],
        color=tweets["color"], fill_alpha=0.2, size=10, )

show(p)

html = file_html(p, CDN, "my plot")

# orig_stdout = sys.stdout
# f = open('out.html', 'w')
# sys.stdout = f
# print(html)
# sys.stdout = orig_stdout
# f.close()

script, div = components(p, CDN)
print(script)
print(div)