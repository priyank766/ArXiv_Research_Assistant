# ArXiv Research Assistant

## Project Overview

The ArXiv Research Assistant is a Streamlit-based application designed to streamline the process of finding and summarizing academic papers from arXiv. Leveraging the power of large language models and the arXiv API, this tool allows users to quickly search for relevant research papers based on a given topic and receive a concise, literature-review style summary of the findings.

This application is built to assist researchers, students, and anyone interested in staying updated with the latest academic publications without having to manually sift through numerous papers.

## Features

- **Intelligent ArXiv Search:** Utilizes the arXiv API to search for research papers based on user-provided topics or questions.
- **Automated Summarization:** Employs an AI agent (powered by Google Gemini) to generate literature-review style summaries of the retrieved papers.
- **Detailed Paper Information:** Displays key details for each paper, including:
  - Title (with a direct link to the PDF)
  - Full list of authors
  - Publication date
  - Concise summary
- **Interactive User Interface:** A user-friendly web interface built with Streamlit for easy interaction.
- **API Key Integration:** Securely handles Gemini API key input for model interaction.
- **Text-to-Speech (Planned/Under Development):** Future capability to read out the generated summaries for an enhanced user experience.

## Technologies Used

- **Python:** The core programming language for the application.
- **Streamlit:** For building the interactive web user interface.
- **Autogen:** An open-source framework for building multi-agent conversation systems, used here to orchestrate the research and summarization agents.
- **`arxiv` Python Library:** For programmatic access to the arXiv API.
- **Google Gemini API:** Powers the intelligent agents for search query formulation and summarization.

## Setup and Installation

Follow these steps to get the ArXiv Research Assistant up and running on your local machine.

### Prerequisites

- Python 3.8+
- A Google Gemini API Key (you can obtain one from [Google AI Studio](https://aistudio.google.com/))

### Steps

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/arxiv_finder.git
    cd arxiv_finder
    ```

    (Note: Replace `https://github.com/your-username/arxiv_finder.git` with the actual repository URL if different.)

2.  **Create a Virtual Environment (Recommended):**
    ```
    uv init
    uv venv
    ```
3.  **Activate the Virtual Environment:**

    - **On Windows:**
      ```bash
      .venv\Scripts\activate
      ```
    - **On macOS/Linux:**
      ```bash
      source .venv/bin/activate
      ```

4.  **Install Dependencies:**

    ```bash
    uv add -r requirements.txt
    ```

    If `requirements.txt` is not present, you can generate it using `pip freeze > requirements.txt` after installing the necessary libraries (streamlit, autogen, arxiv, google-generativeai).

5.  **Set Your Gemini API Key:**
    The application will prompt you to enter your Gemini API key directly in the Streamlit interface. Alternatively, you can set it as an environment variable named `GEMINI_API_KEY`.

    - **For temporary session (replace `YOUR_API_KEY`):**
      - **On Windows (Command Prompt):**
        ```bash
        set GEMINI_API_KEY=YOUR_API_KEY
        ```
      - **On Windows (PowerShell):**
        ```powershell
        $env:GEMINI_API_KEY="YOUR_API_KEY"
        ```
      - **On macOS/Linux:**
        ```bash
        export GEMINI_API_KEY="YOUR_API_KEY"
        ```
    - **For permanent setup:** Add the `export GEMINI_API_KEY="YOUR_API_KEY"` line to your shell's profile file (e.g., `.bashrc`, `.zshrc`, `.profile`).

## Usage

1.  **Run the Streamlit Application:**

    ```bash
    streamlit run main.py
    ```

2.  **Access the Application:**
    Your web browser will automatically open to the Streamlit application (usually at `http://localhost:8501`).

3.  **Enter API Key:**
    In the sidebar, enter your Google Gemini API Key.

4.  **Enter Research Topic:**
    In the main content area, type your research topic or question (e.g., "Latest advancements in quantum computing").

5.  **Find Research Papers:**
    Click the "Find Research Paper" button or press `Enter` in the text input field. The application will then search arXiv and display the summarized results.

## Project Structure

```
arxiv_finder/
├── .env                  # Environment variables (e.g., API keys)
├── main.py               # Main Streamlit application logic
├── pyproject.toml        # Project metadata (if using Poetry/Rye)
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── uv.lock               # Dependency lock file (if using uv)
└── .venv/                # Python virtual environment
    └── ...
```

## Summary

The ArXiv Research Assistant simplifies academic research by automating paper discovery and summarization, making it easier for users to stay informed about new developments in their fields.
