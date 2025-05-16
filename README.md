# Study_Resource_Recommender
An intelligent and interactive web app built with Streamlit that recommends personalized study resources based on user-selected subjects, difficulty levels, and resource types (books, courses, videos, notes).
This project integrates a local dataset with live Google Custom Search API, Coursera, and Internshala searches to provide comprehensive, relevant study materials for learners.

# 🧾 Table of Contents

Project Overview

Features

Installation

Usage

Folder Structure

Dataset

APIs Used

Customization


# 🤓 Project Overview

This Study Resource Recommender System helps users find books, courses, videos, and notes based on selected subject, difficulty, and resource type. It first searches a curated local dataset, then falls back to live Google Custom Search API, Coursera, and Internshala APIs if no exact match is found locally.

The app is designed to be user-friendly with features like saving favorites, recent searches, and exporting recommendations.


# ⚡⚡ Features
Filter by Subject, Difficulty, and Resource Type: Select from a growing list of subjects including AI, Deep Learning, Cloud Computing, and more.

Local Dataset Recommendations: Fast and relevant suggestions from curated CSV data.

Live Web Search Fallback: If no local match, fetch live results from Google Custom Search, Coursera, and Internshala.

Trending Topics: Display popular current courses and topics with direct links.

Save Favorites: Add resources to favorites and export as CSV or JSON.

Recent Searches: Automatically track and show recent user searches.

Light/Dark Mode: Comfortable reading modes toggle.

Download Recommendations: Export your recommended resources for offline use.


# 📩 Installation

**Clone the repository:**
bash
git clone https://github.com/yourusername/study-resource-recommender.git
cd study-resource-recommender

**Install required packages:**
bash
pip install -r requirements.txt

**Set your Google Custom Search API credentials:**
Get your API key and Search Engine ID from Google Cloud Console.

Add them in utils/google_search.py or use environment variables.


# ⭐ Usage

**Run the Streamlit app:**
bash
streamlit run app.py

Open the displayed localhost URL in your browser. Use the sidebar filters to select subject, difficulty, and resource type, then hit Search to get recommendations.


# 📂 Folder Structure

study-resource-recommender/

app.py                   # Main Streamlit app

requirements.txt         # Python dependencies

LICENSE                  # MIT License

README.md                # This README file

data/
    resources.csv        # Local study resource dataset

utils/
   recommender.py       # Recommendation engine logic
   google_search.py     # Google Custom Search integration

assets/                  # Images, logos, CSS (optional)


# 📊 Dataset

The local dataset resources.csv contains curated study materials with fields like:

title: Resource title

subject: Subject category

difficulty: Difficulty level (Beginner, Intermediate, Advanced)

platform: Platform or source name (e.g., Coursera, W3Schools)

resource_type: Book, Course, Video, Notes

link: URL to the resource

You can easily expand or customize the dataset for your needs.


# 🔍 APIs Used

Google Custom Search API

Coursera public course links (scraped or API-based)

Internshala course links (scraped or API-based)

Make sure to get API credentials and set usage limits accordingly.


# 💜 Customization

Add more subjects, difficulties, or resource types in resources.csv and update recommender filters.

Modify trending topics and links in app.py.

Adjust UI styling by customizing Streamlit components or adding CSS in the assets folder.

