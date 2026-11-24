import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

:root {
    --ink: #202124;
    --muted: #68717d;
    --line: #e5e9ef;
    --blue: #4285f4;
    --blue-dark: #2469d8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(ellipse 50% 42% at 62% 40%, rgba(183, 221, 255, 0.72), transparent 76%),
        radial-gradient(ellipse 36% 34% at 39% 45%, rgba(224, 240, 255, 0.72), transparent 80%),
        #f8f9fb;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 1120px;
    padding: 1.5rem 2rem 4rem;
}

.stMarkdown, [data-testid="stMarkdownContainer"] {
    color: var(--ink);
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #3f4650 !important;
    line-height: 1.75;
}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
[data-testid="stMarkdownContainer"] strong {
    color: var(--ink) !important;
}

.brand {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    color: #58616d;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.brand-mark {
    display: inline-grid;
    width: 1.7rem;
    height: 1.7rem;
    place-items: center;
    border-radius: 50%;
    background: #e4efff;
    color: var(--blue-dark);
    font-size: 1rem;
}
.home-hero {
    padding: clamp(5rem, 15vh, 9.5rem) 0 1.8rem;
    text-align: center;
}
.home-hero h1 {
    margin: 0;
    color: #292b2f;
    font-size: clamp(2rem, 4vw, 2.8rem);
    font-weight: 400;
    letter-spacing: -0.045em;
    line-height: 1.2;
}
.home-hero p {
    max-width: 570px;
    margin: 0.85rem auto 0;
    color: #68717d;
    font-size: 1rem;
    line-height: 1.65;
}

