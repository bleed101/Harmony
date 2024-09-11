# Harmony

# Setup
- Make a seperate env for development.
- `pip install -r requirements.txt`
- Create a .env file with desired API keys.
- Create a collection under ChromaDB.
  - On Successfull creation spin off the server `chroma run --host localhost --port 8000 --path ./my_chroma_data`
- You need to install Neo4j(community) Desktop version.
  - Create new Project.
  - Start the project.
  - Launch the browser which will expose the endpoint of the the Neo4j server.
- `streamlit run app.py`
