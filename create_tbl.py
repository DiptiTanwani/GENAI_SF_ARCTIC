import streamlit as st
import pandas as pd
import json
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session, DataFrame
import utils as u
import os
from snowflake.connector import connect

# connect to Snowflake
with open(r'C:\Users\004BEI744\IBM\Techathon\AWS GEN AI 2024\GenAI_AWS_Hackathon_Final\creds-sample.json') as f:
    connection_parameters = json.load(f)  
session = Session.builder.configs(connection_parameters).create()

def app():
# title of the streamlit app
   #st.header(f""":rainbow[Snowflake Table Creater]""")
   st.markdown(""" 
                # :blue[Snowflake Table Creater]
                """)
   st.image(r'C:\Users\004BEI744\IBM\Techathon\AWS GEN AI 2024\GenAI_AWS_Hackathon_Final\Images\Create Tables.png', caption= None, width=500) 

# configuring values for session state
   if "messages" not in st.session_state:
     st.session_state.messages = []
# writing the message that is stored in session state
   for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

   if question := st.chat_input("Provide the DDL to Create Snowflake Table"):
    # with the user icon, write the question to the front end
     with st.chat_message("user"):
         st.markdown(question)
    # append the question and the role (user) as a message to the session state
        # st.session_state.messages.append({"role": "user",
        #                              "content": question})
        # respond as the assistant with the answer
     with st.chat_message("assistant"):
        # making sure there are no messages present when generating the answer
         message_placeholder = st.empty()
        # putting a spinning icon to show that the query is in progress
        #with st.status("Creating the table!", expanded=True) as status:
         session.sql(question).collect()
         message_placeholder.markdown(f""" Table created in Snowflake Database """)   