import os

import pandas as pd

CURR_FILEPATH = os.path.dirname(__file__)

artworks_path = os.path.join(CURR_FILEPATH, "../Artworks.csv")
artworks = pd.read_csv(artworks_path)
collabs = artworks[artworks["ConstituentID"].str.contains(", ", na=False)]

collabs_path = os.path.join(CURR_FILEPATH, "Collabs.csv")
collabs.to_csv(collabs_path, index=False)

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

collab_nationalities = list(filter(lambda x: len(x) > 1, collab_nationalities))
collab_nationalities = list(filter(lambda x: len(set(x)) > 1, collab_nationalities))

unique_nationalities = sorted(
    {art_nat for group in collab_nationalities for art_nat in group}
)
num_unique_nationalities = len(unique_nationalities)

# adjacency matrix
row = [0] * num_unique_nationalities
adj_matrix_plotting = [row.copy() for _ in range(num_unique_nationalities)]
adj_matrix_selection = [row.copy() for _ in range(num_unique_nationalities)]

index_nationality = dict(enumerate(unique_nationalities))
nationality_index = {nat: idx for idx, nat in enumerate(unique_nationalities)}

# populate adjacency matrix
for group in collab_nationalities:
    group = sorted(list(set(group)))
    for i in range(len(group) - 1):
        artist_1_index = nationality_index[group[i]]
        for j in range(i + 1, len(group)):
            artist_2_index = nationality_index[group[j]]

            adj_matrix_plotting[artist_1_index][artist_2_index] += 1

            adj_matrix_selection[artist_1_index][artist_2_index] += 1
            adj_matrix_selection[artist_2_index][artist_1_index] += 1

# get into source | dest | count format
edges_plotting = []  # used to plot chord diagram
edges_selection = []  # used for selection of two nationalities. bidirectional
for i in range(num_unique_nationalities):
    for j in range(num_unique_nationalities):
        if adj_matrix_plotting[i][j] != 0:
            edge = [
                index_nationality[i],
                index_nationality[j],
                adj_matrix_plotting[i][j],
            ]
            edges_plotting.append(edge)
        if adj_matrix_selection[i][j] != 0:
            edge = [
                index_nationality[i],
                index_nationality[j],
                adj_matrix_selection[i][j],
            ]
            edges_selection.append(edge)

collabs_graph_edges = pd.DataFrame(
    edges_plotting, columns=["source", "target", "value"]
)
collabs_graph_edges_path = os.path.join(CURR_FILEPATH, "CollabsGraphEdges.csv")
collabs_graph_edges.to_csv(collabs_graph_edges_path, index=False)

collabs_selection_edges = pd.DataFrame(
    edges_selection, columns=["source", "target", "value"]
)
collabs_selection_edges_path = os.path.join(CURR_FILEPATH, "CollabsSelectionEdges.csv")
collabs_selection_edges.to_csv(collabs_selection_edges_path, index=False)
