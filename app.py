import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# ---- Genius API Setup ----
GENIUS_API_TOKEN = "iet8moSWSDWEzmKx8EOAOWDq2bRfp9ns4RcbNFHtYDx84W_JdkopJwWKYSi8fUfv"
try:
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN, 
                               skip_non_songs=True, 
                               excluded_terms=["(Remix)", "(Live)"],
                               remove_section_headers=True)
    genius.verbose = False
    genius.timeout = 15  # increase timeout
    genius.sleep_time = 0.5  # add delay between requests
except Exception as e:
    st.error(f"Failed to initialize Genius API: {e}")
    st.stop()

# ---- Streamlit UI Setup ----
st.set_page_config(page_title="Taylor Swift Lyrics Visualizer", layout="centered")
st.title("🎤 Sing with Streamlit: Taylor Swift Lyrics Visualizer")
st.markdown("Enter a **Taylor Swift** song title to fetch lyrics and generate a word cloud.")

# ---- Input Field ----
song_title = st.text_input("Enter Song Title (e.g., 'Love Story')", "Love Story")

def clean_lyrics(lyrics):
    """Remove unwanted text from lyrics (like 'Embed' and numbers)"""
    lyrics = re.sub(r'\d*Embed$', '', lyrics)  # Remove "123Embed" at end
    lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove [Verse], [Chorus], etc.
    return lyrics.strip()

if st.button("Fetch Lyrics"):
    if not song_title:
        st.warning("Please enter a song title.")
    else:
        with st.spinner(f"Searching for '{song_title}'..."):
            try:
                # Force Taylor Swift as artist to improve search accuracy
                song = genius.search_song(song_title, artist="Taylor Swift")
                
                if song is None:
                    st.error("Song not found. Try a different title or check spelling.")
                else:
                    lyrics = clean_lyrics(song.lyrics)
                    
                    if not lyrics or len(lyrics) < 20:  # basic validation
                        st.error("Lyrics found but appear to be incomplete or empty.")
                    else:
                        st.subheader(f"🎶 {song.title} Lyrics")
                        st.text_area("Lyrics", lyrics, height=300)

                        # ---- Word Cloud ----
                        st.subheader("☁️ Word Cloud")
                        wordcloud = WordCloud(width=800, height=400, 
                                            background_color='white',
                                            collocations=False).generate(lyrics)

                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis("off")
                        st.pyplot(fig)
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("This might be a temporary issue. Try again later or with a different song.")
