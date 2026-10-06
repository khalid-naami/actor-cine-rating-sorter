"""Apify Actor Entrypoint: CineScore Universe — Cinema, Series, Anime & Animation Intelligence."""

import asyncio
import os
from apify import Actor
from src.movies_database import MASTER_MOVIES_DB
from src.master_catalog import MasterCatalog
from src.rating_sorter_engine import RatingSorterEngine

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        mode = actor_input.get("mode", "Universe Catalog & Top Rankings")
        media_category = actor_input.get("mediaCategory", "All Media Universe")
        raw_titles = actor_input.get("rawMovieTitles", "")
        sort_by = actor_input.get("sortBy", "CineScore (0-100)")
        ascending = bool(actor_input.get("ascending", False))
        genre_filter = actor_input.get("genreFilter", "All Genres")
        min_imdb = float(actor_input.get("minImdb", 0.0))
        min_year = int(actor_input.get("minYear", 1930))
        max_year = int(actor_input.get("maxYear", 2026))
        search_query = actor_input.get("searchQuery", "").strip()
        api_key = actor_input.get("apiKey") or os.getenv("APIFY_TOKEN") or os.getenv("API_KEY", "")

        Actor.log.info(f"Running CineScore Universe in category: '{media_category}' | Mode: '{mode}' | Sort: '{sort_by}'")
        if api_key:
            Actor.log.info("API Key / Token authentication provided.")

        if mode == "Parse Custom Movie List" and raw_titles.strip():
            Actor.log.info("Parsing user-provided raw title list across Media Universe...")
            parsed_items = RatingSorterEngine.parse_user_raw_list(raw_titles)
            results = RatingSorterEngine.filter_and_sort(
                items=parsed_items,
                sort_by=sort_by,
                ascending=ascending,
                selected_genre=genre_filter,
                selected_director="All Directors / Creators",
                selected_service="All Platforms",
                min_imdb=min_imdb,
                min_year=min_year,
                max_year=max_year,
                search_query=search_query
            )
        else:
            catalog_items = MasterCatalog.get_items_by_category(media_category)
            Actor.log.info(f"Filtering and ranking from '{media_category}' ({len(catalog_items)} indexed titles)...")
            results = RatingSorterEngine.filter_and_sort(
                items=catalog_items,
                sort_by=sort_by,
                ascending=ascending,
                selected_genre=genre_filter,
                selected_director="All Directors / Creators",
                selected_service="All Platforms",
                min_imdb=min_imdb,
                min_year=min_year,
                max_year=max_year,
                search_query=search_query
            )

        Actor.log.info(f"Sorting completed. Produced {len(results)} ranked entries.")

        dataset_records = []
        for rank, item in enumerate(results, start=1):
            title = item.get("title") or item.get("episode_title") or "Unknown"
            year = item.get("year") or item.get("start_year")
            director = item.get("director") or item.get("studio") or ", ".join(item.get("creators", []))

            dataset_records.append({
                "rank": rank,
                "title": title,
                "media_type": item.get("media_type", "movie"),
                "year": year,
                "cinescore": item.get("cinescore"),
                "imdb_rating": item.get("imdb_rating"),
                "imdb_votes": item.get("imdb_votes"),
                "mal_score": item.get("mal_score"),
                "rotten_tomatoes_pct": item.get("rotten_tomatoes_pct"),
                "metacritic_score": item.get("metacritic_score"),
                "letterboxd_rating": item.get("letterboxd_rating"),
                "director_or_studio": director,
                "genres": item.get("genres", []),
                "seasons_count": item.get("seasons_count"),
                "episodes_count": item.get("episodes_count"),
                "series_title": item.get("series_title"),
                "episode_title": item.get("episode_title"),
                "top_episode": item.get("top_episode"),
                "streaming_platforms": item.get("streaming_services", []),
                "plot_synopsis": item.get("plot") or item.get("synopsis")
            })

        if dataset_records:
            try:
                await Actor.push_data(dataset_records)
            except Exception as push_err:
                Actor.log.warning(f"Push data validation warning: {push_err}. Retrying sanitized...")
                sanitized = [{k: v for k, v in r.items() if v is not None} for r in dataset_records]
                await Actor.push_data(sanitized)
            Actor.log.info(f"Successfully pushed {len(dataset_records)} ranked records to Apify dataset.")

        # Save executive summary in Key-Value store for Apify MCP & instant API tools
        summary_payload = {
            "mode": mode,
            "mediaCategory": media_category,
            "sortBy": sort_by,
            "totalRankedTitles": len(dataset_records),
            "topLeaderboard": [
                {
                    "rank": r["rank"],
                    "title": r["title"],
                    "media_type": r["media_type"],
                    "year": r["year"],
                    "cinescore": r["cinescore"],
                    "imdb": r["imdb_rating"],
                    "mal": r.get("mal_score"),
                    "director_or_studio": r["director_or_studio"]
                }
                for r in dataset_records[:10]
            ]
        }
        await Actor.set_value("OUTPUT", summary_payload)
        Actor.log.info("Executive summary report written to Key-Value Store key 'OUTPUT'.")

if __name__ == "__main__":
    asyncio.run(main())
