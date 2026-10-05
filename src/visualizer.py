"""Interactive Cinema Visualizations & Rating Analytics with Plotly.

Generates rating correlation scatter plots, CineScore leaderboards,
and genre rating distributions.
"""

from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

CHART_THEME = {
    "paper_bgcolor": "rgba(15, 23, 42, 0.0)",
    "plot_bgcolor": "rgba(15, 23, 42, 0.0)",
    "font_color": "#e2e8f0",
    "grid_color": "rgba(148, 163, 184, 0.15)"
}

def create_ratings_scatter_plot(movies: List[Dict[str, Any]]) -> go.Figure:
    """Creates a scatter plot comparing IMDb Rating vs Rotten Tomatoes %."""
    if not movies:
        return go.Figure()

    df = pd.DataFrame(movies)
    df["genres_str"] = df["genres"].apply(lambda g: ", ".join(g) if isinstance(g, list) else str(g))

    fig = px.scatter(
        df,
        x="imdb_rating",
        y="rotten_tomatoes_pct",
        size="box_office_million",
        color="cinescore",
        hover_name="title",
        hover_data={"year": True, "director": True, "imdb_rating": True, "rotten_tomatoes_pct": True, "cinescore": True, "box_office_million": True},
        labels={
            "imdb_rating": "IMDb Rating (out of 10)",
            "rotten_tomatoes_pct": "Rotten Tomatoes Critics Score (%)",
            "cinescore": "CineScore™ (0-100)",
            "box_office_million": "Box Office ($M)"
        },
        color_continuous_scale="Viridis",
        title="<b>Rating Correlation: IMDb vs Rotten Tomatoes Critics Index</b>"
    )

    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        xaxis=dict(gridcolor=CHART_THEME["grid_color"], range=[7.0, 9.8]),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"], range=[60, 105]),
        margin=dict(l=40, r=20, t=50, b=40),
        height=400
    )
    return fig

def create_cinescore_distribution_bar(movies: List[Dict[str, Any]], top_n: int = 10) -> go.Figure:
    """Creates a ranked bar chart of top movies by CineScore."""
    if not movies:
        return go.Figure()

    df = pd.DataFrame(movies).head(top_n).sort_values(by="cinescore", ascending=True)

    fig = go.Figure(go.Bar(
        x=df["cinescore"],
        y=df["title"] + " (" + df["year"].astype(str) + ")",
        orientation='h',
        marker=dict(
            color=df["cinescore"],
            colorscale="Plasma",
            line=dict(color="#0f172a", width=1)
        ),
        text=df["cinescore"].apply(lambda x: f"{x:.1f}"),
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="#ffffff", size=12, weight="bold")
    ))

    fig.update_layout(
        title=dict(text=f"<b>Top {top_n} Ranked Films by CineScore™ Index</b>", font=dict(color="#f8fafc", size=16)),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        xaxis=dict(title="CineScore™ Composite Rating (0 - 100)", range=[50, 100], gridcolor=CHART_THEME["grid_color"]),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"]),
        margin=dict(l=180, r=20, t=50, b=40),
        height=380
    )
    return fig
