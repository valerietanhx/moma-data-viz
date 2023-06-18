import pandas as pd

artworks = pd.read_csv("Artworks.csv")
collabs = artworks[artworks["ConstituentID"].str.contains(", ", na=False)]
collab_nationalities = collabs["Nationality"].str.findall("\((.*?)\)").values.tolist()

# some are empty
# can just ignore those ba. as in. don't treat them as a collaborator
print(list(filter(lambda x: "" in x, collab_nationalities)))

# https://www.python-graph-gallery.com/chord-diagram/
# plotly only has chord diagram in v3 https://plotly.com/python/v3/filled-chord-diagram/
# can try this too https://github.com/shahinrostami/chord but not interactive i think
# or holoviews https://holoviews.org/reference/elements/bokeh/Chord.html

# is it possible to connect to oneself?
# seems possible based on the plotly tutorial

# tbh another potential graph, which  might look slightly cleaner, is heat map
# bc i'm thinking... a chord diagram isn't very insightful
# since both ends will be the same number
# maybe do both? can you toggle between both on streamlit?
