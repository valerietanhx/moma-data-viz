import pandas as pd
import plotly.express as px

edges = pd.read_csv("collabs/CollabsGraphEdges.csv")

edges["pct"] = edges["value"].rank(method="max", pct=True, ascending=False)
freq = edges[["value", "pct"]].drop_duplicates().sort_values(by="value")
freq["pct"] = freq["pct"] * 100

freq = freq.rename(columns={"value": "Frequency", "pct": "Percentage"})

fig_cdf = px.area(
    freq,
    x="Frequency",
    y="Percentage",
    title="What is the percentage of collaborations that occur at least x times?<br>"
    + "<sup>A collaboration refers to a pair of two nations.</sup>",
    log_x=True,
    color_discrete_sequence=px.colors.sequential.Agsunset,
    hover_data={"Frequency": False, "Percentage": True},
)
fig_cdf.update_layout(
    xaxis_title="Frequency",
    yaxis_title="Percentage of all collaborations",
    xaxis=dict(
        tickvals=list(range(0, 11, 2))
        + list(range(0, 101, 20))
        + list(range(100, 650, 200)),
    ),
    hovermode="x",
)
