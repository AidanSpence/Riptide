import hdf5_getters as g
from pathlib import Path
import csv 
import numpy as np

i = 0

base = Path(r'..\Riptide\millionsongsubset')
files = list(base.rglob("*.h5"))

with open("output.csv", "w", encoding="utf-8", newline="") as f:

    # To stop newline characters
    np.set_printoptions(linewidth=np.inf)


    writer = csv.writer(f)
    writer.writerow(["title","artist_name","release","year","duration","tempo","time_signature","energy",
                        "danceability","key","loudness","mode","end_of_fade_in","start_of_fade_out",
                        "artist_terms","similar_artists","location"])

    for f in files:
        i += 1
        h5 = g.open_h5_file_read(f)
        title = g.get_title(h5)
        artist_name = g.get_artist_name(h5)
        release = g.get_release(h5)
        year = g.get_year(h5)
        duration = g.get_duration(h5)
        tempo = g.get_tempo(h5)
        time_signature = g.get_time_signature(h5)
        energy = g.get_energy(h5)
        danceability = g.get_danceability(h5)
        key = g.get_key(h5)
        loudness = g.get_loudness(h5)
        mode = g.get_mode(h5)
        end_of_fade_in = g.get_end_of_fade_in(h5)
        start_of_fade_out = g.get_start_of_fade_out(h5)
        artist_terms = g.get_artist_terms(h5)
        similar_artists = g.get_similar_artists(h5)
        location = g.get_artist_location(h5)

        writer.writerow([title.decode('UTF-8'), artist_name.decode('UTF-8'), release.decode('UTF-8'),year, duration, tempo, time_signature, energy, danceability, 
                        key, loudness, mode, end_of_fade_in, start_of_fade_out, artist_terms, similar_artists, location.decode('UTF-8')])
        print(i)
        h5.close()