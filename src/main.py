"""Apify Actor Entrypoint: CineScore Movie Rating Sorter & Top 100 Masterpieces."""

import asyncio
import os
from apify import Actor
from src.movies_database import MASTER_MOVIES_DB
from src.rating_sorter_engine import RatingSorterEngine

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        mode = actor_input.get("mode", "Top 100 All-Time Masterpieces")
        raw_titles = actor_input.get("rawMovieTitles", "")
        sort_by = actor_input.get("sortBy", "CineScore (0-100)")
        ascending = bool(actor_input.get("ascending", False))
        genre_filter = actor_input.get("genreFilter", "All Genres")
        min_imdb = float(actor_input.get("minImdb", 0.0))
        min_year = int(actor_input.get("minYear", 1950))
        max_year = int(actor_input.get("maxYear", 2026))
        search_query = actor_input.get("searchQuery", "").strip()
        api_key = actor_input.get("apiKey") or os.getenv("APIFY_TOKEN") or os.getenv("API_KEY", "")

        Actor.log.info(f"Running CineScore Movie Sorter in mode: '{mode}' | Sort By: '{sort_by}' | Ascending: {ascending}")
        if api_key:
            Actor.log.info("API Key / Token authentication provided.")

        if mode == "Parse Custom Movie List" and raw_titles.strip():
            Actor.log.info("Parsing user-provided raw title list...")
            parsed_movies = RatingSorterEngine.parse_user_raw_list(raw_titles)
            results = RatingSorterEngine.filter_and_sort(
                movies=parsed_movies,
                sort_by=sort_by,
                ascending=ascending,
                selected_genre=genre_filter,
                selected_director="All Directors",
                selected_service="All Platforms",
                min_imdb=min_imdb,
                min_year=min_year,
                max_year=max_year,
                search_query=search_query
            )
        else:
            Actor.log.info(f"Filtering and ranking from Master Database ({len(MASTER_MOVIES_DB)} films)...")
            results = RatingSorterEngine.filter_and_sort(
                movies=MASTER_MOVIES_DB,
                sort_by=sort_by,
                ascending=ascending,
                selected_genre=genre_filter,
                selected_director="All Directors",
                selected_service="All Platforms",
                min_imdb=min_imdb,
                min_year=min_year,
                max_year=max_year,
                search_query=search_query
            )

        Actor.log.info(f"Sorting completed. Produced {len(results)} ranked movie entries.")

        dataset_records = []
        for rank, movie in enumerate(results, start=1):
            dataset_records.append({
                "rank": rank,
                "title": movie.get("title"),
                "year": movie.get("year"),
                "cinescore": movie.get("cinescore"),
                "imdb_rating": movie.get("imdb_rating"),
                "imdb_votes": movie.get("imdb_votes"),
                "rotten_tomatoes_pct": movie.get("rotten_tomatoes_pct"),
                "metacritic_score": movie.get("metacritic_score"),
                "letterboxd_rating": movie.get("letterboxd_rating"),
                "director": movie.get("director"),
                "genres": movie.get("genres"),
                "cast": movie.get("cast"),
                "runtime_mins": movie.get("runtime_mins"),
                "box_office_million_usd": movie.get("box_office_million"),
                "oscar_wins": movie.get("oscar_wins"),
                "streaming_platforms": movie.get("streaming_services"),
                "plot_synopsis": movie.get("plot")
            })

        if dataset_records:
            await Actor.push_data(dataset_records)
            Actor.log.info(f"Successfully pushed {len(dataset_records)} ranked movie records to Apify dataset.")

        # Save executive summary in Key-Value store for Apify MCP & instant API tools
        summary_payload = {
            "mode": mode,
            "sortBy": sort_by,
            "totalRankedMovies": len(dataset_records),
            "topMoviesLeaderboard": [
                {
                    "rank": r["rank"],
                    "title": r["title"],
                    "year": r["year"],
                    "cinescore": r["cinescore"],
                    "imdb": r["imdb_rating"],
                    "rt": f"{r['rotten_tomatoes_pct']}%",
                    "letterboxd": r["letterboxd_rating"],
                    "director": r["director"]
                }
                for r in dataset_records[:10]
            ]
        }
        await Actor.set_value("OUTPUT", summary_payload)
        Actor.log.info("Stored movie ranking summary OUTPUT in Key-Value store.")

if __name__ == "__main__":
    asyncio.run(main())
