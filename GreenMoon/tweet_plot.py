import sys
from bokeh.plotting import *
from bokeh.resources import CDN
from bokeh.embed import file_html, components

# make a pandas dataframe called tweets
# tweets.columns = ['time', 'sentiment score', 'color']
# if pos counts / neg counts > 1, sentiment score = positive
# if pos counts / neg counts = 1, sentiment score = neutral
# if pos counts / neg counts > 1, sentiment score = negative


colormap = {'pos': 'green', 'neu': 'yellow', 'neg': 'red'}
tweets['color'] = tweets['sentiment score'].map(lambda x: colormap[x])

p = figure(title = "Sentiment change over time")
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