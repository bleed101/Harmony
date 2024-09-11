import streamlit as st
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import atexit

class Neo4jPage:
    def __init__(self):
        load_dotenv()
        self.NEO4J_URI = os.getenv("NEO4J_URI")
        self.NEO4J_USER = os.getenv("NEO4J_USER")
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(self.NEO4J_URI, auth=(self.NEO4J_USER, self.NEO4J_PASSWORD))
        atexit.register(self.close_driver)

    def display(self):
        st.title("Neo4j with Streamlit")

        query = st.text_area("Enter your Cypher query here")
        if st.button("Run Query"):
            results = self.run_query(query)
            st.write(results)

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    def close_driver(self):
        self.driver.close()
