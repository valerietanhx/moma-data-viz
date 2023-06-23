import pandas as pd

artworks = pd.read_csv("Artworks.csv")
collabs = artworks[artworks["ConstituentID"].str.contains(", ", na=False)]

# cleaning that needs to be inserted here?
# don't consider it multiple collabs if it's the same work, just different parts.
# e.g. different paintings that together form one work.
# but the rest of the logic can be written first.

collab_nationalities = collabs["Nationality"].str.findall("\((.*?)\)").values.tolist()
collab_nationalities = list(  # removing empty strings / unknown nationalities
    map(
        lambda x: list(filter(lambda y: y != "" and y != "Nationality unknown", x)),
        collab_nationalities,
    )
)

unique_nationalities = sorted(
    {art_nat for group in collab_nationalities for art_nat in group}
)
num_unique_nationalities = len(unique_nationalities)

# adjacency matrix
row = [0] * num_unique_nationalities
adj_matrix = [row.copy() for _ in range(num_unique_nationalities)]

index_nationality = dict(enumerate(unique_nationalities))
nationality_index = {nat: idx for idx, nat in enumerate(unique_nationalities)}

# populate adjacency matrix
# NOTE: add logic for duplicate nationalities if necessary
# are we counting a collab as between people? or between nationalities?
# so e.g. we have A1, A2, B1, where A and B are countries
# are the collaborations A1-A2, A2-A1, A1-B1, A2-B1,
# or just A-B?
for group in collab_nationalities:
    for i in range(len(group) - 1):
        artist_1_index = nationality_index[group[i]]
        for j in range(i + 1, len(group)):
            artist_2_index = nationality_index[group[j]]
            adj_matrix[artist_1_index][artist_2_index] += 1
            adj_matrix[artist_2_index][artist_1_index] += 1

# get into source | dest | count format
edges = []
for i in range(num_unique_nationalities):
    for j in range(num_unique_nationalities):
        if adj_matrix[i][j] != 0:
            edge = [index_nationality[i], index_nationality[j], adj_matrix[i][j]]
            edges.append(edge)

collab_graph = pd.DataFrame(edges, columns=["source", "target", "value"])
collab_graph.to_csv("CollabsGraph.csv", index=False)

# https://holoviews.org/reference/elements/bokeh/Chord.html
# https://discuss.streamlit.io/t/plotting-holoviews-plot/215/10
