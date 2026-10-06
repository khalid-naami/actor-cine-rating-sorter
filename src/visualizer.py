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
    if "title" not in df.columns:
        df["title"] = df.get("episode_title", "Unknown")
    else:
        df["title"] = df["title"].fillna(df.get("episode_title", "Unknown"))

    if "year" not in df.columns:
        df["year"] = df.get("start_year", 2000)
    else:
        df["year"] = df["year"].fillna(df.get("start_year", 2000))

    if "director" not in df.columns:
        df["director"] = df.get("studio", "Various")
    else:
        df["director"] = df["director"].fillna(df.get("studio", "Various"))

    if "rotten_tomatoes_pct" not in df.columns:
        df["rotten_tomatoes_pct"] = (df.get("imdb_rating", 8.0) * 10).clip(upper=100)
    else:
        df["rotten_tomatoes_pct"] = df["rotten_tomatoes_pct"].fillna((df.get("imdb_rating", 8.0) * 10).clip(upper=100))

    if "box_office_million" not in df.columns:
        df["box_office_million"] = 100.0
    else:
        df["box_office_million"] = df["box_office_million"].fillna(100.0)

    if "cinescore" not in df.columns:
        df["cinescore"] = (df.get("imdb_rating", 8.0) * 10).round(1)

    if "genres" in df.columns:
        df["genres_str"] = df["genres"].apply(lambda g: ", ".join(g) if isinstance(g, list) else str(g))
    else:
        df["genres_str"] = "General"

    fig = px.scatter(
        df,
        x="imdb_rating",
        y="rotten_tomatoes_pct",
        size="box_office_million",
        color="cinescore",
        hover_name="title",
        labels={
            "imdb_rating": "IMDb Rating (out of 10)",
            "rotten_tomatoes_pct": "Critics Index / Rotten Tomatoes (%)",
            "cinescore": "CineScore™ (0-100)",
            "box_office_million": "Scale Factor"
        },
        color_continuous_scale="Viridis",
        title="<b>Universal Rating Correlation: IMDb vs Critics Composite Index</b>"
    )

    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        xaxis=dict(gridcolor=CHART_THEME["grid_color"], range=[7.0, 10.0]),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"], range=[60, 105]),
        margin=dict(l=40, r=20, t=50, b=40),
        height=400
    )
    return fig

def create_cinescore_distribution_bar(movies: List[Dict[str, Any]], top_n: int = 10) -> go.Figure:
    """Creates a ranked bar chart of top media titles by CineScore."""
    if not movies:
        return go.Figure()

    df = pd.DataFrame(movies).head(top_n)
    if "cinescore" not in df.columns:
        return go.Figure()

    df = df.sort_values(by="cinescore", ascending=True)

    titles = []
    for _, row in df.iterrows():
        t = row.get("title") or row.get("episode_title") or "Unknown"
        y = row.get("year") or row.get("start_year") or ""
        y_str = f" ({y})" if y else ""
        titles.append(f"{t}{y_str}")

    fig = go.Figure(go.Bar(
        x=df["cinescore"],
        y=titles,
        orientation='h',
        marker=dict(
            color=df["cinescore"],
            colorscale="Plasma",
            line=dict(color="#0f172a", width=1)
        ),
        text=df["cinescore"].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "N/A"),
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="#ffffff", size=12, weight="bold")
    ))

    fig.update_layout(
        title=dict(text=f"<b>Top {top_n} Ranked Titles by CineScore™ Index</b>", font=dict(color="#f8fafc", size=16)),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        xaxis=dict(title="CineScore™ Composite Rating (0 - 100)", range=[50, 100], gridcolor=CHART_THEME["grid_color"]),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"]),
        margin=dict(l=180, r=20, t=50, b=40),
        height=380
    )
    return fig
