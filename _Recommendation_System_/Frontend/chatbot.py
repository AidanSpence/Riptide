import random
import re
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from _Recommendation_System_.Frontend.recommender import SongRecommender

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_PATH = PROJECT_ROOT / "models"


class Dialog_Manager:
    """
    Manages user dialogue inputs and converts detected mood, style,
    and genre information into a feature vector suitable for music
    recommendation or prediction models.
    """
    def __init__(self, style, mood, message, genre=None):
        self.style = style.group(0) if style else None
        self.mood = mood.group(0) if mood else None
        self.text = message

        # Load required files
        self.df = joblib.load(MODELS_PATH / "df.jb")
        self.std = joblib.load(MODELS_PATH / "svd.jb")

        self.FEATURES = ["tempo", "key", "loudness", "mode", "time_signature", "duration"]

        # Audio feature weights by mood
        self.mood_weights = {
            "happy" : {"tempo": 212.47, "key": 9, "loudness": -12.34, "mode": 1, "time_signature": 4, "duration": 195.0},
            "sad" : {"tempo": 58.22, "key": 2, "loudness": -38.67, "mode": 0, "time_signature": 3, "duration": 240.0},
            "chill" : {"tempo": 96.55, "key": 6, "loudness": -28.91, "mode": 1, "time_signature": 4, "duration": 210.0},
            "relax" : {"tempo": 44.19, "key": 4, "loudness": -42.77, "mode": 1, "time_signature": 3, "duration": 260.0},
            "energetic" : {"tempo": 187.63, "key": 10, "loudness": -6.58, "mode": 1, "time_signature": 4, "duration": 200.0},
            "party" : {"tempo": 171.88, "key": 11, "loudness": -3.92, "mode": 1, "time_signature": 4, "duration": 230.0},
            "focus" : {"tempo": 82.34, "key": 6, "loudness": -30.12, "mode": 1, "time_signature": 4, "duration": 300.0},
        }

        # Audio feature weights by style
        self.style_weights = {
            "car" : {"tempo": 76.41, "key": 5, "loudness": -33.55, "mode": 1, "time_signature": 4, "duration": 220.0},
            "run" : {"tempo": 198.72, "key": 10, "loudness": -5.73, "mode": 1, "time_signature": 4, "duration": 180.0},
            "workout" : {"tempo": 176.29, "key": 9, "loudness": -7.11, "mode": 1, "time_signature": 4, "duration": 210.0},
            "sleep" : {"tempo": 32.67, "key": 2, "loudness": -46.92, "mode": 0, "time_signature": 3, "duration": 360.0},
            "dance" : {"tempo": 162.45, "key": 10, "loudness": -4.36, "mode": 1, "time_signature": 4, "duration": 215.0},
            "sport" : {"tempo": 183.90, "key": 9, "loudness": -6.84, "mode": 1, "time_signature": 4, "duration": 200.0},
            "party" : {"tempo": 169.77, "key": 11, "loudness": -2.95, "mode": 1, "time_signature": 4, "duration": 240.0},
            "study" : {"tempo": 88.13, "key": 5, "loudness": -31.67, "mode": 1, "time_signature": 4, "duration": 280.0},
        }


    def apply_map(self):
        """
        Create feature vectors for the selected mood and style

        If the mood or style exists in the corresponding weight mappings,
        the predefined feature values are used. Otherwise, random values 
        are generated

        Returns:
            tuple[np.ndarray, np.ndarray]:
                A tuple containing the mood vector and style vector
        """
        if self.mood in self.mood_weights:
            mood_vec = np.array([self.mood_weights[self.mood][f] for f in self.FEATURES])
        else:
            mood_vec = np.array([
                round(random.uniform(10,300), 2), random.randint(0,11), 
                round(random.uniform(-50,0), 2), random.randint(0,1),
                round(random.uniform(10,300)),round(random.uniform(10,300))])
        
        if self.style in self.style_weights:
            style_vec = np.array([self.style_weights[self.style][f] for f in self.FEATURES])
        else:
            style_vec = np.array([
                round(random.uniform(10,300), 2), random.randint(0,11), 
                round(random.uniform(-50,0), 2), random.randint(0,1), 
                round(random.uniform(10,300)),round(random.uniform(10,300))])

        return mood_vec, style_vec
    
    def extract_terms(text: str):
        """
        Extract quoted strings from a text value

        Searches for content enclosed in either single or
        double quotation marks.

        Returns
            list of extracted strings
        """
        if pd.isna(text):
            return []
        # Finds all strings
        return re.findall(r"['\"](.*?)['\"]", str(text))

    def find_genre(self):
        """
        Search dataset for matching genre mentioned
        in the user's message

        If user inputted genre is found ***

        Returns
            vectorised genre
        """
        self.df['artist_terms_clean'] = self.df['artist_terms'].apply(self.extract_terms)

        # Build clean sorted listing of terms
        unique_values = self.df['artist_terms_clean'].explode().dropna().unique()
        unique_values = [term for term in unique_values if term.strip()]
        unique_values.sort(key=len, reverse=True)

        # Converts values into a searchable map
        pattern = r'\b(' + '|'.join(map(re.escape, unique_values)) + r')\b'

        genre = re.search(pattern, self.message)
        return genre

    def dialog_manager(self):
        """
        Generate a final audio-feature vector based on the user's
        detected mood and style preferences

        The mood and style vectors are averaged and selected
        features are normalized before being returned

        Returns
            np.ndarray
                Combined and normalized feature vector
        """
        mood_vec, style_vec = self.apply_map()
        #genre_vec = self.find_genre()

        final_vec = mood_vec + style_vec

        return final_vec


