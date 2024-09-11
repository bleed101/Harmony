# import streamlit as st
# import os
# from dotenv import load_dotenv, find_dotenv
# from llama_index.core.readers.file.base import SimpleDirectoryReader
# from llama_index.core import VectorStoreIndex
# from llama_index.llms.gemini import Gemini
# from chromadb import HttpClient

# class LlmPage:
#     def __init__(self):
#         load_dotenv(find_dotenv(), override=True)
#         self.chroma_client = HttpClient(host='localhost', port=8000)
#         self.collection = self.chroma_client.get_collection(name="my_collection")
#         self.index = self.load_data()
#         self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", verbose=True)
#         self.initialize_session_state()

#     def initialize_session_state(self):
#         if "messages" not in st.session_state:
#             st.session_state.messages = [
#                 "Ask me a question about Streamlit's open-source Python library!"
#             ]

#     @st.cache_resource(show_spinner=False)
#     def load_data(_self):
#         with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
#             reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
#             docs = reader.load_data()
#             llm_config = {
#                 "model": "gemini-pro",
#                 "temperature": 0.5,
#                 "system_prompt": "You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."
#             }
#             index = VectorStoreIndex.from_documents(docs, llm_config=llm_config)
#             return index

#     def display(self):
#         st.header("Talk to your Self-esteem 💬 📚")
#         self.handle_user_input()
#         self.display_messages()

#     def handle_user_input(self):
#         if prompt := st.chat_input("Your question"):
#             st.session_state.messages.append(prompt)
#             self.generate_response(prompt)

#     def display_messages(self):
#         for message in st.session_state.messages:
#             st.write(message)

#     def generate_response(self, prompt):
#         if st.session_state.messages[-1] != "assistant":
#             with st.spinner("Thinking..."):
#                 response = self.chat_engine.chat(prompt)
#                 st.write(response.response)
#                 st.session_state.messages.append(response.response)


# import streamlit as st
# import os
# from dotenv import load_dotenv, find_dotenv
# from llama_index.llms.gemini import Gemini
# from chromadb import HttpClient

# class LlmPage:
#     def __init__(self):
#         load_dotenv(find_dotenv(), override=True)
#         self.chroma_client = HttpClient(host='localhost', port=8000)
#         self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
#         self.index = self.load_data()
#         self.chat_engine = self.create_chat_engine()
#         self.initialize_session_state()

#     def initialize_session_state(self):
#         if "messages" not in st.session_state:
#             st.session_state.messages = [
#                 "Ask me a question about Streamlit's open-source Python library!"
#             ]

#     @st.cache_resource(show_spinner=False)
#     def load_data(_self):
#         with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
#             docs = _self.read_documents("./data")
#             for doc in docs:
#                 _self.collection.add(documents=[doc], ids=[doc['id']])
#             return _self.collection

#     def read_documents(self, input_dir):
#         # Implement your document reading logic here
#         # This should return a list of documents with 'id' and 'text'
#         return [{"id": "doc1", "text": "Document content here"}]

#     def create_chat_engine(self):
#         llm = Gemini(model="gemini-pro", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
#         return llm.as_chat_engine(chat_mode="condense_question", verbose=True)

#     def display(self):
#         st.header("Talk to your Self-esteem 💬 📚")
#         self.handle_user_input()
#         self.display_messages()

#     def handle_user_input(self):
#         if prompt := st.chat_input("Your question"):
#             st.session_state.messages.append(prompt)
#             self.generate_response(prompt)

#     def display_messages(self):
#         for message in st.session_state.messages:
#             st.write(message)

#     def generate_response(self, prompt):
#         if st.session_state.messages[-1] != "assistant":
#             with st.spinner("Thinking..."):
#                 response = self.chat_engine.chat(prompt)
#                 st.write(response.response)
#                 st.session_state.messages.append(response.response)


import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from llama_index.llms.gemini import Gemini
from chromadb import HttpClient

class LlmPage:
    def __init__(self):
        load_dotenv(find_dotenv(), override=True)
        self.chroma_client = HttpClient(host='localhost', port=8000)
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
        self.index = self.load_data()
        self.chat_engine = self.create_chat_engine()
        self.initialize_session_state()

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [
                "Ask me a question about Streamlit's open-source Python library!"
            ]

    @st.cache_data(show_spinner=False)
    def load_data(_self):
        with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
            docs = _self.read_documents("./data")
            for doc in docs:
                _self.collection.add(documents=[doc['text']], ids=[doc['id']])
            return _self.collection.get()

    def read_documents(self, input_dir):
        # Implement your document reading logic here
        # This should return a list of documents with 'id' and 'text'
        return [{"id": "doc1", "text": "Document content here"}]

    def create_chat_engine(self):
        llm = Gemini(model="models/gemini-pro", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
        return llm

    def display(self):
        st.header("Talk to your Self-esteem 💬 📚")
        self.handle_user_input()
        self.display_messages()

    def handle_user_input(self):
        if prompt := st.chat_input("Your question"):
            st.session_state.messages.append(prompt)
            self.generate_response(prompt)

    def display_messages(self):
        for message in st.session_state.messages:
            st.write(message)

    def generate_response(self, prompt):
        if st.session_state.messages[-1] != "assistant":
            with st.spinner("Thinking..."):
                relevant_docs = self.query_documents(prompt)
                messages = [{"role": "user", "content": prompt}]
                response = self.llm.chat(messages=messages, context=relevant_docs)
                st.write(response.response)
                st.session_state.messages.append(response.response)
                # print("hhhhhhhhhhhhhh"+prompt)
                # response = self.chat_engine.chat(prompt)
                # st.write(response.content)
                # # st.write(response.response)
                # # st.session_state.messages.append(response.response)