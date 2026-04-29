import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind - AI Research Agent",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Minimal CSS for theming ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #06060b;
    color: #e8e4dc;
    background-image:
        radial-gradient(ellipse 90% 60% at 15% -15%, rgba(139,92,246,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 70% 50% at 85% 110%, rgba(59,130,246,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 4rem; max-width: 1260px; }

/* ── Animated shimmer ── */
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), rgba(59,130,246,0.4), transparent);
    background-size: 200% 100%;
    animation: shimmer 4s linear infinite;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 0.6rem;
}
.hero h1 .grad {
    background: linear-gradient(135deg, #a78bfa 0%, #3b82f6 50%, #ec4899 100%);
    background-size: 200% 200%;
    animation: shimmer 5s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.95rem;
    font-weight: 300;
    color: #807870;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 12px !important;
    color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #a78bfa !important;
    font-weight: 500 !important;
}

/* ── Primary launch button ── */
div[data-testid="stButton"] > button[kind="secondary"]:not([data-chip]) {
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 60%, #6366f1 100%) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 24px rgba(139,92,246,0.3) !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:not([data-chip]):hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(139,92,246,0.45) !important;
}

/* ── Step card ── */
.step-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.6rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s ease;
}
.step-card.active {
    border-color: rgba(139,92,246,0.45);
    background: rgba(139,92,246,0.06);
    box-shadow: 0 0 20px rgba(139,92,246,0.08);
}
.step-card.done {
    border-color: rgba(52,211,153,0.3);
    background: rgba(52,211,153,0.04);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.04);
    transition: background 0.3s;
}
.step-card.active::before { background: linear-gradient(180deg, #a78bfa, #3b82f6); }
.step-card.done::before { background: #34d399; }
.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #8b5cf6;
    opacity: 0.6;
    min-width: 20px;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-desc {
    font-size: 0.7rem;
    color: #605850;
    margin-top: 0.1rem;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
}
.status-waiting { color: #444; }
.status-running { color: #a78bfa; background: rgba(139,92,246,0.08); }
.status-done    { color: #34d399; background: rgba(52,211,153,0.08); }

/* ── Report panel ── */
.report-panel {
    background: rgba(139,92,246,0.03);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 18px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
}
.report-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #8b5cf6, #3b82f6, #ec4899);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}

/* ── Feedback panel ── */
.feedback-panel {
    background: rgba(52,211,153,0.03);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 18px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
}
.feedback-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #34d399, #2dd4bf, #34d399);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}

.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
}
.panel-label.purple {
    color: #a78bfa;
    border-bottom: 1px solid rgba(139,92,246,0.12);
}
.panel-label.green {
    color: #34d399;
    border-bottom: 1px solid rgba(52,211,153,0.12);
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 1rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::before {
    content: '';
    width: 3px; height: 16px;
    border-radius: 2px;
    background: linear-gradient(180deg, #a78bfa, #3b82f6);
    flex-shrink: 0;
}

/* ── Expander ── */
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #807870 !important;
    letter-spacing: 0.1em !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(139,92,246,0.25) !important;
    color: #a78bfa !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: none !important;
}

/* ── Spinner ── */
.stSpinner > div { color: #a78bfa !important; }

/* ── Footer ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #383430;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.1em;
}

/* ── Hide form submit instructions ── */
.stForm [data-testid="stFormSubmitButton"] + div,
.stForm > div:last-child > small,
div[data-testid="InputInstructions"] { display: none !important; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.2), rgba(59,130,246,0.2), transparent);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render step card ─────────────────────────────────────────────────
def step_card(num, title, state, desc=""):
    status_map = {
        "waiting": ("",          "status-waiting"),
        "running": ("RUNNING",   "status-running"),
        "done":    ("DONE",      "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <div>
                <div class="step-num">{num}</div>
                <div class="step-title">{title}</div>
                {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
            </div>
            <span class="step-status {cls}">{label}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Helper: extract raw tool outputs ─────────────────────────────────────────
def extract_tool_output(result):
    """Extract raw tool message content to preserve URLs and raw data.
    Falls back to detecting JSON tool calls in text and executing them manually
    when the model outputs tool calls as text instead of actually calling them."""
    import json, re
    from tools import scrape_url as _scrape_url_tool

    # 1. Prefer actual tool messages (agent called the tool properly)
    tool_messages = [m.content for m in result['messages'] if m.type == 'tool']
    if tool_messages:
        return "\n\n".join(tool_messages)

    # 2. Fallback: detect JSON tool calls in the LLM's text response
    last_content = result['messages'][-1].content
    try:
        json_match = re.search(r'\[\s*\{.*?"name"\s*:\s*"scrape_url".*?\}\s*\]', last_content, re.DOTALL)
        if json_match:
            calls = json.loads(json_match.group())
            scraped_parts = []
            for call in calls:
                if call.get("name") == "scrape_url" and "url" in call.get("arguments", {}):
                    url = call["arguments"]["url"]
                    scraped = _scrape_url_tool.invoke(url)
                    scraped_parts.append(f"Scraped from {url}:\n{scraped}")
            if scraped_parts:
                return "\n\n".join(scraped_parts)
    except (json.JSONDecodeError, Exception):
        pass

    return last_content


# ── Session state init ───────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False

# Handle chip click: set topic BEFORE the text_input widget is created
if "chip_selected" not in st.session_state:
    st.session_state.chip_selected = None

if st.session_state.chip_selected:
    st.session_state.topic_input = st.session_state.chip_selected
    st.session_state.chip_selected = None
    st.session_state.results = {}
    st.session_state.running = True
    st.session_state.done = False
    st.session_state.current_step = "search"


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Research<span class="grad">Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Layout ───────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    with st.form("research_form", clear_on_submit=False):
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            label_visibility="visible",
        )
        run_btn = st.form_submit_button("Launch Research Pipeline", use_container_width=True)

    # Example chips
    st.caption("TRY")
    examples = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress", "Climate change effects"]
    chip_cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        with chip_cols[i]:
            if st.button(ex, key=f"chip_{i}", use_container_width=True):
                st.session_state.chip_selected = ex
                st.rerun()

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline Status</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def get_step_state(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  get_step_state("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  get_step_state("reader"), "Scrapes and extracts deep content")
    step_card("03", "Writer Chain",  get_step_state("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  get_step_state("critic"), "Reviews and scores the report")


# ── Run pipeline ─────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.current_step = "search"
        st.rerun()

if st.session_state.running and not st.session_state.done:
    topic_val = st.session_state.get("topic_input", "")
    results = dict(st.session_state.results)
    current = st.session_state.get("current_step", "search")

    if current == "search":
        with st.spinner("Search Agent is working..."):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [
                    ("system", "You are a web searcher. You MUST use the 'web_search' tool to look up the user's query. DO NOT answer from your own memory. DO NOT hallucinate search results. You MUST include the exact URLs and snippets returned by the tool in your final response."),
                    ("user", f"Find recent, reliable and detailed information about: {topic_val}")
                ]
            })
            results["search"] = extract_tool_output(sr)
            st.session_state.results = dict(results)
            st.session_state.current_step = "reader"
            st.rerun()

    elif current == "reader":
        with st.spinner("Scraping all sources for deeper content..."):
            import re
            from tools import scrape_url as _scrape_tool

            # Extract all URLs from search results
            urls = re.findall(r'https?://[^\s\n,]+', results.get("search", ""))
            # Remove duplicates while preserving order
            seen = set()
            unique_urls = []
            for u in urls:
                clean = u.rstrip('.,;:)]\'"')
                if clean not in seen:
                    seen.add(clean)
                    unique_urls.append(clean)

            scraped_parts = []
            for url in unique_urls[:7]:  # Scrape top 7 URLs
                try:
                    content = _scrape_tool.invoke(url)
                    if content and not content.startswith("Could not scrape"):
                        scraped_parts.append(f"--- Source: {url} ---\n{content}")
                except Exception:
                    pass

            if scraped_parts:
                results["reader"] = "\n\n".join(scraped_parts)
            else:
                results["reader"] = "No content could be scraped from the URLs."
            st.session_state.results = dict(results)
            st.session_state.current_step = "writer"
            st.rerun()

    elif current == "writer":
        with st.spinner("Writer is drafting the report..."):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = dict(results)
            st.session_state.current_step = "critic"
            st.rerun()

    elif current == "critic":
        with st.spinner("Critic is reviewing the report..."):
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
            st.session_state.results = dict(results)
            st.session_state.running = False
            st.session_state.done = True
            st.session_state.current_step = None
            st.rerun()


# ── Results display ──────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("Search Results (raw)", expanded=False):
            st.code(r["search"], language=None)

    if "reader" in r:
        with st.expander("Scraped Content (raw)", expanded=False):
            st.code(r["reader"], language=None)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label purple">Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind -- Powered by LangChain + Ollama -- Built with Streamlit
</div>
""", unsafe_allow_html=True)