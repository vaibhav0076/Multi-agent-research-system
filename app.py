import io
from contextlib import redirect_stdout
from datetime import datetime

import streamlit as st

from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)


# ---------- Custom stdout stream that updates a Streamlit placeholder live ----------
class StreamlitLogStream(io.TextIOBase):
    """Captures print() output from the pipeline and streams it into a
    Streamlit placeholder so the UI shows live agent progress."""

    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.buffer = ""

    def write(self, s):
        if s:
            self.buffer += s
            self.placeholder.code(self.buffer, language="text")
        return len(s)

    def flush(self):
        pass


def get_text(value):
    """Chains/LLM calls sometimes return AIMessage objects instead of str."""
    return getattr(value, "content", value)


# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔎 Research Pipeline")
    st.markdown(
        "This app runs a **4-agent research pipeline**:\n\n"
        "1. **Search Agent** — finds recent, relevant sources\n"
        "2. **Reader Agent** — scrapes the best source for detail\n"
        "3. **Writer Agent** — drafts a report\n"
        "4. **Critic Agent** — reviews and gives feedback\n"
    )
    st.divider()
    show_logs = st.checkbox("Show live agent logs", value=True)
    st.caption("Logs are captured from the pipeline's console output.")

st.title("Multi-Agent Research Assistant")
st.caption("Enter a topic and let the search, reader, writer, and critic agents do the work.")

if "history" not in st.session_state:
    st.session_state.history = []  # list of {topic, timestamp, result}

topic = st.text_input("Research topic", placeholder="e.g. Impact of AI on renewable energy grids")
run_clicked = st.button("Run Research", type="primary")

if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        log_placeholder = None
        if show_logs:
            with st.expander("Live agent logs", expanded=True):
                log_placeholder = st.empty()

        with st.status("Running research pipeline...", expanded=True) as status:
            try:
                if show_logs and log_placeholder is not None:
                    stream = StreamlitLogStream(log_placeholder)
                    with redirect_stdout(stream):
                        result = run_research_pipeline(topic)
                else:
                    buf = io.StringIO()
                    with redirect_stdout(buf):
                        result = run_research_pipeline(topic)

                status.update(label="Pipeline complete ✅", state="complete", expanded=False)
                st.session_state.history.append(
                    {
                        "topic": topic,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": result,
                    }
                )
            except Exception as e:
                status.update(label="Pipeline failed ❌", state="error", expanded=True)
                st.error(f"Something went wrong while running the pipeline:\n\n{e}")
                st.stop()

# ---------- Display results ----------
if st.session_state.history:
    if len(st.session_state.history) > 1:
        labels = [f"{h['topic']}  ·  {h['timestamp']}" for h in st.session_state.history]
        selected_idx = st.selectbox(
            "View run",
            options=range(len(labels)),
            format_func=lambda i: labels[i],
            index=len(labels) - 1,
        )
    else:
        selected_idx = 0

    run = st.session_state.history[selected_idx]
    result = run["result"]

    st.subheader(f"Results for: {run['topic']}")
    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        report_text = get_text(result.get("report", ""))
        st.markdown(report_text)
        st.download_button(
            "Download report (.md)",
            data=str(report_text),
            file_name=f"{run['topic'].replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(get_text(result.get("feedback", "")))

    with tab_search:
        st.text(result.get("search_results", ""))

    with tab_scraped:
        st.text(result.get("scraped_content", ""))
else:
    st.info("Enter a topic above and click **Run Research** to get started.")