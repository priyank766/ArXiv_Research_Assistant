import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.ui import Console
import arxiv 

from typing import List, Dict,AsyncGenerator
import asyncio

import streamlit as st

model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash", # Use a Gemini model name
    api_key=os.environ.get("GEMINI_API_KEY"), # Read from environment variable
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/", # Gemini's OpenAI-compatible endpoint
    
)

def search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search arXiv for papers matching the query.
    Each Element contains:
    - title
    - authors
    -published date (if available)
    -summary
    -pdf_url

    this function used by ResearcherAgent to search for relevant papers. by tool-use mechanism.
    
    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return.
        
    Returns:
        List[Dict]: A list of dictionaries containing paper details.
    """
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers : List[Dict] = []
    for result in client.results(search):
        papers.append(
            {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "published_date": result.published.strftime("%Y-%m-%d") if result.published else "N/A",
            "summary": result.summary,
            "pdf_url": result.pdf_url
          }
        )
        
    return papers

researcher_agent = AssistantAgent(
    name="ResearcherAgent",
    description="Create arxiv search and search for relevant research papers.then call the SummaryAgent to summarize the results",
    model_client=model_client, # Reverted to model_client
    tools=[search_arxiv],
    system_message=(
        "You are an expert researcher. think of best arxiv query for the given user topic.in json format\n"
        " When you receive a topic, search for relevant research papers on arXiv and return a JSON list of papers with the following fields:\n"
        "concise them into below fields:\n"
        "title:\n"
        "authors:\n"
        "-published date : (if available)\n"
        "-pdf_url: \n"
        "Ensure the list is concise and relevant to the topic."
    )
)

summary_agent = AssistantAgent(
    name="SummaryAgent",
    description="An agent that summarizes the content of a given document's content in a literature-review style and markdown format.",
    model_client=model_client, # Reverted to model_client
    system_message=(
         "You are an expert summary writer. When you receive the JSON list of papers, write a literature-review style report in Markdown format:\n"
         "1. Start with a 1-2 lines introduction of the topic.\n"
         "2. For each paper, create a bullet point with the following information. Follow this format exactly for each paper:\n"
            "   - **Title:** [Paper Title](PDF_URL)\n"
            "   - **Authors:** [The full list of authors, comma-separated]\n"
            "   - **Published Date:** YYYY-MM-DD\n"
            "   - **Summary:** Brief summary of the paper.\n"
         "3. After listing all papers, provide a final section with a single-sentence takeaway for each paper. Include the title (as a Markdown link) and the key contribution.\n"
      )
)

team = RoundRobinGroupChat(
    participants=[researcher_agent, summary_agent],
    termination_condition=TextMessageTermination("SummaryAgent"),
)


async def run_team(task: str):
    """
    Run the team to process the task and generate a summary.
    This function is called when the user clicks the "Get Summary" button.
    """
    result = await team.run(task=task)
    if result and result.messages:
        summary_message_content = None
        for message in reversed(result.messages):
            if hasattr(message, "source") and message.source == "SummaryAgent" and hasattr(message, "content"):
                summary_message_content = message.content
                break
        
        if summary_message_content:
            st.markdown(summary_message_content, unsafe_allow_html=True)
        else:
            st.warning("The team finished but no summary was generated. Please try again.")
    else:
        st.warning("Please Try again with a different topic or question.")


st.set_page_config(page_title="ArXiv Research Assistant", page_icon="📚", layout="wide")

# --- CUSTOM CSS (Dark Theme) ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-image: linear-gradient(to bottom, #0e1117, #1a1f2e);
        color: #fafafa;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #1a1f2e;
    }

    /* Title and Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa;
    }
    h1 { /* Gradient for the main title */
        background: -webkit-linear-gradient(45deg, #007bff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Buttons */
    .stButton>button {
        color: #ffffff;
        background-color: #007bff; /* Vibrant Blue */
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Darker Blue on hover */
    }

    /* Text input */
    .stTextInput>div>div>input {
        background-color: #1a1f2e;
        color: #fafafa;
        border-radius: 8px;
        border: 1px solid #007bff;
    }

    /* Containers and separators */
    .stContainer {
        border-radius: 8px;
    }
    hr {
        border-top: 1px solid #3c4354;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
with st.container():
    st.title("ArXiv Research Assistant")
    st.write("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password", placeholder="Your Gemini API Key")
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("1. Enter your Gemini API key.")
    st.markdown("2. Enter a research topic or question.")
    st.markdown("3. Click 'Find Research Paper'.")

# --- MAIN CONTENT ---

with st.container():
    st.subheader("Enter your research topic or question:")
    task = st.text_input("", placeholder="e.g., Latest advancements in quantum computing")

    if st.button("Find Research Paper"):
        if gemini_api_key and gemini_api_key.strip():
            os.environ["GEMINI_API_KEY"] = gemini_api_key.strip()
            model_client.api_key = gemini_api_key.strip() # Re-added this line

            if task and task.strip():
                with st.spinner("Searching for relevant papers..."):
                    try:
                        # --- RESULT DISPLAY ---
                        with st.container():
              
                            st.markdown("---")
                            st.subheader("Research Summary")
                            asyncio.run(run_team(task))
                            st.success("Task Completed Successfully!!!")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a research topic or question.")
        else:
            st.warning("Please enter your Gemini API Key to proceed.")
