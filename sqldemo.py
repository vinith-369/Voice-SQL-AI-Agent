# # C:\Users\Acer\AppData\Local\Programs\Python\Python39\Scripts\streamlit.exe run sqldemo.py 

# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# import pandas as pd
# from sqlalchemy import create_engine
# import streamlit as st
# import speech_recognition as sr


# api_key ="AIzaSyDaM0twsGt6Rv5M2pY4ze4lZlKc7IQWuiQ"

# llm_name = "gemini-2.5-flash"
# model = ChatGoogleGenerativeAI(api_key=api_key, model=llm_name)

# # from langchain.agents import create_sql_agent
# from langchain_community.agent_toolkits.sql.base import create_sql_agent
# from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
# from langchain_community.utilities import SQLDatabase

# # Path to your SQLite database file
# database_file_path = "./db/salary.db"

# # Create an engine to connect to the SQLite database
# engine = create_engine(f"sqlite:///{database_file_path}")
# file_url = "./salaries_2023.csv"
# os.makedirs(os.path.dirname(database_file_path), exist_ok=True)
# df = pd.read_csv(file_url).fillna(value=0)
# df.to_sql("salaries_2023", con=engine, if_exists="replace", index=False)



# MSSQL_AGENT_PREFIX = """
# You are an agent designed to interact with a SQL database.
# ## Instructions:
# - Given an input question, create a syntactically correct {dialect} query
# to run, then look at the results of the query and return the answer.
# - Unless the user specifies a specific number of examples they wish to
# obtain, **ALWAYS** limit your query to at most {top_k} results.
# - You can order the results by a relevant column to return the most
# interesting examples in the database.
# - Never query for all the columns from a specific table, only ask for
# the relevant columns given the question.
# - You have access to tools for interacting with the database.
# - You MUST double check your query before executing it.If you get an error
# while executing a query,rewrite the query and try again.
# - DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
# to the database.
# - DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS
# OF THE CALCULATIONS YOU HAVE DONE.
# - Your response should be in Markdown. However, **when running  a SQL Query
# in "Action Input", do not include the markdown backticks**.
# Those are only for formatting the response, not for executing the command.
# - ALWAYS, as part of your final answer, explain how you got to the answer
# on a section that starts with: "Explanation:". Include the SQL query as
# part of the explanation section.
# - If the question does not seem related to the database, just return
# "I don\'t know" as the answer.
# """

# MSSQL_AGENT_FORMAT_INSTRUCTIONS = """
# ## Use the following format:

# Question: the input question you must answer.
# Thought: you should always think about what to do.
# Action: the action to take, should be one of [{tool_names}].
# Action Input: the input to the action.
# Observation: the result of the action.
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer.
# Final Answer: the final answer to the original input question.
# """

# db = SQLDatabase.from_uri(f"sqlite:///{database_file_path}")
# toolkit = SQLDatabaseToolkit(db=db, llm=model)

# sql_agent = create_sql_agent(
#     prefix=MSSQL_AGENT_PREFIX,
#     format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,
#     llm=model,
#     toolkit=toolkit,
#     top_k=30,
#     verbose=True,
# )

# # Streamlit interface with styling
# st.set_page_config(
#     page_title="SQL Query AI Agent",
#     page_icon=":robot:",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # Title and description
# st.title("Voice-SQL AI Agent")
# st.markdown(
#     """
#     Welcome to the **SQL Query AI Agent**! This app allows you to:
#     - Query a database using natural language.
#     - Use voice input for queries.
#     """
# )

# # Function to capture voice input and convert to text
# def get_voice_input():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening for your query... Speak now!")
#         try:
#             audio = recognizer.listen(source, timeout=5)
#             st.info("Processing your voice input...")
#             query = recognizer.recognize_google(audio)
#             st.success(f"Recognized query: {query}")
#             return query.strip()  # Strip extra spaces
#         except sr.UnknownValueError:
#             st.error("Sorry, I could not understand the audio.")
#         except sr.RequestError as e:
#             st.error(f"Could not request results; {e}")
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#     return None

# # Initialize session state for the question
# if "question" not in st.session_state:
#     st.session_state["question"] = ""

# # Option to choose between text or voice input
# st.sidebar.header("Input Options")
# input_mode = st.sidebar.radio("Choose input mode:", ("Text", "Voice"))

# if input_mode == "Text":
#     st.session_state["question"] = st.text_input("Enter your query:", value=st.session_state["question"])
# elif input_mode == "Voice":
#     if st.button("Record Voice Query"):
#         voice_query = get_voice_input()
#         if voice_query:
#             st.session_state["question"] = voice_query

# # Display the current query for debugging
# st.write(f"Current query: {st.session_state['question']}")

