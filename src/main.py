"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    # Starter example profile — edit these values to try different users
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    print("User profile:")
    for key, value in user_prefs.items():
        print(f"  {key}: {value}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n--- Top Recommendations ---\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"#{rank}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"    Score: {score:.2f}  |  Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
