# Apify Actor: CineScore Multi-Platform Movie Rating Sorter & Top 100 Masterpieces 🎬🍿

A movie rating aggregator and custom ranking Actor inspired by [DidierRLopes/SortMoviesPerRating](https://github.com/DidierRLopes/SortMoviesPerRating). Features multi-platform rating telemetry (IMDb, Rotten Tomatoes, Metacritic, Letterboxd), a composite **CineScore (0-100)** algorithm, the **Top 100 All-Time Masterpieces** catalog, and a smart title list parser.

---

## 🌟 Key Features

1. **Multi-Source Critical Consensus**: Integrates ratings across all 4 major film authorities:
   - **IMDb** (0-10) with vote weight
   - **Rotten Tomatoes** (0-100% Tomatometer)
   - **Metacritic** (0-100 Metascore)
   - **Letterboxd** (0-5 cinephile community score)
2. **Proprietary CineScore Formula**:
   $$\text{CineScore} = (0.35 \times \text{IMDb} \times 10) + (0.25 \times \text{RT}) + (0.20 \times \text{Metacritic}) + (0.20 \times \text{Letterboxd} \times 20)$$
3. **Top 100 All-Time Masterpieces**: Built-in verified database spanning cinema history from classics (*The Godfather*, *Citizen Kane*, *12 Angry Men*) to modern icons (*Oppenheimer*, *Dune 2*, *Parasite*, *Spirited Away*).
4. **Custom List Title Parser**: Feed raw, unformatted, or numbered lists of movie titles (e.g. copied from blogs, letterboxd watchlists, or spreadsheets) to instantly look up ratings and sort them.
5. **Multi-Criteria Ranking**: Sort by CineScore, IMDb, Rotten Tomatoes, Metascore, Letterboxd, Release Year, Box Office Earnings, or Oscar Wins.

---

## 📥 Input Schema

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` | Select | `"Top 100 All-Time Masterpieces"` | Choose between exploring the Masterpieces catalog or parsing custom titles. |
| `rawMovieTitles` | Textarea | Sample titles | Pasted list of movies (used when mode is 'Parse Custom Movie List'). |
| `sortBy` | Select | `"CineScore (0-100)"` | Metric to sort by (`CineScore`, `IMDb`, `Rotten Tomatoes`, `Metacritic`, `Letterboxd`, `Release Year`, `Box Office`, `Oscar Wins`). |
| `ascending` | Boolean | `false` | True for lowest-to-highest, False for highest-to-lowest. |
| `genreFilter` | Select | `"All Genres"` | Filter by genre (Action, Sci-Fi, Drama, Crime, Animation, etc.). |
| `minImdb` | Number | `0.0` | Minimum IMDb score threshold. |
| `minYear` | Integer | `1950` | Minimum release year. |
| `maxYear` | Integer | `2026` | Maximum release year. |
| `searchQuery` | String | `""` | Search text matching title, director, or cast. |

---

## 📤 Output Dataset Format

```json
{
  "rank": 1,
  "title": "The Godfather",
  "year": 1972,
  "cinescore": 97.4,
  "imdb_rating": 9.2,
  "imdb_votes": "2,050,000+",
  "rotten_tomatoes_pct": 97,
  "metacritic_score": 100,
  "letterboxd_rating": 4.6,
  "director": "Francis Ford Coppola",
  "genres": ["Crime", "Drama"],
  "runtime_mins": 175,
  "box_office_million_usd": 250.3,
  "oscar_wins": 3,
  "streaming_platforms": ["Paramount+", "Amazon Prime"]
}
```

---

## 🚀 How to Run Locally

```bash
cd actor-cine-rating-sorter
pip install -r requirements.txt
python -m src.main
```
