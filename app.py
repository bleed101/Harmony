import streamlit as st
from components.chromadb_page import ChromaDBPage
from components.neo4j_page import Neo4jPage
from components.llm_page import LlmPage

class MultiPageApp:
    def __init__(self):
        self.pages = {
            "ChromaDB Interaction": ChromaDBPage(),
            "Neo4j Interaction": Neo4jPage(),
            "Harmony": LlmPage()
        }

    def run(self):
        with st.sidebar.title("Navigation"):
            page = st.sidebar.selectbox("", list(self.pages.keys()))
        self.pages[page].display()

if __name__ == "__main__":
    app = MultiPageApp()
    app.run()
