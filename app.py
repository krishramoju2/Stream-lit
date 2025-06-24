import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---- Genius API Setup ----
GENIUS_API_TOKEN = "1sIQ_ISmltVhZf_wKbgKKULHpu5Bc5ATiWFIJayHaAiba3pd2VqWfqmasG7PFPdm"
genius = lyricsgenius.Genius(GENIUS_API_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])
genius.verbose = False  # optional: hides logs in console

# ---- Streamlit UI Setup ----
st.set_page_config(page_title="Taylor Swift Lyrics Visualizer", layout="centered")

st.title("🎤 Sing with Streamlit: Taylor Swift Lyrics Visualizer")
st.markdown("Enter a **Taylor Swift** song title to fetch lyrics and generate a word cloud.")

# ---- Input Field ----
song_title = st.text_input("Enter Song Title (e.g., 'Love Story')")

if st.button("Fetch Lyrics"):
    if not song_title:
        st.warning("Please enter a song title.")
    else:
        with st.spinner("Fetching lyrics..."):
            try:
                song = genius.search_song(song_title, "Taylor Swift")
                if song and song.lyrics:
                    lyrics = song.lyrics
                    st.subheader("🎶 Lyrics")
                    st.text_area("Lyrics", lyrics, height=300)

                    # ---- Word Cloud ----
                    st.subheader("☁️ Word Cloud")
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)

                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.error("Song not found or lyrics not available.")
            except Exception as e:
                st.error(f"Error: {e}")
