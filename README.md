# 🎬 CineSage

**AI-Powered Movie Information Extraction**

CineSage is a smart tool that reads a natural-language movie description and extracts the key information about it — cast, director, genre, ratings, plot, awards, and more — all in a clean, structured format. The web app is powered by **LangChain** and **Google Gemini**, and comes with a polished **Streamlit** interface.

---

## ✨ Features

- 🎬 **Movie Metadata** — name, genre, director, release year, production company
- 👥 **Main Cast** — listed as a clean array
- 📖 **Plot & Story** — a concise summary of the narrative
- ⭐ **Ratings** — IMDb, Rotten Tomatoes, Metacritic (when mentioned)
- 🏆 **Awards & Recognition** — notable honors and achievements
- 🎭 **Themes & Setting** — key motifs and locations
- 🎼 **Music & Runtime** — composer, runtime, and box office details
- 🔑 **Keywords** — 5–10 important keywords for quick scanning
- 📥 **Downloadable Results** — export the extracted info as a text file
- 🌙 **Dark, modern UI** — built with Streamlit and custom CSS

---

## 🧱 Tech Stack

| Technology | Purpose |
|------------|---------|
| [Python](https://www.python.org/) | Core programming language |
| [LangChain](https://www.langchain.com/) | Prompt templating & LLM orchestration |
| [Google Gemini](https://ai.google.dev/) | Language model for web extraction |
| [Streamlit](https://streamlit.io/) | Web interface |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |

---

## 📁 Project Structure

```
CineSage/
├── core.py          # Legacy command-line extractor (Mistral)
├── ui.py            # Streamlit web interface (Gemini)
└── README.md        # You are here
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python **3.9+**
- A free [Gemini API key](https://aistudio.google.com/apikey)

### 2. Clone the repository

```bash
git clone https://github.com/Mahdeen52/CineSage.git
cd CineSage
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root and add your Gemini key:

```bash
GEMINI_API_KEY=your_api_key_here
# Optional; defaults to gemini-3.6-flash
GEMINI_MODEL=gemini-3.6-flash
```

For Streamlit Community Cloud, add `GEMINI_API_KEY` (and optionally
`GEMINI_MODEL`) under **Manage app → Settings → Secrets** instead. Changes to
the local `.env` file are not deployed because that file is intentionally
excluded from Git.

### 5. Run the app

**Web interface (recommended):**

```bash
streamlit run ui.py
```

**Command-line version:**

```bash
python core.py
```

The legacy command-line version still uses `MISTRAL_API_KEY`; the Streamlit web
app does not.

---

## 🖥️ Usage

1. Launch the Streamlit app.
2. Paste a movie description in the text area (e.g. *"Interstellar is a 2014 science fiction film directed by Christopher Nolan..."*).
3. Click **✨ Extract Information**.
4. Review the structured result and click **📥 Download Result** to save it.

---

## 📝 Example Output

For a description like:

> *Interstellar is a 2014 science fiction film directed by Christopher Nolan, starring Matthew McConaughey and Anne Hathaway...*

CineSage returns a clean, structured breakdown of:

```
- Movie Name: Interstellar
- Genre: Sci-Fi / Drama
- Director: Christopher Nolan
- Release Year: 2014
- Main Cast: Matthew McConaughey, Anne Hathaway, ...
- Plot: ...
- IMDb Rating: 8.7
- Awards: ...
- Keywords: ...
```

---

## 🛠️ Customization

Want to tweak the extraction fields? Open `core.py` and edit the system prompt inside the `ChatPromptTemplate`. The prompt lists every field CineSage extracts, so you can easily add or remove fields to match your needs.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🧑‍💻 Author

Built with ❤️ by [Mahdeen52](https://github.com/Mahdeen52).

---

**© 2026 CineSage • AI Movie Information Extractor**
