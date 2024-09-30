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
import uuid

from dotenv import load_dotenv, find_dotenv
from llama_index.llms.gemini import Gemini
from chromadb import HttpClient
from llama_index.core.llms import ChatMessage
from collections import Counter
from sentence_transformers import SentenceTransformer

class LlmPage:
    def __init__(self):
        load_dotenv(find_dotenv(), override=True)
        self.chroma_client = HttpClient(host='localhost', port=8000)
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection",metadata={"hnsw:space": "cosine"})
        self.index = self.load_data()
        self.initialize_session_state()
        self.chat_engine = self.create_chat_engine()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Pre-trained model for sentence embeddings

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.5
        if "top_p" not in st.session_state:
            st.session_state.top_p = 0.9
        if "top_k" not in st.session_state:
            st.session_state.top_k = 50
        if "faq_counter" not in st.session_state:
            st.session_state.faq_counter = Counter()

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
        # Query all documents with a count value (retrieve all entries first)
        all_prompts = self.collection.get(include=['documents', 'metadatas'])
        # Filter results to ensure the 'count' field exists and then sort them by count in descending order
        sorted_prompts = sorted(
            [doc for doc in all_prompts['metadatas'] if doc is not None and 'count' in doc],
            key=lambda x: x['count'],
            reverse=True
        )
        # Example prompts
        faq_prompts = [
            # "How create custom server in NodeJs?",
            # "How can I Implement React with Nodejs?",
            # "How can I implement LLMs in Nodejs?",
        ]
        dynamic_range= min(3,len(sorted_prompts))
        for i in range(dynamic_range):
            faq_prompts.append(sorted_prompts[i]['prompt'])

        button_cols = st.columns(3)

        button_pressed = ""
        for i in range(dynamic_range):
            if button_cols[i].button(faq_prompts[i]):
                button_pressed = faq_prompts[i]
        
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
        self.display_messages()
        self.frequently_asked_questions()

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
                self.update_faq_counter(prompt)
                
    def update_faq_counter(self, prompt):
        prompt_embedding = self.embedding_model.encode(prompt).tolist()
        results = self.collection.query(query_embeddings=[prompt_embedding], n_results=1, include=['documents', 'distances','metadatas'])
        
        if results['documents'][0] and results['distances'][0][0] < 0.45:  # Threshold for cosine similarity
            matched_question = results['documents'][0][0]
            st.session_state.faq_counter[matched_question] += 1
            current_count = results['metadatas'][0][0]['count']
            self.collection.update(results['ids'][0][0], metadatas=[{"count": current_count + 1}])
        else:
            new_id = str(uuid.uuid4())  # Generate a new UUID
            st.session_state.faq_counter[prompt] += 1
            self.collection.add(
                ids=[new_id],
                documents=[prompt],
                embeddings=[prompt_embedding],
                metadatas=[{'prompt':prompt,"count": 1}]
            )

    
    def reset_chat(self):
        if st.sidebar.button("Clear Chat",type="primary"):
            for key in st.session_state.keys():
                print("deleting...")
                print(st.session_state)
                del st.session_state[key]
            self.initialize_session_state()
            self.chat_engine = self.create_chat_engine()  # Reinitialize the LLM
        