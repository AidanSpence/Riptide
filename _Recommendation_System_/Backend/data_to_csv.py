from pathlib import Path
import csv
import numpy as np
import hdf5_getters as g

# Configuration
BASE_DIR = Path(r"D:\Users\270385733\OneDrive - UP Education\Desktop\millionsongsubset")
FILES_POOL = list(BASE_DIR.rglob("*.h5"))


def make_csv(files: list[Path]):
    """Extracts song features from HDF5 files and exports them into a CSV file."""

    # Prevent numpy array conversions from injecting arbitrary newline characters
    np.set_printoptions(linewidth=np.inf)

    # Define features mapped explicitly to the output structure
    headers = [
        "title", "artist_name", "year", "duration", "tempo", 
        "time_signature", "key", "loudness", "mode", 
        "end_of_fade_in", "start_of_fade_out", "artist_terms"
    ]

    decode_bytes = lambda val: val.decode('UTF-8') if isinstance(val, bytes) else val

    with open("output.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for idx, file_path in enumerate(files, start=1):
            h5 = g.open_h5_file_read(file_path)

            try:
                # Extract string values
                title = decode_bytes(g.get_title(h5))
                artist_name = decode_bytes(g.get_artist_name(h5))
                artist_terms = g.get_artist_terms(h5).astype(str)

                writer.writerow([
                    title,
                    artist_name,
                    g.get_year(h5),
                    g.get_duration(h5),
                    g.get_tempo(h5),
                    g.get_time_signature(h5),
                    g.get_key(h5),
                    g.get_loudness(h5),
                    g.get_mode(h5),
                    g.get_end_of_fade_in(h5),
                    g.get_start_of_fade_out(h5),
                    artist_terms
                ])

            finally:
                h5.close()

            if idx % 500 == 0 or idx == len(files):
                print(f"{idx}/{len(files)} files done")

if __name__ == "__main__":
    make_csv(FILES_POOL)
    print("Saved output to 'output.csv'.")