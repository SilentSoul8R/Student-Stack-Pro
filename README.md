# 🎓 Student Stack Pro

An all-in-one AI workspace built with **Python · CrewAI · Groq · Streamlit**.

| Tool | What it does |
|---|---|
| 🔎 Research Agents | 3-agent crew (Researcher → Reviewer → Writer): reports, summaries, briefings, study guides. Optional live web search. |
| ✉️ Email Writer | Writer + Proofreader agents, multiple options, tone/language control, “open in mail app”. |
| 💼 LinkedIn Posts | Strategist + Copywriter agents, hooks, hashtags, live post preview. |
| 📚 PDF Study Lab | RAG (TF-IDF retrieval) over PDFs: notes, flashcards (Anki export), Q&A with page citations. |
| 🖼️ Slide Reader | `.pptx`/PDF decks → slide-by-slide notes, summary, glossary, practice questions, cheat-sheet. |
| 🗓️ Timetable Maker | Deterministic clash-free scheduler + optional AI planner (AI output is validated), `.ics` + CSV export. |
| 📝 Writer's Desk | Markdown editor, offline Grammarly-style checks, readability score, AI rewrite with diff, `.docx` export. |
| 📄 Resume Studio | Form → live preview → PDF / Word; AI polish, tailor to a job ad, import from pasted text. |

## 📥 Downloads
PDF, Word and Markdown for research, notes, slide notes and the editor · printable double-sided **flashcard PDF**, Quizlet CSV and Anki TSV · timetable CSV/.ics · resume PDF/Word ·
**💾 Workspace backup (JSON)** in the sidebar saves and restores your documents, resume, notes, cards and timetable. It never contains your API key or uploaded files.

## Run locally
```bash
git clone https://github.com/<you>/student-stack-pro.git && cd student-stack-pro
python3.11 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/check_env.py          # confirms every package imports
streamlit run app.py
```
Get a free key at <https://console.groq.com>, paste it in **AI settings** (sidebar). Optional: `pip install -r requirements-optional.txt` for web search.

## 🔒 API-key privacy
* The key is entered in a password field and held **only in Streamlit session memory** — never written to disk, logs or `os.environ`.
* It's passed straight to CrewAI's `LLM` object; error messages are scrubbed so it can't leak.
* `.env` and `.streamlit/secrets.toml` are in `.gitignore`. **Never commit a real key.** If you ever do, revoke it in the Groq console.
* CrewAI telemetry/tracing is disabled in code.
* **Public deployments:** do *not* put your own key in secrets unless you accept strangers spending your quota. Either leave it unset (each visitor pastes their own key) or set `REQUIRE_USER_KEY = "true"`.


=======
## 🚀 Deploy from GitHub (Streamlit Community Cloud)
1. Push this folder to a GitHub repo (`git init && git add . && git commit -m "init" && git push`). Check `git status` shows no `.env`/`secrets.toml`.
2. Go to <https://share.streamlit.io> → **New app** → pick the repo, branch `main`, file `app.py`.
3. **Advanced settings → Python version: 3.11.**
4. (Optional) **Secrets**: `GROQ_API_KEY = "gsk_..."` for a private/personal app, or `REQUIRE_USER_KEY = "true"` for a public one.
5. Deploy. First build takes a few minutes (CrewAI is large).

Docker: `docker build -t student-stack-pro . && docker run -p 8501:8501 student-stack-pro`

## Project layout
```
app.py                 navigation, home, error shield
core/llm.py            Groq+CrewAI runner, key handling, retries, JSON parsing
core/utils.py          PDF/PPTX readers, chunking, TF-IDF retriever, md→docx
core/scheduler.py      timetable engine + AI-output validator + .ics
core/textcheck.py      offline grammar/style checks, diff
core/resume_render.py  resume HTML / PDF / DOCX
modules/*.py           one file per tool (UI + agents)
tests/                 offline unit tests (no API key needed)
```

## Notes & limits
* Groq's free tier has token-per-minute limits; the app retries on rate limits. Use `llama-3.1-8b-instant` for speed, `llama-3.3-70b-versatile` for quality. Model ids can change — use **Custom…** in AI settings.
* Scanned PDFs/images need OCR, which isn't included. PDF resumes use standard Latin fonts.
* If you use CrewAI ≥ 1.0, install `pip install "crewai[litellm]"` (Groq goes through LiteLLM) and re-run `check_env.py`.
<<<<<<< HEAD
* AI output can be wrong — review before sending or submitting.
=======
* AI output can be wrong so please review before sending or submitting.
>>>>>>> 59511f36a8fa45a6c79ff526e281d24485767581

## Tests
`pip install pytest && pytest -q` (offline; covers scheduler, retrieval, text checks, resume PDF/DOCX).
