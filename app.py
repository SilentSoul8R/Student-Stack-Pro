"""Student Stack Pro — 8 AI tools in one Streamlit app (CrewAI + Groq)."""
import importlib

import streamlit as st

st.set_page_config(page_title="Student Stack Pro", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

from core import backup, llm, ui  # noqa: E402  (must come after set_page_config)

PAGES = {
    "🏠 Home": (None, ""),
    "🔎 Research Agents": ("modules.research", "Reports, summaries and study guides from any topic."),
    "✉️ Email Writer": ("modules.email_agent", "Polished emails in any tone and language."),
    "💼 LinkedIn Posts": ("modules.linkedin", "Posts in your voice, with hooks and hashtags."),
    "📚 PDF Study Lab": ("modules.study_rag", "RAG over your PDFs: notes, flashcards, Q&A."),
    "🖼️ Slide Reader": ("modules.slides", "Slides in, comprehensive notes and quizzes out."),
    "🗓️ Timetable Maker": ("modules.timetable", "Clash-free weekly plan with .ics export."),
    "📝 Writer's Desk": ("modules.editor", "Word-like editor with grammar checks and AI."),
    "📄 Resume Studio": ("modules.resume", "Beautiful resumes as PDF or Word."),
}
LABELS = list(PAGES)


def go(label: str) -> None:
    st.session_state["nav"] = label


def home() -> None:
    ui.hero("Student Stack Pro 🎓", "Eight AI agents for study, work and career — powered by CrewAI and Groq.")
    if not llm.get_api_key():
        st.info("👈 Start by adding your free Groq API key in **AI settings** in the sidebar "
                "(get one at console.groq.com). Tools that don't need AI — timetable, editor checks — work right away.")
    tools = LABELS[1:]
    for row in range(0, len(tools), 4):
        cols = st.columns(4)
        for col, label in zip(cols, tools[row:row + 4]):
            with col, st.container(border=True):
                st.markdown(f"### {label}")
                st.caption(PAGES[label][1])
                st.button("Open →", key=f"open_{label}", on_click=go, args=(label,), use_container_width=True)
    st.markdown("#### 🔒 Privacy by design")
    st.markdown("- Your API key stays in this session's memory — never saved to disk, logs or the repo.\n"
                "- Uploaded files and text are processed in memory and discarded when you close the tab.\n"
                "- CrewAI telemetry is switched off. Only the text needed for a request is sent to Groq.")


def main() -> None:
    ui.inject_css()
    st.session_state.setdefault("nav", LABELS[0])
    with st.sidebar:
        st.markdown("## 🎓 Student Stack Pro")
        st.radio("Tools", LABELS, key="nav", label_visibility="collapsed")
    llm.sidebar_settings()
    backup.sidebar_backup()
    st.sidebar.caption("🔒 Key is session-only · telemetry off")
    page = st.session_state["nav"]
    if page == LABELS[0]:
        home()
        return
    try:
        importlib.import_module(PAGES[page][0]).render()
    except Exception as exc:  # noqa: BLE001  - never show raw tracebacks (could echo secrets)
        st.error(f"Something went wrong in this tool: {llm.scrub(exc)[:300]}")
        st.caption("Try again, or switch tool and come back. If it keeps happening, open an issue on the GitHub repo.")


main()
