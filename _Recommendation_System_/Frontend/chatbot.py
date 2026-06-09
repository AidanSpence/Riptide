import re
import random
import numpy as np
import joblib
from pathlib import Path
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
        """
        
        """
        self.style = style.group(0) if style else None
        self.mood = mood.group(0) if mood else None
        #self.genre = genre.group(0) if genre else None
        self.df = joblib.load(MODELS_PATH / "df.jb")
        self.text = message
        self.mood_weights = {
            "happy" : {"tempo": 212.47, "key": 9, "loudness": -12.34, "mode": 1},
            "sad" : {"tempo": 58.22, "key": 2, "loudness": -38.67, "mode": 0},
            "chill" : {"tempo": 96.55, "key": 6, "loudness": -28.91, "mode": 1},
            "relax" : {"tempo": 44.19, "key": 4, "loudness": -42.77, "mode": 1},
            "energetic" : {"tempo": 187.63, "key": 10, "loudness": -6.58, "mode": 1},
            "party" : {"tempo": 171.88, "key": 11, "loudness": -3.92, "mode": 1},
            "focus" : {"tempo": 82.34, "key": 6, "loudness": -30.12, "mode": 1},
        }

        self.style_weights = {
            "car" : {"tempo": 76.41, "key": 5, "loudness": -33.55, "mode": 1},
            "run" : {"tempo": 198.72, "key": 10, "loudness": -5.73, "mode": 1},
            "workout" : {"tempo": 176.29, "key": 9, "loudness": -7.11, "mode": 1},
            "sleep" : {"tempo": 32.67, "key": 2, "loudness": -46.92, "mode": 0},
            "dance" : {"tempo": 162.45, "key": 10, "loudness": -4.36, "mode": 1},
            "sport" : {"tempo": 183.90, "key": 9, "loudness": -6.84, "mode": 1},
            "party" : {"tempo": 169.77, "key": 11, "loudness": -2.95, "mode": 1},
            "study" : {"tempo": 88.13, "key": 5, "loudness": -31.67, "mode": 1},
        }
        self.FEATURES = ["tempo", "key", "loudness", "mode"]

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
            mood_dict = self.mood_weights[self.mood]
            mood_vec = np.array([mood_dict[f] for f in self.FEATURES])
        else:
            mood_vec = np.array([round(random.uniform(10,300), 2), random.randint(0,11), round(random.uniform(-50,0), 2), random.randint(0,1)])
        print(mood_vec)
            

        if self.style in self.style_weights:
            style_dict = self.style_weights[self.style]
            style_vec = np.array([style_dict[f] for f in self.FEATURES])
        else:
            style_vec = np.array([round(random.uniform(10,300), 2), random.randint(0,11), round(random.uniform(-50,0), 2), random.randint(0,1)])
        print(style_vec)

        return mood_vec, style_vec
    
    def extract_terms(text):
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

        # Extract all unique values then Remove any blank empty strings caused by double quotes
        # and sort by length so longer phrases match before shorter sub-words
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

        
        """
        mood_vec, style_vec = self.apply_map()
        genre_vec = self.find_genre()

        final_vec = 0.5 * mood_vec + 0.5 * style_vec
        final_vec[0] /= 200.0  # Normalise tempo
        final_vec[1] /= 11.0 # Normalise key

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
        """
        Initialize the chatbot and load all required models

        Loads:
        - Feature matrix used by the recommender
        - Trained SongRecommender model
        - Text vectorizer

        Initializes:
        - Intent detection patterns
        - Goal detection patterns
        - Style and mood patterns
        - Song count extraction pattern
        """
        self.X =joblib.load(MODELS_PATH / "X_final.jb")
        self.recommender = SongRecommender(input_dim=self.X.shape[1], device="cpu")
        self.vectorizer = joblib.load(MODELS_PATH / "vectorizer.jb")
        self.message = " "
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
        """
        Determines user's primary intent

        Run's the appropriate method for handling
        users message

        Returns
            str from appropriate method
        """
        if re.search(self.intent["help"], self.message):
            return self.help()

        if re.search(self.intent["recommend"], self.message):
            return self.recommend()
        
        return self.confused()
    
    def detect_goal(self):
        """
        Detect the recommendation goal

        Returns
            0 : Playlist recommendation
            1 : Single song recommendation
            None : No goal detected
        """
        for key,value in self.goal.items():
            goal = key
            pattern = value
            found_match = re.search(pattern, self.message)
            if found_match and goal =='playlist':
                return 0
            elif found_match and goal =='new_song':
                return 1
            
    def detect_style(self):
        """
        Detect an activity or usage context from the user message
        Returns
            Regex match object if a style is found,
            otherwise None
        """
        style = re.search(self.style, self.message)
        return style
            
    def detect_mood(self):
        """
        Detect the user's desired mood from message

        Returns
            Regex match object if a mood is found,
            otherwise None
        """
        mood = re.search(self.moods, self.message)
        return mood
    
    def extract_number(self):
        """
        Extract the requested number of songs

        Returns
            Extracted numeric value as a string,
            or None if no number is found
        """
        number = re.search(self.number, self.message)
    
        if number:
            return number.group(1)  # Returns only the number portion
        return None

    def chat(self, user_input: str):
        """
        Processes a user message and generates a response.

        The input text is converted to lowercase and stored
        before intent detection is performed.

        Returns
            output <-- Chatbot response
        """
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
        style = self.detect_style()
        mood = self.detect_mood()
        #genre = self.detect_genre()

        manager = Dialog_Manager(style, mood, self.message) # genre
        request_text = manager.dialog_manager()
        text_vector = self.vectorizer.transform([self.message]).toarray()[0]
        query_vector = np.concatenate([request_text,text_vector])

        if goal == 0:
            length = self.extract_number()
            k_val = int(length) if length is not None else 10
        elif goal == 1:
            k_val = 1
        else:
            k_val = 10
        
        results = self.recommender.recommend(query_vector, k=k_val)
        return results
    
    def help(self):
        """
        Returns the Chatbot help message

        Returns
            str
        """
        return """I can help you discover and refine music based on your preferences.

You can ask me to:
- Recommend music (e.g. "recommend a playlist", "suggest songs")
- Create something new (e.g. "make a workout playlist")

You can specify:
- Goal: playlist, new song
- Style: workout, study, sleep, party, run, etc.
- Mood: happy, sad, chill, energetic, focus, relax
- Genre: rock, pop, rap, hip hop, jazz, edm, classical
- Number of songs: e.g. "10 songs"

Examples:
- "Recommend a chill study playlist"
- "Make a happy pop playlist with 15 songs"
- "Suggest a new rock song"
- "Improve this playlist to be more energetic"

Type "help" anytime to see this again.
"""
#- Improve results (e.g. "make it more energetic", "adjust the mood")

    def confused(self):
        """
        Returns a Chatbot fallback response when users message is 
        not understood

        Returns
            str
        """
        return """I’m not sure what you mean.

Try asking for:
- A recommendation (e.g. "recommend a playlist")
- A specific type of music (e.g. "happy workout playlist")

Type "help" to see all options."""


if __name__ == "__main__":
    bot = Chatbot()
    out = bot.chat("make a playlist")
    print(out)
    
