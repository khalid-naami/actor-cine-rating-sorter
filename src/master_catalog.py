"""Unified Master Catalog for CineScore Platform.

Aggregates Movies, TV Series, Anime Series, Anime Movies, Cartoons,
Animated Feature Films, and Top Rated Legendary Episodes.
"""

from typing import Dict, List, Any, Optional
from src.movies_database import MASTER_MOVIES_DB
from src.series_database import MASTER_SERIES_DB, TOP_SERIES_EPISODES
from src.anime_database import MASTER_ANIME_DB, RAW_TOP_ANIME_MOVIES, TOP_ANIME_EPISODES
from src.cartoons_database import MASTER_CARTOONS_DB, RAW_TOP_ANIMATED_MOVIES, TOP_CARTOON_EPISODES

# Format Anime Movies for Master Catalog
FORMATTED_ANIME_MOVIES: List[Dict[str, Any]] = []
for idx, m in enumerate(RAW_TOP_ANIME_MOVIES, 1):
    m_copy = dict(m)
    m_copy["id"] = f"anime_movie_{idx:03d}"
    m_copy["media_type"] = "anime_movie"
    m_copy["genres"] = ["Animation", "Anime", "Fantasy", "Drama"]
    m_copy["cinescore"] = round(((m_copy.get("mal_score", 8.0) / 10.0) * 50) + ((m_copy.get("imdb_rating", 8.0) / 10.0) * 35) + ((m_copy.get("rotten_tomatoes_pct", 90)) * 0.15), 1)
    FORMATTED_ANIME_MOVIES.append(m_copy)

# Format Western Animated Feature Films for Master Catalog
FORMATTED_ANIMATED_MOVIES: List[Dict[str, Any]] = []
for idx, m in enumerate(RAW_TOP_ANIMATED_MOVIES, 1):
    m_copy = dict(m)
    m_copy["id"] = f"animated_movie_{idx:03d}"
    m_copy["media_type"] = "animated_movie"
    m_copy["genres"] = ["Animation", "Family", "Adventure", "Comedy"]
    m_copy["cinescore"] = round(((m_copy.get("imdb_rating", 8.0) / 10.0) * 45) + ((m_copy.get("rotten_tomatoes_pct", 90)) * 0.35) + 18.0, 1)
    FORMATTED_ANIMATED_MOVIES.append(m_copy)

# Unified Hall of Fame Episodes
HALL_OF_FAME_EPISODES: List[Dict[str, Any]] = []

for ep in TOP_SERIES_EPISODES:
    ep_item = dict(ep)
    ep_item["category"] = "Live-Action Series"
    ep_item["media_type"] = "legendary_episode"
    HALL_OF_FAME_EPISODES.append(ep_item)

for ep in TOP_ANIME_EPISODES:
    ep_item = dict(ep)
    ep_item["category"] = "Anime Series"
    ep_item["media_type"] = "legendary_episode"
    HALL_OF_FAME_EPISODES.append(ep_item)

for ep in TOP_CARTOON_EPISODES:
    ep_item = dict(ep)
    ep_item["category"] = "Cartoon / Animation"
    ep_item["media_type"] = "legendary_episode"
    HALL_OF_FAME_EPISODES.append(ep_item)

# Sort Hall of Fame Episodes by IMDb rating descending
HALL_OF_FAME_EPISODES.sort(key=lambda x: x.get("imdb_rating", 0.0), reverse=True)


class MasterCatalog:
    """Provides high-performance querying and filtering across the entire CineScore Universe."""

    CATEGORY_MAP = {
        "All Media Universe": None,
        "🎬 Top 100 Movies": "movie",
        "📺 Top 100 TV Series": "tv_series",
        "🎌 Top 100 Anime Series": "anime_series",
        "🎌 Top Anime Movies": "anime_movie",
        "🎨 Top 100 Cartoons": "cartoon_series",
        "🎨 Top 100 Animated Feature Films": "animated_movie",
        "🏆 Hall of Fame Legendary Episodes": "legendary_episode"
    }

    @classmethod
    def get_items_by_category(cls, category_name: str) -> List[Dict[str, Any]]:
        """Retrieves raw dataset matching the chosen category."""
        if category_name == "🎬 Top 100 Movies":
            return MASTER_MOVIES_DB
        elif category_name == "📺 Top 100 TV Series":
            return MASTER_SERIES_DB
        elif category_name == "🎌 Top 100 Anime Series":
            return MASTER_ANIME_DB
        elif category_name == "🎌 Top Anime Movies":
            return FORMATTED_ANIME_MOVIES
        elif category_name == "🎨 Top 100 Cartoons":
            return MASTER_CARTOONS_DB
        elif category_name == "🎨 Top 100 Animated Feature Films":
            return FORMATTED_ANIMATED_MOVIES
        elif category_name == "🏆 Hall of Fame Legendary Episodes":
            return HALL_OF_FAME_EPISODES
        else:
            # Combine all core media
            combined = []
            combined.extend(MASTER_MOVIES_DB)
            combined.extend(MASTER_SERIES_DB)
            combined.extend(MASTER_ANIME_DB)
            combined.extend(FORMATTED_ANIME_MOVIES)
            combined.extend(MASTER_CARTOONS_DB)
            combined.extend(FORMATTED_ANIMATED_MOVIES)
            return combined

    @classmethod
    def get_summary_stats(cls) -> Dict[str, Any]:
        """Returns grand statistics of the entire cinema & animation universe."""
        return {
            "total_movies": len(MASTER_MOVIES_DB),
            "total_series": len(MASTER_SERIES_DB),
            "total_anime_series": len(MASTER_ANIME_DB),
            "total_anime_movies": len(FORMATTED_ANIME_MOVIES),
            "total_cartoons": len(MASTER_CARTOONS_DB),
            "total_animated_movies": len(FORMATTED_ANIMATED_MOVIES),
            "total_legendary_episodes": len(HALL_OF_FAME_EPISODES),
            "grand_total": len(MASTER_MOVIES_DB) + len(MASTER_SERIES_DB) + len(MASTER_ANIME_DB) + len(FORMATTED_ANIME_MOVIES) + len(MASTER_CARTOONS_DB) + len(FORMATTED_ANIMATED_MOVIES) + len(HALL_OF_FAME_EPISODES)
        }
