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
from llama_index.core.llms import ChatMessage

class LlmPage:
    def __init__(self):
        load_dotenv(find_dotenv(), override=True)
        self.chroma_client = HttpClient(host='localhost', port=8000)
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
        self.index = self.load_data()
        self.initialize_session_state()
        self.chat_engine = self.create_chat_engine()

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.5
        if "top_p" not in st.session_state:
            st.session_state.top_p = 0.9
        if "top_k" not in st.session_state:
            st.session_state.top_k = 50

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
    
    def frequently_asked_questions(self):
        # Example prompts
        example_prompts = [
            "How create custom server in NodeJs?",
            "How can I Implement React with Nodejs?",
            "How can I implement LLMs in Nodejs?",
        ]

        button_cols = st.columns(3)

        button_pressed = ""

        if button_cols[0].button(example_prompts[0]):
            button_pressed = example_prompts[0]
        elif button_cols[1].button(example_prompts[1]):
            button_pressed = example_prompts[1]
        elif button_cols[2].button(example_prompts[2]):
            button_pressed = example_prompts[2]
        
        if button_pressed:
            st.session_state.messages.append({"role": "user", "content":button_pressed})
            self.generate_response(button_pressed)        
    
    def create_chat_engine(self):
        llm = Gemini(model="models/gemini-pro",
            temperature=st.session_state.temperature,
            top_p=st.session_state.top_p,
            top_k=st.session_state.top_k, 
            system_prompt="You are an expert on the Streamlit Python library and your job is \
            to answer technical questions. Assume that all questions are related to the Streamlit\
            Python library. Keep your answers technical and based on facts – do not hallucinate features.")
        return llm

    def display(self):
        st.header("Talk to your Self-esteem 💬 📚")
        self.handle_user_input()
        self.reset_chat()
        self.frequently_asked_questions()
        self.display_messages()

    def handle_user_input(self):
        st.divider()
        hyper_parameters = st.columns(3)
        st.session_state.temperature = float(hyper_parameters[0].text_input("Temperature (0.0-1.0)", value=st.session_state.get("temperature", 0.5)))
        st.session_state.top_p = float(hyper_parameters[1].text_input("Top-p (0.0-1.0)", value=st.session_state.get("top_p", 0.9)))
        st.session_state.top_k = int(hyper_parameters[2].text_input("Top-k (0-100)", value=st.session_state.get("top_k", 50)))
        if prompt := st.chat_input("Your question"):
            st.session_state.messages.append({"role": "user", "content":prompt})
            self.generate_response(prompt)

    def display_messages(self):
        print(st.session_state.messages)
        for message in st.session_state.messages:
            st.chat_message(message["role"]).write(message["content"])

    def generate_response(self, prompt):
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.spinner("Thinking..."):
                messages = [ChatMessage(role="user", content=prompt)]
                response = self.chat_engine.stream_chat(messages=messages)
                response_content = ""
                for r in response:
                    response_content += r.delta
                st.session_state.messages.append({"role": "assistant", "content": response_content})
    
    def reset_chat(self):
        if st.sidebar.button("Clear Chat",type="primary"):
            for key in st.session_state.keys():
                print("deleting...")
                print(st.session_state)
                del st.session_state[key]
            self.initialize_session_state()
            self.chat_engine = self.create_chat_engine()  # Reinitialize the LLM
        