# GENAI_SF_ARCTIC

#Prerequisites

Python 3.8 or later 🐍
pip3 📦
Installation

Clone this repository

git clone https://github.com/yourusername/snowflake-arctic-chatbot.git
cd snowflake-arctic-chatbot
Install requirements

   pip install -r requirements.txt
Add your API token to your secrets file
Create a .streamlit folder with a secrets.toml file inside.

mkdir .streamlit
cd .streamlit
touch secrets.toml
Use your text editor or IDE of choice to add the following to secrets.toml:

REPLICATE_API_TOKEN = "your API token here"
Learn more about Streamlit secrets management in our docs.

Alternatively, you can enter your Replicate API token via the st.text_input widget in the app itself (once you're running the app).

Run the Streamlit app Note: there are two versions of the app included in this repo.
