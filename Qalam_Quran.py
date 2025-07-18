import streamlit as st
import requests
import base64
import tempfile
import openai
import os
from io import BytesIO
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from quran_api import get_surah_list, get_surah, get_verse_audio_url

# Configuration API OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Interface Streamlit
st.set_page_config(page_title="Qalam Quran", layout="centered")
st.title("🕌 Qalam Quran - Assistant pour découvrir le Coran et la langue arabe")

# 1. Sélection de la sourate
st.subheader("1. Choisis une sourate")
response = requests.get("https://api.quran.com/v4/chapters")
data = response.json()
surah_list = response.json()["chapters"]
surah_names = [f"{s['id']}. {s['name_arabic']} ({s['name_simple']})" for s in surah_list]
surah_id = st.selectbox("Sourate", surah_names)
surah_number = int(surah_id.split(".")[0])
# 2. Affichage des versets
st.subheader("2. Versets avec audio")
verses = requests.get(f"https://api.quran.com/v4/quran/verses/uthmani?chapter_number={surah_number}").json()["verses"]
selected_verse = st.selectbox("Choisis un verset", [f"{v['verse_number']}: {v['text_uthmani'][:30]}..." for v in verses])
selected_verse_number = int(selected_verse.split(":")[0])
verse_text = next(v['text_uthmani'] for v in verses if v['verse_number'] == selected_verse_number)
st.markdown(f"**Verset {selected_verse_number} :** {verse_text}")

# 3. Upload et analyse audio utilisateur avec Whisper
st.subheader("3. Récite et téléverse ton audio")
user_audio = st.file_uploader("Téléverse un fichier .wav ou .mp3 contenant ta récitation", type=["wav", "mp3"])

if user_audio:
    st.audio(user_audio)
    st.success("Audio reçu. Analyse avec Whisper en cours...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(user_audio.read())
        tmp_path = tmp.name
    try:
        with open(tmp_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        user_text = transcript["text"]
        st.markdown(f"📝 **Transcription Whisper :** {user_text}")
        missing_words = [word for word in verse_text.split() if word not in user_text]
        if missing_words:
            st.warning("❗ Mots manquants ou mal prononcés : " + ", ".join(missing_words))
        else:
            st.success("✅ Récitation correcte !")
    except Exception as e:
        st.error(f"Erreur d'analyse Whisper : {e}")

# 4. Explication GPT
st.subheader("4. Explication du verset avec GPT")
if st.button("🧠 Générer l'explication du verset"):
    with st.spinner("Appel à GPT..."):
        prompt = f"Explique ce verset du Coran en arabe simple et donne aussi son sens spirituel pour un débutant : {verse_text}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un professeur bienveillant d'arabe coranique."},
                    {"role": "user", "content": prompt}
                ]
            )
            explanation = response["choices"][0]["message"]["content"]
            st.markdown("### 🧠 Explication")
            st.write(explanation)
        except Exception as e:
            st.error(f"Erreur GPT : {e}")

# 5. Suivi de progression
st.subheader("5. Suivi de ta progression")
if "history" not in st.session_state:
    st.session_state.history = []
if user_audio and 'user_text' in locals():
    st.session_state.history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sourate": surah_id,
        "verset": selected_verse_number,
        "transcription": user_text,
        "erreurs": missing_words if missing_words else []
    })
if st.button("📊 Voir l'historique"):
    st.markdown("### Historique des récitations")
    for item in st.session_state.history:
        st.markdown(f"- {item['date']} - {item['sourate']} - Verset {item['verset']} - Erreurs : {', '.join(item['erreurs']) if item['erreurs'] else 'Aucune'}")
    df = pd.DataFrame(st.session_state.history)
    if not df.empty:
        df["nb_erreurs"] = df["erreurs"].apply(lambda x: len(x))
        fig, ax = plt.subplots()
        ax.plot(df["date"], df["nb_erreurs"], marker='o')
        ax.set_ylabel("Erreurs")
        ax.set_xlabel("Date")
        ax.set_title("📈 Évolution du nombre d'erreurs")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# 6. Plan de révision intelligent
if st.button("📅 Planifier ma révision"):
    erreur_freq = {}
    for h in st.session_state.history:
        for err in h["erreurs"]:
            erreur_freq[err] = erreur_freq.get(err, 0) + 1
    sorted_erreurs = sorted(erreur_freq.items(), key=lambda x: -x[1])
    st.markdown("### 🔁 Mots à revoir en priorité :")
    for mot, freq in sorted_erreurs:
        st.markdown(f"- {mot} ({freq} erreurs)")

# 7. Vocabulaire enrichi
st.subheader("6. Vocabulaire extrait du verset")
if verse_text:
    vocabulaire = set(verse_text.split())
    for mot in vocabulaire:
        st.markdown(f"- **{mot}** (🔁 Revoir ce mot)")

# Pied de page
st.markdown("""
---
📘 *Qalam Quran est un prototype pour découvrir le Coran, verset par verset, et apprendre la langue arabe. D'autres fonctionnalités à venir inshAllah.*
""")
