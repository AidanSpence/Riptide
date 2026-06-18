# Riptide

Riptide is an innovative AI music recommendation system that utilizes machine learning with a clustering backend. By combining collaborative filtering concepts with deep data clustering, Riptide creates a hybrid recommendation engine designed to maximize musical diversity while requiring minimal user data.

> **Status:** Currently in a Minimum Viable Product (MVP) state.


## Key Features

* **Clustering Backend:** Groups music by deep sonic and metadata attributes to find hidden connections between tracks.
* **Hybrid System:** Blends user preference mapping with algorithmic discovery to break user "filter bubbles."
* **Cold Start Friendly:** Delivers highly accurate, diverse recommendations using minimal initial user data.
* **Powered by Scale:** Built utilizing data insights from the massive Million Song Dataset.


## Live Demo

The latest build of Riptide is deployed and available on the cloud:
**[Riptide Live Deployment](CLOUD_UPLOAD_LINK_HERE)**


## Dataset Reference

This project utilizes the **[Million Song Dataset](http://millionsongdataset.com/)**, a freely-accessible collection of audio features and metadata for a million contemporary popular music tracks, authored by Thierry Bertin-Mahieux.


## Getting Started

Follow these instructions to get a copy of the MVP up and running on your local machine.

### Prerequisites

* Python 3.10+
* Pip (Python package manager)
* [MillionSongSubset](http://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz) <-- for backend code

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AidanSpence/Riptide.git](https://github.com/AidanSpence/Riptide.git)
   cd riptide

### Running Code

To run Ai system independently
python -m _Recommendation_System_.Frontend.chatbot

To starts an html server on port 5500 for loading website
python -m http.server 5500