class Chatbot:
    """
    Music recommendation chatbot that interprets user requests and
    generates song or playlist recommendations based on goals,
    moods, and activity styles.

    To run chatbot
        .chat(str)
    """
    def __init__(self):
        # Neural network scoring components
        self.X = joblib.load(MODELS_PATH / "X_final.jb")
        self.recommender = SongRecommender(input_dim=self.X.shape[1], device="cpu")

        # Files for vector processing
        self.vectorizer = joblib.load(MODELS_PATH / "vectorizer.jb")
        self.svd = joblib.load(MODELS_PATH / "svd.jb")
        self.num_scaler = joblib.load(MODELS_PATH / "num_scaler.jb")

        self.message = " "

        # Regex Intent Matching Parameters
        self.intent = {
            'help': r'\b(help|assist|support|how (do|to)|what can you do|commands|options)\b',
            'recommend': r'\b(recommend|suggest|find|give me|make|create|build)\b',
            'improve': r'\b(improve|better|refine|adjust|tune)\b',
        }
        self.goal = {
            'playlist': r'\b(playlist|new playlist)\b',
            'new_song': r'\b(new song|song|something new)\b',
        }
        self.style = (r'\b(car|run|workout|sleep|dance|sport|party|study)\b')
        self.moods = (r'\b(happy|sad|chill|relax|energetic|party|focus)\b')
        self.number = (r'(\d+)\s*song')

    def detect_intent(self):
        """Routes processing flow based on matching parameters"""
        if re.search(self.intent["help"], self.message):
            return self.help()
        if re.search(self.intent["recommend"], self.message):
            return self.recommend()
        return self.confused()
    
    def detect_goal(self):
        """Determines if the output goal requests a full playlist or a single track"""
        for key,value in self.goal.items():
            goal = key
            pattern = value
            found_match = re.search(pattern, self.message)
            if found_match and goal =='playlist':
                return '0'
            elif found_match and goal =='new_song':
                return '1'
        return None
            
    def detect_style(self):
        style = re.search(self.style, self.message)
        return style
            
    def detect_mood(self):
        mood = re.search(self.moods, self.message)
        return mood
    
    def extract_number(self):
        number = re.search(self.number, self.message)
        if number:
            return number.group(1)  # Returns only the number portion
        return None

    def chat(self, user_input: str):
        """Primary interaction, normalizes input and processes matching intents."""
        self.message = user_input.lower()
        #self.message = input().lower()
        output = self.detect_intent()
        return output

    def recommend(self):
        """
        Generate song recommendations from the user's request.

        Detects goal, mood, and style to build a structured query representation.
        Vectorizes the user's message and combines feature vectors then
        generates recommendations using the recommender

        Returns 
            Recommendation
        """
        goal = self.detect_goal()
        if goal is None:
            return self.confused()
        
        style = self.detect_style()
        mood = self.detect_mood()

        # Convert categorical audio contexts to vector spaces
        manager = Dialog_Manager(style, mood, self.message) # genre
        request_text = np.array(manager.dialog_manager(), dtype=np.float32).reshape(1, -1)
        request_text_scaled = self.num_scaler.transform(request_text)

        # Vectorize user message and reduce size
        text_vector = self.vectorizer.transform([self.message])
        text_reduced = self.svd.transform(text_vector)

        #
        query_vector = np.concatenate([request_text_scaled, text_reduced], axis=1).reshape(-1)

        # Set playlist size
        if goal == '0':
            length = self.extract_number()
            k_val = int(length) if length is not None else 10
        else:
            k_val = 1 if goal == 1 else 10

        # Get recommendation results
        results = self.recommender.recommend(query_vector, k=k_val)
        return results.replace('style="text-align: right;"', 'style="text-align: left;"') 
    
    def help(self):
        return (
            "I can help you discover and refine music based on your preferences.\n\n"
            "You can ask me to:\n"
            "- Recommend music (e.g. 'recommend a playlist', 'suggest songs')\n"
            "- Create something new (e.g. 'make a workout playlist')\n\n"
            "You can specify:\n"
            "- Goal: playlist, new song\n"
            "- Style: workout, study, sleep, party, run, etc.\n"
            "- Mood: happy, sad, chill, energetic, focus, relax\n"
            "- Genre: rock, pop, rap, hip hop, jazz, edm, classical\n"
            "- Number of songs: e.g. '10 songs'\n\n"
            "Examples:\n"
            "- 'Recommend a chill study playlist'\n"
            "- 'Make a happy pop playlist with 15 songs'\n"
            "Type 'help' anytime to see this again."
        )

    def confused(self):
        return (
            "I’m not sure what you mean.\n\n"
            "Try asking for:\n"
            "- A recommendation (e.g. 'recommend a playlist')\n"
            "- A specific type of music (e.g. 'happy workout playlist')\n\n"
            "Type 'help' to see all options."
        )


if __name__ == "__main__":
    bot = Chatbot()
    out = bot.chat("make a playlist")
    print(out)
