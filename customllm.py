# from typing import Any
# from llama_index.core.base.llms.types import (CompletionResponse, 
#                                               CompletionResponseGen, 
#                                               LLMMetadata)
# from llama_index.core.llms import CustomLLM
# from llama_index.core.llms.callbacks import llm_completion_callback
# from llama_index.llms.gemini import Gemini
# from llama_index.core import (ServiceContext, SimpleDirectoryReader, SummaryIndex)
# from dotenv import load_dotenv
# import os
# load_dotenv()

# # Initialize the Gemini model
# gemini = Gemini( api_key=os.getenv("GEMINI_API_KEY"))

# context_window = 2048
# num_output = 256

# model="models/gemini-pro",
# class CustomGemini(CustomLLM):
#     # def __init__(self):
#     #     self.gemini = Gemini(
#     #         model="models/gemini-pro",
#     #         temperature=0.5,
#     #         top_p=50,
#     #         top_k=0.2, 
#     #         system_prompt="You are an expert on the Streamlit Python library and your job is \
#     #         to answer technical questions. Assume that all questions are related to the Streamlit\
#     #         Python library. Keep your answers technical and based on facts – do not hallucinate features."
#     #     )

#     @property
#     def metadata(self) -> LLMMetadata:
#         """Get LLM metadata."""
#         return LLMMetadata(
#             context_window=context_window,
#             num_output=num_output,
#             model_name=model
#         )

#     @llm_completion_callback()
#     def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
#         response = gemini.complete(prompt, **kwargs)
#         return CompletionResponse(text=response.text)

#     @llm_completion_callback()
#     def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
#         response = gemini.complete(prompt, **kwargs)
#         words = response.text.split()
#         partial_response = ""
#         for word in words:
#             partial_response += word + " "
#             yield CompletionResponse(text=partial_response, delta=word)
            
# # Define our custom Gemini model
# ddgemini = CustomGemini()

# print(ddgemini.complete("hello",temp=2))
# # Create a service context with the custom Gemini model
# service_context = ServiceContext.from_defaults(
#     llm=gemini,
#     context_window=context_window,
#     num_output=num_output,
# )

# # Load your data
# documents = SimpleDirectoryReader("./data").load_data()

# # Create an index from the documents
# index = SummaryIndex.from_documents(documents, service_context=service_context)

# # Query the index and print the response
# query_engine = index.as_query_engine()
# response = query_engine.query("What did the author do after his time at Y Combinator?")
# print(response)


# ------------------------------------------------------------------------------------------------------

# import os
# from dotenv import load_dotenv
# from typing import Any, Dict, Optional
# import requests
# from llama_index.core.base.llms.types import CompletionResponse, CompletionResponseGen, LLMMetadata
# from llama_index.core.llms import CustomLLM
# from llama_index.core.llms.callbacks import llm_completion_callback
# from pydantic import BaseModel, Field
# from llama_index.core.base.llms.types import ChatMessage, MessageRole

# # Load environment variables
# load_dotenv()

# class CustomGeminiAPI(CustomLLM, BaseModel):
#     api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_API_KEY"))
#     api_url: str = Field(default_factory=lambda: f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={os.getenv('GOOGLE_API_KEY')}")
#     headers: dict = Field(default_factory=lambda: {"Content-Type": "application/json"})
#     system_prompt: str = Field(default="You are a helpful AI assistant.")
#     max_tokens: int = 2048  # Default max tokens for output

#     def __init__(self, **data):
#         super().__init__(**data)
#         print(f"API Key: {self.api_key[:5]}..." if self.api_key else "API Key not found")
#         print(f"API URL: {self.api_url}")
#         print(f"System Prompt: {self.system_prompt}")
#         print(f"Max Tokens: {self.max_tokens}")

#     @property
#     def metadata(self) -> LLMMetadata:
#         return LLMMetadata(
#             context_window=8192,  # Gemini 1.5 Pro context window
#             num_output=self.max_tokens,
#             model_name="models/gemini-1.5-pro"
#         )

#     def _make_request(self, prompt: str, **kwargs: Any) -> Dict:
#         # Include system prompt in the request
#         full_prompt = f"{self.system_prompt}\n\nHuman: {prompt}\n\nAssistant:"
#         data = {
#             "contents": [{"parts": [{"text": full_prompt}]}],
#             "generationConfig": {
#                 "temperature": kwargs.get("temperature", 0.7),
#                 "topP": kwargs.get("top_p", 1.0),
#                 "topK": kwargs.get("top_k", 40),
#                 "maxOutputTokens": min(kwargs.get("max_tokens", self.max_tokens), self.max_tokens)
#             }
#         }
#         try:
#             response = requests.post(self.api_url, headers=self.headers, json=data)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"Error making request: {e}")
#             print(f"Response content: {response.content}")
#             raise

