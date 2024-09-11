import streamlit as st
import sys
# sys.path.append('C:/Users/Divyanshu/Desktop/Github/AIApp')
# from ./Pages import ChromaDBPage, Neo4jPage
from Pages.chromadb_page import ChromaDBPage
from Pages.neo4j_page import Neo4jPage
from Pages.llm_page import LlmPage

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )
# st.sidebar.success("Select a demo above.")
class MultiPageApp:
    def __init__(self):
        self.pages = {
            "ChromaDB Interaction": ChromaDBPage(),
            "Neo4j Interaction": Neo4jPage(),
            "LLM Interaction": LlmPage()
        }

    def run(self):
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", list(self.pages.keys()))
        self.pages[page].display()

if __name__ == "__main__":
    app = MultiPageApp()
    app.run()
