import streamlit as st
from quran_api import get_surah_list, get_surah, get_verse_audio_url

st.set_page_config(page_title="Qalam Quran AI", layout="centered")

st.title("📖 Qalam-Quran-AI : Lecture interactive du Coran")

# Récupérer la liste des sourates
surahs = get_surah_list()
surah_names = [f"{s['number']}. {s['englishName']} - {s['name']}" for s in surahs]
surah_map = {name: s['number'] for name, s in zip(surah_names, surahs)}

# Sélecteur de sourate
selected_surah = st.selectbox("Choisis une sourate :", surah_names)

if selected_surah:
    surah_number = surah_map[selected_surah]
    # Récupérer la sourate en arabe et traduction française
    surah_ar = get_surah(surah_number, "ar")
    surah_fr = get_surah(surah_number, "fr.hamidullah")

    st.markdown(f"## {surah_ar['englishName']} - {surah_ar['name']}")

    for aya_ar, aya_fr in zip(surah_ar['ayahs'], surah_fr['ayahs']):
        st.markdown(f"**{aya_ar['numberInSurah']}**. {aya_ar['text']}  \n➜ _{aya_fr['text']}_")

        # Affichage du lecteur audio pour chaque verset
        audio_url = get_verse_audio_url(aya_ar["number"])
        st.audio(audio_url, format="audio/mp3")
