import time

import streamlit as st
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from utils import Answer, llm, load_id
from tools.student_tools import student_tools
from tools.learning_tools import learning_tools
from tools.rag import sumarize_retrieved_documents
from tools.instructor_tools import extract_instructor_info
from history_data.history import save_history, get_summary_history, retrieve_history_db

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Aymen English", page_icon="💬", layout="centered")

# ----------------------------------------------------------------------------
# One-time setup, cached across reruns (Streamlit reruns the whole script
# on every interaction, so anything expensive/stateful needs caching or
# session_state so it isn't rebuilt on every message).
# ----------------------------------------------------------------------------
tools = [*student_tools, *learning_tools, extract_instructor_info, sumarize_retrieved_documents]


@st.cache_resource
def build_agents():
    """Build both agents once per server process."""
    history_system_prompt = open("history_system.txt", "r").read()
    system_prompt = open("system_prompt.txt", "r").read()

    history_agent = create_agent(
        llm,
        tools=[get_summary_history, retrieve_history_db],
        system_prompt=history_system_prompt,
    )

    memory = InMemorySaver()
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=system_prompt,
        response_format=Answer,
        checkpointer=memory,
        name="Aymen_English",
    )
    return history_agent, agent


history_agent, agent = build_agents()

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = load_id()

if "chat_history" not in st.session_state:
    # what gets rendered in the chat window
    st.session_state.chat_history = []

config = {"configurable": {"thread_id": st.session_state.user_id}}

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Aymen English")
    st.caption(f"User ID: `{st.session_state.user_id}`")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

st.title("💬 Aymen English")

# ----------------------------------------------------------------------------
# Render existing chat history
# ----------------------------------------------------------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------------------------------------------------------
# Handle new input
# ----------------------------------------------------------------------------
user_input = st.chat_input("Enter your question...")

if user_input:
    # show user message immediately
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            start = time.time()
            with st.spinner("Thinking..."):
                # 1) pull relevant context from prior conversation history
                history_context = history_agent.invoke(
                    {"messages": [{"role": "user", "content": user_input}]}
                )["messages"][-1].content

                # 2) run the main agent with that context injected
                answer = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "system",
                                "content": f"Relevant conversation context:\n{history_context}",
                            },
                            {"role": "user", "content": user_input},
                        ]
                    },
                    config=config,
                )
            elapsed = time.time() - start

            structured = answer["structured_response"]
            res = structured.answer
            save = structured.add_to_db

            placeholder.markdown(res)
            st.caption(f"⏱️ {elapsed:.1f}s")

            # 3) persist to your history store, same as the original script
            save_history(user_input, res, save)

            st.session_state.chat_history.append({"role": "assistant", "content": res})

        except Exception as ex:
            error_msg = f"⚠️ Error in generating response , try again later"
            placeholder.markdown(error_msg)
