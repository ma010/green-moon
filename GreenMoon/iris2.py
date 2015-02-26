import sys
from bokeh.sampledata.iris import flowers
from bokeh.plotting import *
from bokeh.resources import CDN
from bokeh.embed import file_html, components

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
flowers['color'] = flowers['species'].map(lambda x: colormap[x])

p = figure(title = "Iris Morphology")
p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Petal Width'

p.circle(flowers["petal_length"], flowers["petal_width"],
        color=flowers["color"], fill_alpha=0.2, size=10, )

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