#     @llm_completion_callback()
#     def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
#         try:
#             response_json = self._make_request(prompt, **kwargs)
#             text = response_json['candidates'][0]['content']['parts'][0]['text']
#             return CompletionResponse(text=text)
#         except KeyError as e:
#             print(f"Error parsing response: {e}")
#             print(f"Response JSON: {response_json}")
#             raise

#     @llm_completion_callback()
#     def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
#         response_json = self._make_request(prompt, **kwargs)
#         text = response_json['candidates'][0]['content']['parts'][0]['text']
#         words = text.split()
#         partial_response = ""
#         for word in words:
#             partial_response += word + " "
#             yield CompletionResponse(text=partial_response, delta=word)

#     def chat(self, messages: list[ChatMessage], **kwargs: Any) -> CompletionResponse:
#         # Convert messages to Gemini format, including system prompt
#         gemini_messages = [{"role": "system", "parts": [{"text": self.system_prompt}]}]
#         for message in messages:
#             role = "model" if message.role == MessageRole.ASSISTANT else "user"
#             gemini_messages.append({"role": role, "parts": [{"text": message.content}]})
        
#         data = {
#             "contents": gemini_messages,
#             "generationConfig": {
#                 "temperature": kwargs.get("temperature", 0.7),
#                 "topP": kwargs.get("top_p", 1.0),
#                 "topK": kwargs.get("top_k", 40),
#                 "maxOutputTokens": min(kwargs.get("max_tokens", self.max_tokens), self.max_tokens)
#             }
#         }
        
#         try:
#             response = requests.post(self.api_url, headers=self.headers, json=data)
#             response.raise_for_status()
#             response_json = response.json()
#             text = response_json['candidates'][0]['content']['parts'][0]['text']
#             return CompletionResponse(text=text)
#         except requests.exceptions.RequestException as e:
#             print(f"Error making request: {e}")
#             print(f"Response content: {response.content}")
#             raise
#         except KeyError as e:
#             print(f"Error parsing response: {e}")
#             print(f"Response JSON: {response_json}")
#             raise

# # Example usage
# def main():
#     # Initialize the custom Gemini API with a specific system prompt
#     gemini_api = CustomGeminiAPI(
#         system_prompt="You are a knowledgeable AI assistant specialized in explaining complex topics in simple terms.",
#         max_tokens=1024
#     )

#     # Use the LLM for completion
#     prompt = "Explain the concept of quantum computing."
#     response = gemini_api.complete(prompt, max_tokens=200)
#     print(f"Completion response: {response.text}")

#     # Use the LLM for chat
#     messages = [
#         ChatMessage(role=MessageRole.USER, content="What is the capital of France?"),
#         ChatMessage(role=MessageRole.ASSISTANT, content="The capital of France is Paris."),
#         ChatMessage(role=MessageRole.USER, content="What's a famous landmark there?")
#     ]
#     chat_response = gemini_api.chat(messages)
#     print(f"Chat response: {chat_response.text}")

# if __name__ == "__main__":
#     main()
# ------------------------------------------------------------------------------------------------------
import os
from typing import Any, Dict
import requests
from llama_index.core.base.llms.types import CompletionResponse, CompletionResponseGen, LLMMetadata
from llama_index.core.llms import CustomLLM
from llama_index.core.llms.callbacks import llm_completion_callback
from pydantic import BaseModel,Field

class CustomGeminiAPI(CustomLLM):
    # api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_API_KEY"))
    api_key: str =  os.getenv("GOOGLE_API_KEY")
    print(api_key)
    api_url: str = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers: dict = Field(default_factory=dict)
    def __init__(self,**data):
        super().__init__(**data)
        # self.api_key = os.getenv("GOOGLE_API_KEY")
        # self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.headers = {
            "Content-Type": "application/json",
            # "x-goog-api-key": self.api_key
        }

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=2048,
            num_output=256,
            model_name="models/gemini-1.5-flash-latest"
        )

    def _make_request(self, prompt: str, **kwargs: Any) -> Dict:
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.5),
                "topP": kwargs.get("top_p", 0.8),
                "topK": kwargs.get("top_k", 40),
                "maxOutputTokens": kwargs.get("max_tokens", 256)
            }
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response_json = self._make_request(prompt, **kwargs)
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        return CompletionResponse(text=text)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response_json = self._make_request(prompt, **kwargs)
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        words = text.split()
        partial_response = ""
        for word in words:
            partial_response += word + " "
            yield CompletionResponse(text=partial_response, delta=word)

# Usage
gemini_api = CustomGeminiAPI()
print(gemini_api.complete("hello"))