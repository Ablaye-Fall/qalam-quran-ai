# 🕌 Qalam Quran

**Qalam Quran** est un assistant intelligent pour découvrir le Coran, verset par verset, et apprendre la langue arabe de manière interactive.

## 📌 Fonctionnalités principales

- 🔊 Récitation avec retour vocal et transcription automatique (via Whisper)
- 🧠 Explication du verset avec GPT
- 📈 Suivi des progrès de récitation
- 🔁 Plan de révision intelligent basé sur les erreurs
- 📘 Extraction et enrichissement du vocabulaire
- 🎧 Bouton “Revoir ce mot” (à venir)

## 🚀 Lancer l'application

1. Installer Python et Streamlit
2. Cloner ce repo :
```bash
git clone https://github.com/ton-utilisateur/qalam-quran.git
cd qalam-quran
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Créer un fichier `.streamlit/secrets.toml` :
```toml
OPENAI_API_KEY = "ta_clé_openai"
```

5. Lancer l'app :
```bash
streamlit run app/Qalam_Quran.py
```

---

**💡 Créé pour ceux qui veulent apprendre le Coran avec douceur, intelligence et clarté.**
