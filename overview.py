import streamlit as st

def app():
    
    st.markdown(""" 
                # :blue[GEN-AI Project Lifecycle Optimizer using Snowflake Arctic]
                """)

    
    st.image(r'C:\Users\004BEI744\IBM\Techathon\SF_ARCTIC\Images\Overview_SF.png', caption= None, width=700) 
                  
    st.markdown(""" 
                 ##### :blue[1. Meeting Summary Generation]
                Condensing discussions and email correspondence into concise summaries.
                ##### :blue[2. Data model Design Assistant]
                Choosing the data model format, drafting DDLs and DMLs for tables, and formulating test scenarios.
                ##### :blue[3. Snowflake Table Creater]
                Creating tables in Snowflake database.
                ##### :blue[4. Snowflake Data Loader]
                Inserting data into Snowflake tables.
                ##### :blue[5. Entity Relationship Diagram]
                Designing an Entity Relationship Diagram (ERD) for the data model.
                ##### :blue[6. Natural Language Query Against Snowflake Tables]
                Responding to natural language queries from a Snowflake table.
            """)
    
                    
