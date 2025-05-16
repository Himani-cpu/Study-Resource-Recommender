import streamlit as st
import pandas as pd
import json
from utils.recommender import Recommender
from utils.google_search import google_search

st.set_page_config(page_title="📚 Study Resource Recommender", layout="wide")

# Initialize session state variables
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Title
st.title("📚 Study Resource Recommender")

recommender = Recommender()

# Sidebar
with st.sidebar:
    st.header("🔍 Search Filters")
    subject = st.selectbox("Select Subject", recommender.get_subjects())
    difficulty = st.selectbox("Select Difficulty", recommender.get_difficulties())
    resource_type = st.selectbox("Select Resource Type", ["All", "Book", "Course", "Video", "Notes", "Web"])
    specific_topic = st.text_input("Enter Specific Topic (optional)")
    search_btn = st.button("Search")

    # Dark/Light mode toggle
    if st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode):
        st.session_state.dark_mode = True
        st.markdown(
            """
            <style>
            body, .main, .sidebar .sidebar-content {
                background-color: #121212;
                color: white;
            }
            a, .st-bx {
                color: #bb86fc;
            }
            </style>
            """, unsafe_allow_html=True
        )
    else:
        st.session_state.dark_mode = False
        st.markdown("", unsafe_allow_html=True)  # Reset styles

    # Favorites display and download
    st.markdown("### ❤️ Favorites")
    if st.session_state.favorites:
        for i, fav in enumerate(st.session_state.favorites):
            st.markdown(f"**{fav['title']}** ({fav['platform']}, {fav['difficulty']})")
        if st.button("Download Favorites CSV"):
            fav_df = pd.DataFrame(st.session_state.favorites)
            st.download_button("Download CSV", data=fav_df.to_csv(index=False), file_name="favorites.csv")
        if st.button("Download Favorites JSON"):
            st.download_button("Download JSON", data=json.dumps(st.session_state.favorites), file_name="favorites.json")
    else:
        st.write("No favorites added yet.")

    # Recent searches display
    st.markdown("### 🕒 Recent Searches")
    if st.session_state.recent_searches:
        for rs in st.session_state.recent_searches[-5:][::-1]:
            st.write(f"- {rs}")
    else:
        st.write("No recent searches.")

# Trending section with links
st.markdown("## 🔥 Trending Topics")
trending = {
    "AI Tools": "https://www.coursera.org/search?query=ai%20tools",
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "App Development": "https://www.udemy.com/topic/app-development/",
    "Prompt Engineering": "https://www.coursera.org/search?query=prompt%20engineering",
    "Data Science": "https://www.coursera.org/specializations/jhu-data-science",
    "Deep Learning": "https://www.deeplearning.ai/",
    "Cloud Computing": "https://www.coursera.org/specializations/google-cloud-platform",
}
for topic, link in trending.items():
    st.markdown(f"- **[{topic}]({link})**")

# Process search
if search_btn:
    st.session_state.search_clicked = True
    # Save recent search
    search_summary = f"{subject} | {difficulty} | {resource_type}"
    if specific_topic.strip():
        search_summary += f" | {specific_topic.strip()}"
    st.session_state.recent_searches.append(search_summary)

if st.session_state.search_clicked:
    # Get recommendations from local db
    results = recommender.recommend(subject, difficulty, resource_type, specific_topic)

    st.markdown("## 🎓 Recommendations")

    if results:
        for idx, res in enumerate(results[:10]):
            with st.form(key=f"form_{idx}"):
                st.markdown(f"**{res['title']}**")
                st.markdown(f"*Platform:* {res['platform']} | *Level:* {res['difficulty']} | *Type:* {res.get('type', 'N/A')}")
                st.markdown(f"[🔗 Resource Link]({res['link']})")
                if res.get('description'):
                    st.markdown(f"_{res['description']}_")

                add_fav = st.form_submit_button("Add to Favorites ❤️")
                if add_fav:
                    if res not in st.session_state.favorites:
                        st.session_state.favorites.append(res)
                        st.success(f"Added '{res['title']}' to favorites.")
                    else:
                        st.info(f"'{res['title']}' is already in favorites.")
            st.markdown("---")

    else:
        st.warning("No exact matches found in our local database. Trying Google Search...")

        # Prepare query for Google Search based on inputs
        base_query = f"{difficulty} {subject}"
        if specific_topic.strip():
            base_query += f" {specific_topic.strip()}"
        if resource_type != "All":
            base_query += f" {resource_type}"

        google_results = google_search(base_query, max_results=10)

        if google_results:
            st.success("Here are some web results from Google:")
            for idx, g in enumerate(google_results):
                with st.form(key=f"google_form_{idx}"):
                    st.markdown(f"**{g['title']}**")
                    st.markdown(f"[🔗 {g['link']}]({g['link']})")
                    st.markdown(f"_{g['description']}_")
                    add_fav = st.form_submit_button("Add to Favorites ❤️")
                    if add_fav:
                        fav_item = {
                            "title": g['title'],
                            "link": g['link'],
                            "platform": "Web",
                            "difficulty": difficulty,
                            "type": resource_type,
                            "description": g['description']
                        }
                        if fav_item not in st.session_state.favorites:
                            st.session_state.favorites.append(fav_item)
                            st.success(f"Added '{g['title']}' to favorites.")
                        else:
                            st.info(f"'{g['title']}' is already in favorites.")
                st.markdown("---")

            # Download google search results csv/json
            if st.button("Download Google Results CSV"):
                g_df = pd.DataFrame(google_results)
                st.download_button("Download CSV", data=g_df.to_csv(index=False), file_name="google_results.csv")
            if st.button("Download Google Results JSON"):
                st.download_button("Download JSON", data=json.dumps(google_results), file_name="google_results.json")

        else:
            st.error("No results found from Google Search API.")