# if st.button("Run Query"):
#     if st.session_state["question"]:
#         try:
#             # Debugging: Log the query
#             st.info(f"Processing query: {st.session_state['question']}")

#             # Invoke the SQL agent
#             res = sql_agent.invoke(st.session_state["question"])

#             # Debugging: Log the raw output
#             st.info("Query executed successfully. Raw output:")
#            # st.json(res)  # Display the raw response for debugging

#             # Display the final output
#             if "output" in res:
#                 st.markdown(res["output"])
#             else:
#                 st.error("No output returned by the SQL agent.")
#         except Exception as e:
#             # Handle errors gracefully
#             st.error(f"An error occurred while processing the query: {e}")
#     else:
#         st.error("Please provide a query.")







import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import speech_recognition as sr

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

# ------------------ API and LLM setup ------------------
api_key = "AIzaSyDaM0twsGt6Rv5M2pY4ze4lZlKc7IQWuiQ"
llm_name = "gemini-2.5-flash"
model = ChatGoogleGenerativeAI(api_key=api_key, model=llm_name)

# ------------------ Database setup ------------------
db_dir = "./db"
os.makedirs(db_dir, exist_ok=True)
database_file_path = os.path.join(db_dir, "uploaded_files.db")
engine = create_engine(f"sqlite:///{database_file_path}")

db = SQLDatabase.from_uri(f"sqlite:///{database_file_path}")
toolkit = SQLDatabaseToolkit(db=db, llm=model)

MSSQL_AGENT_PREFIX = """
You are an agent designed to interact with a SQL database.
## Instructions:
- Given an input question, create a syntactically correct {dialect} query
to run, then look at the results of the query and return the answer.
- Unless the user specifies a specific number of examples they wish to
obtain, **ALWAYS** limit your query to at most {top_k} results.
- You can order the results by a relevant column to return the most
interesting examples in the database.
- Never query for all the columns from a specific table, only ask for
the relevant columns given the question.
- You have access to tools for interacting with the database.
- You MUST double check your query before executing it.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
to the database.
- DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS
OF THE CALCULATIONS YOU HAVE DONE.
- Your response should be in Markdown, but **do not include markdown backticks in Action Input.**
- ALWAYS include a section starting with "Explanation:" showing how you arrived at the answer with the SQL query used.
- If unrelated to the database, respond with "I don't know".
"""

MSSQL_AGENT_FORMAT_INSTRUCTIONS = """
## Use the following format:

Question: the input question you must answer.
Thought: you should always think about what to do.
Action: the action to take, should be one of [{tool_names}].
Action Input: the input to the action.
Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: the final answer to the original input question.
"""

sql_agent = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,
    format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,
    llm=model,
    toolkit=toolkit,
    top_k=30,
    verbose=True,
)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="SQL Query AI Agent", page_icon="🧠", layout="wide")
st.title("🧠 SQL Query AI Agent with Voice and File Upload")
st.markdown("Upload CSV files to build your database, then query using natural language or voice input.")

# ------------------ File Upload Section ------------------

uploaded_file = st.file_uploader("Upload a CSV file to add to the database:", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file).fillna(0)
        table_name = uploaded_file.name.split(".")[0]
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        st.success(f"File '{uploaded_file.name}' uploaded and table '{table_name}' created successfully!")
        st.write(df.head())
    except Exception as e:
        st.error(f"Failed to upload or parse file: {e}")

# ------------------ Voice Input Function ------------------

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak your query.")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.info("Processing voice input...")
            query = recognizer.recognize_google(audio)
            st.success(f"Recognized: {query}")
            return query.strip()
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Voice service error: {e}")
        except Exception as e:
            st.error(f"Voice capture error: {e}")
    return None

# ------------------ Query Section ------------------

st.sidebar.header("Query Input Options")
input_mode = st.sidebar.radio("Choose input mode:", ["Text", "Voice"])

if "question" not in st.session_state:
    st.session_state["question"] = ""

if input_mode == "Text":
    st.session_state["question"] = st.text_input("Enter your natural language SQL query:", value=st.session_state["question"])
else:
    if st.button("Record Voice Query"):
        voice_query = get_voice_input()
        if voice_query:
            st.session_state["question"] = voice_query

st.write(f"**Current Query:** {st.session_state['question']}")

# ------------------ Run Query Button ------------------

if st.button("Run Query"):
    if st.session_state["question"]:
        try:
            st.info(f"Running: {st.session_state['question']}")
            res = sql_agent.invoke(st.session_state["question"])
            if "output" in res:
                st.markdown(res["output"])
            else:
                st.error("The agent did not return an output.")
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.warning("Please enter a query before running.")

