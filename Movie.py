import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCdrOAxmJAQFAjAuJmupJeRBQuMR8IEn0c")

# Load Gemini model
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

# App title and layout
st.set_page_config(page_title="🎬 AI Movie Recommender", layout="centered")
st.title("🎬 AI Movie Recommender")

# User Preferences
st.header("Enter Your Preferences")

language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
genre = st.selectbox("Genre", ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance"])
rating = st.slider("Minimum IMDb Rating", 1.0, 10.0, 7.0, 0.5)
platform = st.selectbox("Streaming Platform", ["Netflix", "Amazon Prime", "Disney+", "Hulu", "HBO Max"])

# Output display
recommendation_placeholder = st.empty()

# Session state for regenerate
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# Prompt builder
def build_prompt():
    return f"""
    Recommend 3 great {genre} movies in {language} with at least {rating} IMDb rating that are available on {platform}.
    For each movie, include the title, a short description, and why it's worth watching.
    """

# Generate recommendations
def generate_recommendations():
    prompt = build_prompt()
    st.session_state.last_prompt = prompt
    response = model.generate_content(prompt)
    return response.text

# Generate button
if st.button("🎥 Generate Recommendations"):
    recommendations = generate_recommendations()
    recommendation_placeholder.markdown(f"### 🍿 Recommendations:\n\n{recommendations}")
    st.download_button("📥 Download", recommendations, file_name="movie_recommendations.txt")

# Regenerate button
if st.button("🔁 Regenerate"):
    if st.session_state.last_prompt:
        response = model.generate_content(st.session_state.last_prompt)
        recommendation_placeholder.markdown(f"### ♻️ New Recommendations:\n\n{response.text}")
        st.download_button("📥 Download", response.text, file_name="movie_recommendations.txt")
    else:
        st.warning("Please generate recommendations first.")
