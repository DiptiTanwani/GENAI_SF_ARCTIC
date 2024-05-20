import os
from dotenv import load_dotenv
import yaml
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.sql_database import SQLDatabase
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _postgres_prompt
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.prompts.example_selector.semantic_similarity import (
    SemanticSimilarityExampleSelector,
)
from langchain.vectorstores import Chroma
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import LLMChain
from langchain_community.llms import Replicate
from langchain_core.prompts import PromptTemplate
load_dotenv()

os.environ["REPLICATE_API_TOKEN"] = 'r8_Z9VTSs6E1Q3SAdLolQlW1GZ58SQL1BN1b2FYD'

llm = Replicate(
model="snowflake/snowflake-arctic-instruct",
model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1},
)

# Executing the SQL database chain with the users question
def snowflake_answer(question):
    """
    This function collects all necessary information to execute the sql_db_chain and get an answer generated, taking
    a natural language question in and returning an answer and generated SQL query.
    :param question: The question the user passes in from the frontend
    :return: The final answer in natural langauge along with the generated SQL query.
    """
    # retrieving the final Snowflake URI to initiate a connection with the database
    snowflake_url = get_snowflake_uri()
    # formatting the Snowflake URI and preparing it to be used with Langchain sql_db_chain, selecting the specific
    # tables to be used
    db = SQLDatabase.from_uri(snowflake_url, sample_rows_in_table_info=1, include_tables=["orders","customer","stores","product","date"])
    # loading the sample prompts from SampleData/moma_examples.yaml
    examples = load_samples()
    # initiating the sql_db_chain with the specific LLM we are using, the Snowflake connection string and the
    # selected examples
    sql_db_chain = load_few_shot_chain(llm, db, examples)
    # the answer created by Amazon Bedrock and ultimately passed back to the end user
    answer = sql_db_chain(question)
    # Passing back both the generated SQL query and the final result in a natural language format
    return answer["intermediate_steps"][1], answer["result"]


def get_snowflake_uri():
    # SQLAlchemy 2.0 reference: https://docs.sqlalchemy.org/en/20/dialects/postgresql.html
    # URI format: postgresql+psycopg2://user:pwd@hostname:port/dbname
    """
    This function initiates the creation of the snowflake URL for use with the SQLDatbaseChain
    :return: The full snowflake URL that is used to query against
    """
    # setting the key parameters to build the Snowflake connection string, these are stored in the .env file
    #snowflake_account = os.getenv("snowflake_account")
    #username = os.getenv("username")
    #password = os.getenv("password")
    #database = os.getenv("database")
    #schema = os.getenv("schema")
    #role = os.getenv("role")
	
    snowflake_account = "dvdjvwb-ik29782"
    username = "netravatihegde"
    password = "IBMaws2024"
    database = "TECHNOVA"
    schema = "PUBLIC"
    role = "ACCOUNTADMIN"
    tables = ["orders","customer","stores","product","date"]
    #aws_cli_profile = "default"

# Building the Snowflake URL to use with the DB_chain
    snowflake_url = f"snowflake://{username}:{password}@{snowflake_account}/{database}/{schema}?role={role}"
    # returning the final Snowflake URL that was built in the line of code above
    return snowflake_url


def load_samples():
    """
    Load the sql examples for few-shot prompting examples
    :return: The sql samples in from the SampleData/moma_examples.yaml file
    """
    # instantiating the sql samples variable
    sql_samples = None
    # opening our prompt sample file
    with open(r'C:\Users\004BEI744\IBM\Techathon\SF_ARCTIC\customer_examples.yaml') as stream:
        # reading our prompt samples into the sql_samples variable
        sql_samples = yaml.safe_load(stream)
    # returning the sql samples as a string
    return sql_samples

def load_few_shot_chain(llm, db, examples):
    """
    This function is used to load in the most similar prompts, format them along with the users question and then is
    passed in to Amazon Bedrock to generate an answer.
    :param llm: Large Language model you are using
    :param db: The Snowflake database URL
    :param examples: The samples loaded from your examples file.
    :return: The results from the SQLDatabaseChain
    """
    # This is formatting the prompts that are retrieved from the SampleData/moma_examples.yaml
    example_prompt = PromptTemplate(
        input_variables=["table_info", "input", "sql_cmd", "sql_result", "answer"],
        template=(
            "{table_info}\n\nQuestion: {input}\nSQLQuery: {sql_cmd}\nSQLResult:"
            " {sql_result}\nAnswer: {answer}"
        ),
    )
    # instantiating the hugging face embeddings model to be used to produce embeddings of user queries and prompts
    local_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # The example selector loads the examples, creates the embeddings, stores them in Chroma (vector store) and a
    # semantic search is performed to see the similarity between the question and prompts, it returns the 3 most similar
    # prompts as defined by k
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        local_embeddings,
        Chroma,
        k=min(3, len(examples)),
    )
    # This is orchestrating the example selector (finding similar prompts to the question), example_prompt (formatting
    # the retrieved prompts, and formatting the chat history and the user input
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_postgres_prompt + "Provide no preamble" + " Here are some examples:",
        suffix=PROMPT_SUFFIX,
        input_variables=["table_info", "input", "top_k"],
    )
    # Where the LLM, DB and prompts are all orchestrated to answer a user query.
    return SQLDatabaseChain.from_llm(
        llm,
        db,
        prompt=few_shot_prompt,
        use_query_checker=False,  # must be False for OpenAI model
        verbose=True,
        return_intermediate_steps=True,
    )
