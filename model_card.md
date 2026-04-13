# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is designed to suggest songs from a small catalog based on a user's stated genre preference, mood preference, target energy level, and whether they prefer acoustic-sounding music. It is built for classroom exploration — to demonstrate how a basic content-based recommendation system works — and is not intended for real-world deployment or production use.

**Who it is for:** Students and learners exploring how AI recommendation systems are built.

**What it assumes:** That the user can describe their taste with a single preferred genre, a single mood, and a rough energy target. It does not learn from listening history or adapt over time.

**What it is NOT for:** Replacing real music apps, making decisions for actual users, or being used outside an educational context.

---

## 3. How the Model Works

VibeFinder compares every song in the catalog against the user's stated preferences and gives each song a point score. Songs that match better get more points. The final ranked list puts the highest-scoring songs first.

Here is how points are awarded for each song:

- **Genre match** — If the song's genre matches what the user listed as their favorite, it earns 3 points. This is the most important factor.
- **Mood match** — If the song's mood matches the user's preferred mood, it earns 2 more points.
- **Energy closeness** — Songs earn up to 2 points based on how close their energy level is to what the user wants. A perfect match earns the full 2 points; a song that is completely opposite earns 0. Songs in between earn a proportional amount.
- **Acoustic bonus** — If the user prefers acoustic music and the song is mostly acoustic, it earns 1 extra point.

