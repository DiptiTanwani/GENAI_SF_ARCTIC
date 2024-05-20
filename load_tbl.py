import streamlit as st
import pandas as pd
import json
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session, DataFrame
import utils as u
import os
from snowflake.connector import connect
import time
import configparser, re, json, os

# connect to Snowflake
with open(r'C:\Users\004BEI744\IBM\Techathon\AWS GEN AI 2024\GenAI_AWS_Hackathon_Final\creds-sample.json') as f:
    connection_parameters = json.load(f)  
session = Session.builder.configs(connection_parameters).create()

def loadInferAndPersist(file) -> snowpark.DataFrame:
    file_df = pd.read_csv(file)
    snowparkDf=session.write_pandas(file_df, 'CUSTOMER_TEST', auto_create_table=False, overwrite=True)
    return snowparkDf

def get_dataset(table):
    # load messages df
    df = session.table(table)
    return df

class Table:
    def __init__(self, name, comment):
        self.name = name
        self.comment = comment if comment is not None and comment != 'None' else ''
        self.label = None

        self.columns = []           # list of all columns
        self.uniques = {}           # dictionary with UNIQUE constraints, by name + list of columns
        self.pks = []               # list of PK columns (if any)
        self.fks = {}               # dictionary with FK constraints, by name + list of FK columns


    @classmethod
    def getClassName(cls, name, useUpperCase, withQuotes=True):
        if re.match("^[A-Z_0-9]*$", name) == None:
            return f'"{name}"' if withQuotes else name
        return name.upper() if useUpperCase else name.lower()


    def getName(self, useUpperCase, withQuotes=True):
        return Table.getClassName(self.name, useUpperCase, withQuotes)
        
def getDatabase():
    global session
    names = []
    query = "show databases"
    results = session.sql(query).collect()
    for row in results:
        names.append(str(row["name"]))
    sel = 0 if "TECHNOVA" not in names else names.index("TECHNOVA")
    return st.selectbox('Database', tuple(names), index=sel,
        help="Select an existing database")


def getSchema(database):
    global session
    names = []
    if database != "":
        query = f"show schemas in database {Table.getClassName(database, False)}"
        results = session.sql(query).collect()
        for row in results:
            schemaName = str(row["name"])
            if schemaName != "INFORMATION_SCHEMA":
                names.append(schemaName)
    sel = 0 if "PUBLIC" not in names else names.index("PUBLIC")
    return st.selectbox('Schema', tuple(names), index=sel, 
        help="Select a schema for the current database")

def getTable(database,schema):
    global session
    names = []
    if database != "":
        query = f"show tables in database {Table.getClassName(database, False)}"
        results = session.sql(query).collect()
        for row in results:
            tableName = str(row["name"])
            if tableName != "TEST":
                names.append(tableName)
    sel = 0 if "CUSTOMER_TEST" not in names else names.index("CUSTOMER_TEST")
    return st.selectbox('Table', tuple(names), index=sel, 
        help="Select a table for the current schema")        
    

def app():
# title of the streamlit app
   #st.header(f""":rainbow[Snowflake Data Loader]""")
   st.markdown(""" 
                # :blue[Snowflake Data Loader]
                """)
   st.image(r'C:\Users\004BEI744\IBM\Techathon\AWS GEN AI 2024\GenAI_AWS_Hackathon_Final\Images\Load Tables.png', caption= None, width=500) 
   
   st.markdown (""" 
                ---
                """)
   
   st.header(f""":blue[Insert data using a csv file]""")
   
   file = st.file_uploader(" ", type={"csv"})
   if file is not None:
        df= loadInferAndPersist(file)
        st.write("Data loaded to Snowflake table")
        with st.expander("Technical information"):
        
            u.describeSnowparkDF(df)
            st.write("Data loaded to Snowflake:")
            st.dataframe(df)
   st.markdown (""" 
                ---
                """) 
   st.header(f""":blue[Snowflake Table Editor️]""")
   st.write("Select a table to update/add/delete data:")
   
   global database, schema, table
   database = getDatabase()
   schema = getSchema(database)
   table = getTable(database,schema)

   dataset = get_dataset(table)

   with st.form("data_editor_form"):
       st.caption("Edit the dataframe below:")
       edited = st.data_editor(dataset, use_container_width=True, num_rows="dynamic")
       submit_button = st.form_submit_button("Submit")

   if submit_button:
      try:
        #Note the quote_identifiers argument for case insensitivity
          session.write_pandas(edited, "CUSTOMER_TEST", overwrite=True)
          st.success("Table updated")
          time.sleep(5)
      except:
             st.warning("Error updating table")
    #display success message for 5 seconds and update the table to reflect what is in Snowflake
      st.rerun()