.st-key-composer {
    max-width: 780px;
    margin: 0 auto;
    padding: 0.65rem 0.8rem 0.65rem 1.1rem;
    border: 1px solid rgba(220, 226, 234, 0.9);
    border-radius: 999px;
    background: #fff;
    box-shadow: 0 5px 18px rgba(47, 70, 98, 0.12);
}
.st-key-composer [data-testid="stHorizontalBlock"] {
    align-items: center;
    gap: 0.5rem;
}
.st-key-composer [data-testid="stMarkdownContainer"] p {
    margin: 0;
    color: #5f6873 !important;
    font-size: 1.55rem;
    line-height: 1;
    text-align: center;
}
.stTextInput > label { display: none; }
.stTextInput > div > div {
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input {
    min-height: 3.3rem;
    padding: 0.65rem 0.25rem !important;
    border: 0 !important;
    outline: none !important;
    background: transparent !important;
    box-shadow: none !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input::placeholder {
    color: #7a818a !important;
    opacity: 1;
}
.stButton > button,
.stDownloadButton > button {
    min-height: 2.8rem;
    border: 1px solid #e1e6ee !important;
    border-radius: 999px !important;
    background: #fff !important;
    color: #30343a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: background 0.18s, border-color 0.18s, transform 0.18s !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #c9d8ee !important;
    background: #f5f9ff !important;
    transform: translateY(-1px);
}
.st-key-composer .stButton > button {
    min-height: 2.8rem;
    padding: 0 1.25rem !important;
    border-color: var(--blue) !important;
    background: var(--blue) !important;
    color: #fff !important;
    font-weight: 600 !important;
}
.st-key-composer .stButton > button:hover {
    border-color: var(--blue-dark) !important;
    background: var(--blue-dark) !important;
}

.suggestion-heading {
    margin: 1.8rem 0 0.55rem;
    color: #737b85;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-align: center;
    text-transform: uppercase;
}
.st-key-suggestions .stButton > button {
    min-height: 3rem;
    padding: 0.55rem 0.85rem !important;
    border-color: rgba(225, 231, 239, 0.9) !important;
    background: rgba(255, 255, 255, 0.66) !important;
    color: #404852 !important;
    text-align: left;
}
.st-key-suggestions .stButton > button:hover {
    background: #fff !important;
}

.pipeline-heading {
    margin: 2.7rem 0 0.9rem;
    color: #7b838d;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-align: center;
    text-transform: uppercase;
}
.step-card {
    min-height: 5.3rem;
    padding: 0.85rem 0.9rem;
    border: 1px solid rgba(226, 231, 238, 0.9);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.68);
    transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
}
.step-card.active {
    border-color: #9dc2fa;
    background: #fff;
    box-shadow: 0 3px 12px rgba(66, 133, 244, 0.1);
}
.step-card.done {
    border-color: #b8dfc7;
    background: #f7fcf8;
}
.step-header {
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.step-num {
    display: inline-grid;
    width: 1.4rem;
    height: 1.4rem;
    place-items: center;
    border-radius: 50%;
    background: #eef1f5;
    color: #737d89;
    font-size: 0.68rem;
    font-weight: 600;
}
.step-card.active .step-num {
    background: #e7f0ff;
    color: var(--blue-dark);
}
.step-card.done .step-num {
    background: #e5f5e9;
    color: #27834a;
}
.step-title {
    color: #353b43;
    font-size: 0.83rem;
    font-weight: 600;
}
.step-status {
    margin: 0.45rem 0 0 1.95rem;
    color: #7a838e;
    font-size: 0.72rem;
}
.step-description {
    margin: 0.35rem 0 0 1.95rem;
    color: #79828d;
    font-size: 0.72rem;
    line-height: 1.4;
}
.status-running { color: var(--blue-dark); }
.status-done { color: #27834a; }

.results-heading {
    margin: 3.5rem 0 0.5rem;
    color: #292d33;
    font-size: 1.65rem;
    font-weight: 600;
    letter-spacing: -0.03em;
}
.st-key-report_panel,
.st-key-feedback_panel {
    margin-top: 1rem;
    padding: 1.7rem 2rem;
    border: 1px solid #e5e9ef;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.84);
    box-shadow: 0 3px 14px rgba(47, 70, 98, 0.045);
}
.st-key-feedback_panel {
    background: rgba(255, 255, 255, 0.66);
}
.panel-label {
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #edf0f4;
    color: #68717d;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.st-key-report_panel [data-testid="stMarkdownContainer"] p,
.st-key-report_panel [data-testid="stMarkdownContainer"] li,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] p,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] li {
    color: #3f4650 !important;
}
.st-key-report_panel [data-testid="stMarkdownContainer"] h1,
.st-key-report_panel [data-testid="stMarkdownContainer"] h2,
.st-key-report_panel [data-testid="stMarkdownContainer"] h3,
.st-key-report_panel [data-testid="stMarkdownContainer"] h4,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h1,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h2,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h3,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h4 {
    color: #252a31 !important;
}

.result-panel {
    padding: 1.2rem 1.4rem;
    border: 1px solid #e5e9ef;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.72);
}
.result-panel-title {
    margin-bottom: 0.8rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #edf0f4;
    color: #68717d;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.result-content {
    color: #3f4650;
    font-size: 0.9rem;
    line-height: 1.75;
    white-space: pre-wrap;
}
details summary {
    color: #4d5661 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}
.stSpinner > div { color: var(--blue) !important; }
.notice {
    margin-top: 3rem;
    color: #8a929c;
    font-size: 0.75rem;
    text-align: center;
}

@media (max-width: 700px) {
    .block-container { padding: 1rem 1rem 3rem; }
    .home-hero { padding-top: 5.5rem; }
    .st-key-composer { padding-left: 0.65rem; padding-right: 0.55rem; }
    .st-key-report_panel, .st-key-feedback_panel { padding: 1.2rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("Up next", "status-waiting"),
        "running": ("In progress", "status-running"),
        "done":    ("Complete", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
        </div>
        <div class="step-status {cls}">{label}</div>
        {"<div class='step-description'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Prompt home ───────────────────────────────────────────────────────────────
st.markdown(
    '<div class="brand"><span class="brand-mark">✳</span> ResearchMind</div>',
    unsafe_allow_html=True,
)
st.markdown("""
<div class="home-hero">
    <h1>Where should we start?</h1>
    <p>Choose a topic and let our research agents search, read, and shape it into a clear report.</p>
</div>
""", unsafe_allow_html=True)

with st.container(key="composer"):
    col_icon, col_topic, col_submit = st.columns([0.07, 0.73, 0.20], vertical_alignment="center")
    with col_icon:
        st.markdown('<p class="composer-plus">＋</p>', unsafe_allow_html=True)
    with col_topic:
        topic = st.text_input(
            "Research topic",
            placeholder="Ask ResearchMind anything",
            key="topic_input",
            label_visibility="collapsed",
        )
    with col_submit:
        run_btn = st.button("Research", use_container_width=True)

examples = [
    "AI agents: latest developments",
    "CRISPR: recent discoveries",
    "Fusion energy: key milestones",
]

def choose_example(example: str):
    st.session_state.topic_input = example

st.markdown('<div class="suggestion-heading">Try a research prompt</div>', unsafe_allow_html=True)
with st.container(key="suggestions"):
    suggestion_cols = st.columns(3)
    for col, example in zip(suggestion_cols, examples):
        with col:
            st.button(
                example,
                key=f"suggestion_{examples.index(example)}",
                use_container_width=True,
                on_click=choose_example,
                args=(example,),
            )

results = st.session_state.results
pipeline_steps = [
    ("search", "Search", "Find reliable sources"),
    ("reader", "Read", "Explore key material"),
    ("writer", "Write", "Draft the report"),
    ("critic", "Review", "Check report quality"),
]
active_step = next((key for key, _, _ in pipeline_steps if key not in results), None)
st.markdown('<div class="pipeline-heading">How the research comes together</div>', unsafe_allow_html=True)
with st.container(key="pipeline"):
    step_cols = st.columns(4)
    for col, (key, title, description) in zip(step_cols, pipeline_steps):
        state = "done" if key in results else (
            "running" if st.session_state.running and key == active_step else "waiting"
        )
        with col:
            step_card(key[:2].upper(), title, state, description)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="results-heading">Research report</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        with st.container(key="report_panel"):
            st.markdown(
                '<div class="panel-label orange">📝 Final Research Report</div>',
                unsafe_allow_html=True,
            )
            st.markdown(r["writer"])

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        with st.container(key="feedback_panel"):
            st.markdown(
                '<div class="panel-label green">🧐 Critic Feedback</div>',
                unsafe_allow_html=True,
            )
            st.markdown(r["critic"])


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)