The maximum a song can score is 8 points. After all songs are scored, the list is sorted from highest to lowest and the top 5 are returned along with a plain-language explanation of each score.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`.

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, electronic, classical, r&b, country, metal, blues, folk

**Moods represented:** happy, chill, intense, relaxed, focused, moody, hype, euphoric, peaceful, smooth, nostalgic, melancholy, dreamy

**Numeric features per song:** energy (0–1), tempo in BPM, valence (emotional brightness, 0–1), danceability (0–1), acousticness (0–1)

**Changes from starter:** The original dataset had 10 songs. Eight songs were added to cover genres and moods that were missing, so the system could be tested with more diverse user profiles.

**Limitations of the data:**
- 18 songs is an extremely small catalog. Most real platforms have millions of tracks.
- Many genres have only one representative song, so a user who matches that genre will always get that one song as their top result.
- The data reflects a particular set of editorial choices — it does not represent all global music cultures or styles.
- There are no songs with lyrics data, no artist popularity scores, and no real user listening history.

---

## 5. Strengths

- **Transparent scoring** — Every recommendation comes with a plain-language explanation. Unlike black-box systems, you can see exactly why each song was ranked where it was.
- **Works well for common profiles** — For users with well-represented genres (pop, lofi, rock), the top results feel intuitive. A pop/happy user gets a pop/happy song first, every time.
- **No data required from other users** — The system only needs the current user's stated preferences. It does not depend on collecting behavior data from anyone else.
- **Handles acoustic preference explicitly** — The `likes_acoustic` flag makes acoustic preference a first-class signal rather than something buried in energy or tempo.

---

## 6. Limitations and Bias

**Genre lock-in (filter bubble):** Genre carries a 3-point weight — the highest of any factor. This means a song that perfectly matches a user's energy and mood but belongs to a different genre will almost always lose to any genre-match, even one with poor energy or the wrong mood. A user who lists `"pop"` will never discover jazz or folk through this system, even if those songs would genuinely resonate with them.

**Catalog imbalance:** Several genres — classical, metal, blues, r&b, hip-hop, electronic, folk, country — have only one song each. A user who matches any of these genres will always get that single song as their top result, with no meaningful variety. This is a representation problem: the system behaves as if those genres are unimportant because they are underrepresented in the data.

**The conflicting-preference edge case:** When a user has contradictory preferences (e.g., `genre=classical`, `mood=peaceful`, `energy=0.9`), the system still awards full genre and mood points to Morning Sonata — even though that song has energy 0.22, nowhere near the user's target of 0.9. The genre+mood dominance masks what is actually a poor energy match. In a real system this would likely disappoint the user.

**Binary matching for genre and mood:** Genre and mood are either a full match (earn full points) or a complete miss (earn nothing). There is no partial credit for related genres (e.g., "indie pop" is not recognized as close to "pop") or related moods (e.g., "relaxed" and "chill" are treated as totally different).

**Acoustic asymmetry:** Users who prefer acoustic music get a +1 bonus point. Users who prefer produced/electronic music receive no equivalent bonus. The system slightly favors acoustic-preferring users when scores are otherwise tied.

---

## 7. Evaluation

Six user profiles were tested, ranging from straightforward to deliberately contradictory:

| Profile | Top result | Felt accurate? |
|---|---|---|
| High-Energy Pop Fan (pop/happy/0.8) | Sunrise City — pop, happy, energy 0.82 | Yes — closest match on all dimensions |
| Chill Lofi Student (lofi/chill/0.38, acoustic) | Library Rain — lofi, chill, energy 0.35, acoustic 0.86 | Yes — near-perfect match |
| Intense Rock Fan (rock/intense/0.92) | Storm Runner — rock, intense, energy 0.91 | Yes — only rock song but it fits well |
| Smooth R&B Listener (r&b/smooth/0.55) | Slow Burn — r&b, smooth, energy 0.55 | Yes — perfect match, but #2–5 are generic energy-only matches |
| Acoustic Folk Dreamer (folk/dreamy/0.30, acoustic) | Wildflower Road — folk, dreamy, energy 0.30, acoustic 0.90 | Yes — maximum possible score (8.0) |
| Edge Case: Classical/Peaceful but energy 0.9 | Morning Sonata — classical, peaceful, energy 0.22 | No — genre+mood wins even with a 0.68 energy gap |

**Weight-shift experiment:** Genre weight was halved (3.0 → 1.5) and energy weight was doubled (2.0 → 4.0). Key findings:
- For the pop/happy user: Rooftop Lights (indie pop/happy, energy 0.76) jumped from #3 to #2, ahead of Gym Hero, because energy proximity and mood now outweigh genre-only matches.
- For the edge case: Morning Sonata's score dropped from 6.64 to 5.78. Storm Runner (rock/intense, energy 0.91) jumped to #2 with score 3.96, showing the system can detect better energy matches when genre isn't so dominant. However, Morning Sonata still wins overall because genre+mood+acoustic combined still outweigh pure energy proximity.
- **Conclusion:** The weight shift makes recommendations more energy-sensitive and genre-tolerant, which helps users who want a specific "feel" more than a specific genre. The original weights better suit users who strongly identify with one genre.

**Profile comparison notes:**
- The EDM/high-energy profile and the classical/peaceful edge case both get "genre-locked" results — the system picks whichever song matches the genre first, and everything else falls far behind. This shows that genre weight is the single biggest driver of the output.
- The lofi/acoustic and folk/acoustic profiles both benefit from the acoustic bonus, which helps surface acoustically similar songs even when genre doesn't match perfectly (e.g., ambient and blues appear in the lofi and folk results' lower ranks because they score acoustic bonus points).

---

## 8. Future Work

- **Add genre similarity weighting** — Instead of full match or no match, define genre groups (e.g., lofi and ambient are "chill/low-energy" genres; rock and metal are "high-intensity" genres) and award partial points for nearby genres. This would reduce filter-bubble behavior.
- **Expand the catalog significantly** — With only 18 songs, several genres have no variety. Adding 50–100 songs per genre would make the ranking more meaningful and prevent single-song monopolies for rare genres.
- **Add listening history** — Even a simple "songs the user has played before" list could be used to downweight already-heard songs and introduce variety into the recommendations.
- **Support multi-value preferences** — Allow users to list multiple favorite genres or moods instead of just one. Real listeners rarely fit into a single genre box.
- **Add a diversity rule** — Prevent the top 5 results from all being the same genre. Force at least one "discovery" slot for a song outside the user's stated genre.

---

## 9. Personal Reflection

The system behaved mostly as I expected which was itself a useful thing to notice. When you can see every weight and every calculation, the results stop feeling like "the algorithm decided" and start feeling like basic math you could do by hand. That transparency made it easier to understand why real platforms keep their recommendation logic hidden: once you know the rules, you can predict the output, and that takes away some of the "magic" that keeps users engaged.

The biggest thing I'd want to improve is the catalog size and variety. With only 18 songs, genres like classical or blues have just one track each, so the system doesn't really have a choice, it always recommends the same song for those profiles. A much bigger dataset would make the ranking actually meaningful. Beyond that, I'd want to build something closer to an AI DJ, a system that adapts based on what you've actually been listening to, not just what you said you like when you filled out a profile. That kind of dynamic, taste-learning recommender would be a lot more interesting to build and a lot more useful in practice.
