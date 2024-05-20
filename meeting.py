import streamlit as st
import replicate
import os
#from transformers import AutoTokenizer

replicate_api = st.secrets['REPLICATE_API_TOKEN']

#os.environ["REPLICATE_API_TOKEN"] = 'r8_Z9VTSs6E1Q3SAdLolQlW1GZ58SQL1BN1b2FYD'

# Function for generating Snowflake Arctic response
def generate_arctic_response():
    prompt = []
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            prompt.append("<|im_start|>user\n" + dict_message["content"] + "<|im_end|>")
        else:
            prompt.append("<|im_start|>assistant\n" + dict_message["content"] + "<|im_end|>")
    
    prompt.append("<|im_start|>assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                           input={"prompt": prompt_str,
                                  "prompt_template": r"{prompt}",
                                  "temperature": 0.30,
                                  "top_p": 0.90,
                                  }):
        yield str(event)

def app():
# App title
   st.title(f""":blue[Meeting Summary Generation with Snowflake Arctic]""")
   st.image(r'C:\Users\004BEI744\IBM\Techathon\SF_ARCTIC\Images\Meeting_Summary_SF.png', caption= None, width=500) 
   if "messages" not in st.session_state:
     st.session_state.messages = []
   if prompt := st.chat_input("Provide the meeting transcript"):

     st.session_state.messages.append({"role": "user", "content": prompt})
     with st.chat_message("user"):
         st.write(prompt)

     with st.chat_message("assistant"):
         response = generate_arctic_response()
         full_response = st.write_stream(response)
     st.session_state.messages = []
