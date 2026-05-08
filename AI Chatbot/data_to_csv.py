import pandas
import glob
import hdf5_getters as g
from pathlib import Path
import csv 

base = Path(r'..\Riptide\millionsongsubset')
files = list(base.rglob("*.h5"))

print(files)

with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["title","artist_name","release","year","duration","tempo","time_signature","energy",
                        "danceability","key","loudness","mode","beats_start","end_of_fade_in","start_of_fade_out",
                        "bars_start","sections_start","segments_loudness_max","segments_loudness_max_time","segments_loudness_start",
                        "segments_pitches","segments_start","segments_timbre","artist_terms","similar_artists","location"])

    for f in files:
        print("next")
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
        beats_start = g.get_beats_start(h5)
        end_of_fade_in = g.get_end_of_fade_in(h5)
        start_of_fade_out = g.get_start_of_fade_out(h5)
        bars_start = g.get_bars_start(h5)
        sections_start = g.get_sections_start(h5)
        segments_loudness_max = g.get_segments_loudness_max(h5)
        segments_loudness_max = g.get_segments_loudness_max(h5)
        segments_loudness_max_time = g.get_segments_loudness_max_time(h5)
        segments_loudness_start = g.get_segments_loudness_start(h5)
        segments_pitches = g.get_segments_pitches(h5)
        segments_start = g.get_segments_start(h5)
        segments_timbre = g.get_segments_timbre(h5)
        artist_terms = g.get_artist_terms(h5)
        similar_artists = g.get_similar_artists(h5)
        location = g.get_artist_location(h5)
        print("loaded")
        writer.writerow([title.decode('UTF-8'), artist_name.decode('UTF-8'), release.decode('UTF-8'),year, duration, tempo, time_signature, energy, danceability, 
                        key, loudness, mode, beats_start, end_of_fade_in, start_of_fade_out, bars_start, sections_start, segments_loudness_max, segments_loudness_max,
                        segments_loudness_max_time, segments_loudness_start, segments_pitches, segments_start, segments_timbre, artist_terms,
                        similar_artists, location.decode('UTF-8')])
        print("wrote")
        h5.close()