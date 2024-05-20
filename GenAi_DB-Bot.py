## Import all apps which you want to merge in one project 
import overview
import meeting
import dmda
import create_tbl
import load_tbl
import report_sql
import erd_app

## Import necessary libraries 

import streamlit as st

PAGES = {
    "Overview": overview,
    "Meeting Summary Generation": meeting,
    "Data Model Design Assistant": dmda,
    "Snowflake Table Creator": create_tbl,
    "Snowflake Data Loader": load_tbl,
    "Entity Relationship Diagram": erd_app,
    "Natural Language Query Against Snowflake Tables": report_sql
    #"Image Generation": image_app
}

st.sidebar.title(f""":blue[GEN-AI Project Lifecycle Optimizer]""")
selection = st.sidebar.radio("Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything:", list(PAGES.keys()))
page = PAGES[selection]
page.app()


#st.image('Data Warehouse 1.png', caption= None)
