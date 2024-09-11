import streamlit as st
import chromadb

class ChromaDBPage:
    def __init__(self):
        self.chroma_client = chromadb.HttpClient(host='localhost', port=8000)
        self.collection = self.chroma_client.get_collection(name="my_collection")

    def display(self):
        st.title("ChromaDB Interaction App")

        # Add documents to the collection
        st.header("Add Documents")
        doc_text = st.text_area("Enter document text")
        doc_id = st.text_input("Enter document ID")
        if st.button("Add Document"):
            self.add_document(doc_text, doc_id)

        # Query the collection
        st.header("Query Documents")
        query_text = st.text_area("Enter query text")
        n_results = st.number_input("Number of results", min_value=1, max_value=10, value=2)
        if st.button("Query"):
            self.query_documents(query_text, n_results)

    def add_document(self, doc_text, doc_id):
        self.collection.add(documents=[doc_text], ids=[doc_id])
        st.success(f"Document added with ID: {doc_id}")

    def query_documents(self, query_text, n_results):
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        st.write("Results:", results)
