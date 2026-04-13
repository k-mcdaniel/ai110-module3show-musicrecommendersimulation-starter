"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi Student": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Intense Rock Fan": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
    "Smooth R&B Listener": {
        "genre": "r&b",
        "mood": "smooth",
        "energy": 0.55,
        "likes_acoustic": False,
    },
    "Acoustic Folk Dreamer": {
        "genre": "folk",
        "mood": "dreamy",
        "energy": 0.30,
        "likes_acoustic": True,
    },
    "Edge Case — High Energy but Peaceful": {
        "genre": "classical",
        "mood": "peaceful",
        "energy": 0.9,
        "likes_acoustic": True,
    },
}


def print_recommendations(songs, user_prefs, label, k=5):
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{'=' * 55}")
    print(f"  Profile: {label}")
    print(f"  Prefs:   genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs['likes_acoustic']}")
    print(f"{'=' * 55}")

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f}  |  {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    for label, prefs in PROFILES.items():
        print_recommendations(songs, prefs, label)


if __name__ == "__main__":
    main()
