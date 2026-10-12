
import streamlit as st
from pipeline import run_research_pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="ResearchAI | Intelligent Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================
DEFAULTS = {
    "last_successful_topic": None,
    "research_running": False,
    "research_results": None,
    "research_topic_completed": None,
    "agent_status": {
        "Search Agent": "pending",
        "Reader Agent": "pending",
        "Writer Agent": "pending",
        "Critic Agent": "pending",
    },
    "research_error": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, dict) else value


AGENTS = [
    {
        "name": "Search Agent",
        "number": "01",
        "icon": "🔎",
        "description": (
            "Searches the web for relevant information, "
            "source URLs, and snippets using Tavily."
        ),
    },
    {
        "name": "Reader Agent",
        "number": "02",
        "icon": "📖",
        "description": (
            "Visits the discovered URLs and extracts "
            "useful webpage content using BeautifulSoup."
        ),
    },
    {
        "name": "Writer Agent",
        "number": "03",
        "icon": "✍️",
        "description": (
            "Transforms the collected research into "
            "a structured, evidence-based report."
        ),
    },
    {
        "name": "Critic Agent",
        "number": "04",
        "icon": "🧠",
        "description": (
            "Evaluates report quality, evidence, citations, "
            "completeness, and reasoning."
        ),
    },
]


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --bg: #0b1020;
        --panel: #121a2c;
        --border: #27344d;
        --text: #edf2ff;
        --muted: #9baac4;
        --accent: #8b7cff;
        --cyan: #54d8e8;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 10% 0%,
                #24204a 0%,
                transparent 36%
            ),
            radial-gradient(
                ellipse at 95% 15%,
                #103345 0%,
                transparent 30%
            ),
            var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .hero {
        text-align: center;
        padding: 38px 20px 30px;
        animation: fadeUp 0.8s ease-out;
    }

    .hero-icon {
        display: inline-block;
        font-size: 42px;
        padding: 16px 23px;
        margin-bottom: 15px;
        border: 1px solid #6f63d9;
        border-radius: 24px;
        background: linear-gradient(135deg, #292552, #143244);
        box-shadow: 0 0 38px #7564ff25;
        animation: float 3s ease-in-out infinite;
    }

    .hero h1 {
        font-size: clamp(2.2rem, 5vw, 3.8rem);
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0;
        color: #f5f6ff;
    }

    .gradient-text {
        background: linear-gradient(90deg, #a89bff, #63dff1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 680px;
        margin: 15px auto 0;
        line-height: 1.8;
    }

    .eyebrow {
        display: inline-block;
        color: #b9b0ff;
        background: #8174ff15;
        border: 1px solid #8174ff50;
        padding: 7px 14px;
        border-radius: 100px;
        font-size: 0.77rem;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }

    .section-heading {
        color: #f1f4ff;
        font-size: 1.35rem;
        font-weight: 700;
        margin: 20px 0 8px;
    }

    .subheading {
        color: var(--muted);
        font-size: 0.92rem;
        margin-bottom: 20px;
    }

    .agent-card {
        background: linear-gradient(145deg, #151e32, #101728);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 21px;
        min-height: 190px;
        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;
        animation: fadeUp 0.8s ease-out;
    }

    .agent-card:hover {
        transform: translateY(-5px);
        border-color: #8174ff;
        box-shadow: 0 10px 30px #8174ff14;
    }

    .agent-icon {
        font-size: 26px;
        margin-bottom: 12px;
    }

    .agent-title {
        color: #f2f4ff;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 9px;
    }

    .agent-description {
        color: #9baac4;
        font-size: 0.85rem;
        line-height: 1.65;
    }

    .step-number {
        color: #a89bff;
        font-size: 0.72rem;
        letter-spacing: 1.5px;
        margin-bottom: 7px;
    }

    .panel {
        background: linear-gradient(145deg, #151e32, #101728);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 24px;
        margin: 14px 0;
    }

    div[data-testid="stTextInput"] input {
        background: #111a2c;
        color: #f4f6ff;
        border: 1px solid #34415c;
        border-radius: 12px;
        min-height: 53px;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #9184ff;
        box-shadow: 0 0 0 1px #9184ff;
    }

    .stButton > button,
    div[data-testid="stDownloadButton"] > button {
        width: 100%;
        min-height: 48px;
        border: 1px solid #9588ff;
        border-radius: 12px;
        color: white;
        font-weight: 700;
        background: linear-gradient(100deg, #7666ee, #536fe3);
        transition: all 0.25s ease;
    }

    .stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        border-color: #b5adff;
        box-shadow: 0 0 25px #8174ff35;
        transform: translateY(-2px);
        color: white;
    }

    .stButton > button:disabled {
        opacity: 0.42;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }

    div[data-testid="stTabs"] button {
        border-radius: 10px;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: #151e32;
        border: 1px solid var(--border);
        padding: 17px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9baac4;
    }

    div[data-testid="stMetricValue"] {
        color: #b5adff;
    }

    .status-card {
        background: linear-gradient(145deg, #151e32, #101728);
        border: 1px solid #27344d;
        border-radius: 13px;
        padding: 15px 18px;
        margin: 8px 0;
        transition: border-color 0.25s ease;
    }

    .status-running {
        border-color: #8b7cff;
        box-shadow: 0 0 18px #8174ff12;
    }

    .status-completed {
        border-color: #299b77;
    }

    .status-failed {
        border-color: #e05d70;
    }

    .status-name {
        font-weight: 700;
        color: #f2f4ff;
    }

    .status-detail {
        font-size: 0.83rem;
        color: #9baac4;
        margin-top: 4px;
    }

    .footer {
        text-align: center;
        color: #7887a3;
        font-size: 0.82rem;
        border-top: 1px solid #27344d;
        padding-top: 22px;
        margin-top: 60px;
        line-height: 1.9;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-8px);
        }
    }

    @media (max-width: 700px) {
        .hero {
            padding: 20px 5px;
        }

        .hero h1 {
            letter-spacing: -1px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🔬</div>
        <div class="eyebrow">✦ MULTI-AGENT AI RESEARCH SYSTEM</div>
        <h1>Research<span class="gradient-text">AI</span></h1>
        <p>
            Turn any research question into a structured report.
            Four specialized AI agents search the web, read sources,
            write findings, and evaluate the final report.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENT OVERVIEW
# ============================================================
st.markdown(
    """
    <div class="section-heading">Your research team</div>
    <div class="subheading">
        Four specialized agents working together in one research pipeline.
    </div>
    """,
    unsafe_allow_html=True,
)

columns = st.columns(4, gap="medium")

for column, agent in zip(columns, AGENTS):
    with column:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="step-number">AGENT {agent["number"]}</div>
                <div class="agent-icon">{agent["icon"]}</div>
                <div class="agent-title">{agent["name"]}</div>
                <div class="agent-description">
                    {agent["description"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# TOPIC INPUT AND DUPLICATE PREVENTION
# ============================================================
st.markdown("")
st.markdown(
    """
    <div class="section-heading">Start a new investigation</div>
    <div class="subheading">
        Enter a research topic. A successfully completed topic cannot
        be submitted again in this session unless you change it.
    </div>
    """,
    unsafe_allow_html=True,
)

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Impact of AI on healthcare in 2026",
    key="research_topic_input",
    help="Enter a specific topic for more useful research results.",
)

normalized_topic = topic.strip().casefold()
previous_topic = st.session_state.last_successful_topic

same_topic = bool(
    normalized_topic
    and previous_topic
    and normalized_topic == previous_topic
)

if not topic.strip():
    st.info("Enter a research topic to enable the Start AI Research button.")
elif same_topic:
    st.warning(
        "This topic has already been researched successfully. "
        "Change the topic to start a new investigation."
    )

start_disabled = (
    not topic.strip()
    or same_topic
    or st.session_state.research_running
)

start_research = st.button(
    "✦  Start AI Research",
    disabled=start_disabled,
    use_container_width=True,
    key="start_research_button",
)



# ============================================================
# RESEARCH EXECUTION AND LIVE PROGRESS
# ============================================================
if start_research:
    current_topic = topic.strip()

    # Extra protection against duplicate submissions
    if (
        st.session_state.last_successful_topic
        == current_topic.casefold()
    ):
        st.warning(
            "This topic has already been researched successfully. "
            "Please enter a different topic."
        )

    else:
        st.session_state.research_running = True
        st.session_state.research_error = None
        st.session_state.agent_status = {
            agent["name"]: "pending" for agent in AGENTS
        }

        st.markdown("---")
        st.markdown("### Research pipeline")
        st.caption(f"Topic: {current_topic}")

        overall_status = st.empty()
        progress_bar = st.progress(0)

        # Create exactly four placeholders ONCE.
        agent_placeholders = {}

        for agent in AGENTS:
            agent_placeholders[agent["name"]] = st.empty()

        def render_agent_status():
            statuses = st.session_state.agent_status

            completed_count = sum(
                value == "completed"
                for value in statuses.values()
            )

            progress_bar.progress(
                completed_count / len(AGENTS)
            )

            for agent in AGENTS:
                name = agent["name"]
                status = statuses[name]
                placeholder = agent_placeholders[name]

                if status == "completed":
                    icon = "✅"
                    label = "Completed"
                    css_class = "status-completed"
                    detail = "Task completed successfully."

                elif status == "running":
                    icon = "🔄"
                    label = "Running"
                    css_class = "status-running"
                    detail = "Currently processing this stage..."

                elif status == "failed":
                    icon = "❌"
                    label = "Failed"
                    css_class = "status-failed"
                    detail = "This stage encountered an error."

                else:
                    icon = "⏳"
                    label = "Pending"
                    css_class = ""
                    detail = "Waiting for the previous stage."

                # Replace only this agent's existing placeholder.
                with placeholder.container():
                    st.markdown(
                        f"""
                        <div class="status-card {css_class}">
                            <div class="status-name">
                                {icon} {name}
                                <span style="
                                    float:right;
                                    color:#b5adff;
                                    font-size:0.85rem;
                                ">{label}</span>
                            </div>
                            <div class="status-detail">
                                {detail}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Render the four pending agents once.

        
        def update_progress(agent_name, status):
            if agent_name not in st.session_state.agent_status:
                return

            st.session_state.agent_status[agent_name] = status

            if status == "running":
                overall_status.info(
                    f"Currently running: {agent_name}"
                )
            elif status == "completed":
                overall_status.success(
                    f"{agent_name} completed successfully."
                )
            elif status == "failed":
                overall_status.error(
                    f"{agent_name} failed."
                )

            render_agent_status()


        try:
            overall_status.info(
                "Starting the research pipeline..."
            )

            results = run_research_pipeline(
                current_topic,
                progress_callback=lambda name, status: (
                    update_progress(name, status)
                ),
            )

            st.session_state.research_results = results
            st.session_state.research_topic_completed = current_topic
            st.session_state.last_successful_topic = (
                current_topic.casefold()
            )

            overall_status.success(
                "All four agents completed successfully!"
            )

            progress_bar.progress(1.0)
            st.balloons()

        except Exception as error:
            st.session_state.research_error = str(error)

            # Mark the currently running agent as failed.
            for name, status in st.session_state.agent_status.items():
                if status == "running":
                    st.session_state.agent_status[name] = "failed"
                    break

            render_agent_status()

            overall_status.error("Research pipeline failed.")

            with st.expander("Technical error details"):
                st.code(str(error))

        finally:
            st.session_state.research_running = False



# ============================================================
# RESULTS WORKSPACE
# ============================================================
results = st.session_state.research_results

if results:
    st.markdown("---")
    st.markdown(
        """
        <div class="section-heading">Research workspace</div>
        <div class="subheading">
            Review the report, critic evaluation, search results,
            and content collected from webpages.
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_result = results.get(
        "search_result", "No search results returned."
    )
    reader_result = results.get(
        "reader_result", "No scraped content returned."
    )
    writer_result = results.get(
        "writer_result", "No research report returned."
    )
    critic_result = results.get(
        "critic_result", "No critic evaluation returned."
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Agents executed", "4")

    with metric2:
        st.metric("Research status", "Completed")

    with metric3:
        st.metric("Report generated", "Yes")

    tab_report, tab_critic, tab_search, tab_reader = st.tabs(
        [
            "📄 Final Report",
            "🧠 Critic Evaluation",
            "🔎 Search Results",
            "📚 Scraped Content",
        ]
    )

    with tab_report:
        st.markdown("### Research Report")

        if st.session_state.research_topic_completed:
            st.caption(
                f"Topic: {st.session_state.research_topic_completed}"
            )

        st.markdown(str(writer_result))

        st.download_button(
            label="⬇️ Download Research Report",
            data=str(writer_result),
            file_name="research_report.md",
            mime="text/markdown",
            key="download_report",
        )

    with tab_critic:
        st.markdown("### Critic Agent Evaluation")
        st.markdown(str(critic_result))

        st.download_button(
            label="⬇️ Download Critic Evaluation",
            data=str(critic_result),
            file_name="critic_evaluation.md",
            mime="text/markdown",
            key="download_critic",
        )

    with tab_search:
        st.markdown("### Search Agent Output")
        st.markdown(str(search_result))

        st.download_button(
            label="⬇️ Download Search Results",
            data=str(search_result),
            file_name="search_results.txt",
            mime="text/plain",
            key="download_search",
        )

    with tab_reader:
        st.markdown("### Reader Agent Output")
        st.markdown(str(reader_result))

        st.download_button(
            label="⬇️ Download Scraped Content",
            data=str(reader_result),
            file_name="scraped_content.txt",
            mime="text/plain",
            key="download_reader",
        )

    st.markdown(
        """
        <div class="panel">
            <div class="agent-title">✨ Research complete</div>
            <div class="agent-description">
                Review the report and critic evaluation before relying
                on the findings. AI-generated research can contain errors
                and should be checked against the original sources.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        ResearchAI · Powered by LangChain, Tavily & Mistral AI
        <br>
        Search intelligently. Read deeply. Write clearly. Evaluate critically.
    </div>
    """,
    unsafe_allow_html=True,
)
