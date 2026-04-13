import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _compute_score(
    song_genre: str,
    song_mood: str,
    song_energy: float,
    song_acousticness: float,
    fav_genre: str,
    fav_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """Shared scoring logic used by both the OOP and functional interfaces.

    Returns a (score, reasons) tuple where reasons is a list of plain-language
    strings explaining each component that contributed to the score.
    """
    score = 0.0
    reasons = []

    if song_genre.lower() == fav_genre.lower():
        score += 3.0
        reasons.append("genre match (+3.0)")

    if song_mood.lower() == fav_mood.lower():
        score += 2.0
        reasons.append("mood match (+2.0)")

    energy_points = (1.0 - abs(target_energy - song_energy)) * 2.0
    score += energy_points
    reasons.append(f"energy proximity ({energy_points:.1f})")

    if likes_acoustic and song_acousticness > 0.5:
        score += 1.0
        reasons.append("acoustic match (+1.0)")

    return score, reasons


class Recommender:
    """OOP interface for scoring and ranking songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a single song against the given user profile."""
        return _compute_score(
            song.genre, song.mood, song.energy, song.acousticness,
            user.favorite_genre, user.favorite_mood,
            user.target_energy, user.likes_acoustic,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        _, reasons = self._score(user, song)
        return "; ".join(reasons) if reasons else "No strong match found."


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs against user_prefs, returning the top-k results.

    Each result is a (song_dict, score, explanation) tuple.
    """
    results = []
    for song in songs:
        score, reasons = _compute_score(
            song["genre"], song["mood"], song["energy"], song["acousticness"],
            user_prefs.get("genre", ""),
            user_prefs.get("mood", ""),
            float(user_prefs.get("energy", 0.5)),
            bool(user_prefs.get("likes_acoustic", False)),
        )
        explanation = "; ".join(reasons) if reasons else "No strong match."
        results.append((song, score, explanation))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]
