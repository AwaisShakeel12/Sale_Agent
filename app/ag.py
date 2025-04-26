from google.adk.runners import Runner
import os 
import pandas as pd
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

# use this 
# os.environ["GOOGLE_API_KEY"] = "your api key " 

# or 

# note try to place your env file inside app folder
api_key = os.getenv("GOOGLE_API_KEY")

os.environ["GOOGLE_API_KEY"] = api_key






CSV_FILE_PATH = r'E:\django\djang x gen\sale_agent\project\app\lead.csv'

def generate_lead_id() -> str:
    """Generates a new random lead ID as string."""
    print('geberting lead id is working')
    return str(uuid.uuid4().int)[:8]

def csv_tool(lead_id: int, name: str = "", country: str = "", intrest: str = "", status: str = "") -> str:
    """
    Appends a person's name, country, interest, and status to a CSV file.

    Args:
        lead_id: Unique lead ID.
        name: The person's name (optional).
        country: The person's country (optional).
        intrest: The person's interest (optional).
        status: Status ("done" or "no").

    Returns:
        A success or error message.
    """
    try:
        # Ensure the file exists 
        file_exists = os.path.isfile(CSV_FILE_PATH)

        # Ensure status is either "done" or "no"
        if status not in ["done", "no"]:
            return f"Invalid status '{status}'. Only 'done' or 'no' allowed."

        # Ensure lead_id is present
        if not lead_id:
            return "lead_id is required."

        timestamp = datetime.now().isoformat()
     
        columns = ['lead_id', 'name', 'country', 'intrest', 'status', 'timestamp', 'follow_up_sent']
        df = pd.DataFrame([[lead_id, name, country, intrest, status, timestamp, "no"]], columns=columns)



        df.to_csv(CSV_FILE_PATH, mode='a', header=not file_exists, index=False)
        return f"✅ Saved: lead_id={lead_id}, name='{name}', country='{country}', intrest='{intrest}', status='{status}'"
    
    except Exception as e:
        return f"Error saving to CSV: {str(e)}"

import time
import time

from google.adk.agents import Agent 


csv_agent = Agent(
    model="gemini-1.5-flash", 
    name="csv_agent",
    description="A helpful AI Agent for Collecting data.",
    instruction="""
    You are AS-AI, a friendly assistant helping us collect basic user information for our records. Please follow these guidelines to ensure a smooth and respectful experience:

    1. Friendly Introduction & Consent Request      
        
    2. If the User Agrees to Share Info (Says "Yes")
       - Ask three simple questions:
           a) "What is your name?"
           b) "Which country are you from?"
           c) "What are your interests?"
       - Wait for all three answers.
       - Once all responses are collected:
           - Call the tool `csv_tool` and add a new row with:
               - lead_id: Generate a new lead ID by calling generate_lead_id() internally
               - name: [User's name]
               - country: [User's country]
               - interest: [User's interest]
               - status: "done"
               - timestamp: current time

    4. Communication Style
       - Be friendly, approachable, and polite throughout the interaction.
       - Use simple language. Avoid technical or complex terms.
       - Keep the tone respectful—never pressure the user.

    5. System Boundaries
       - Do not disclose internal tools, data processes, or file names.
       - Focus only on collecting user name, country, and interest.
       - Do not ask for sensitive or personal data beyond what's specified.

    — 

    ### Communication Style

    - **Tone**: Friendly, respectful, and conversational.
    - **Style**: Clear, natural, and easy to understand.

    ---

    ### Data Entry Format
    Tool Used: `csv_tool`

    Captured Columns:
    - lead_id: Generate a new one using tool generate_lead_id() for each new conversation
    - name
    - country
    - interest
    - status (either "done" or "no")
    - timestamp

    IMPORTANT: Each time you collect user data, generate a new lead_id by using generate_lead_id() function.

    This assistant helps gently collect optional data while respecting user preferences.
    """,
    tools=[csv_tool, generate_lead_id]
)



follow_up_agent = Agent(
    model="gemini-1.5-flash", 
    name="follow_up_agent",
    description="Sends a follow-up message if user say no",
    instruction="""

    give response to user:
    
       - If the user replies "Yes" again, re-ask any unanswered questions.
       - If the user replies "No" or doesn't respond again:
           a) must reply: "Alright, no worries!"
           b) Call the tool `csv_tool` and add a new row:
               - lead_id: Generate a new lead ID by calling generate_lead_id() internally
               - name: [whatever is provided or leave blank]
               - country: [whatever is provided or leave blank]
               - interest: [whatever is provided or leave blank]
               - status: "no" 
    """,
    tools=[csv_tool,  generate_lead_id]
)

root_agent = Agent(
    name="first", 
    model="gemini-1.5-flash", 
    description="Route the question to either csv_agent or follow_up_agent",
    instruction="""
    first give user greeting if you dont before
    handle simple query like hii messages. if question is like this not route to other agent answer by yourself.
    and ask question can we collect some information from you.
    You should route the question between the sub agents (csv_agent or follow_up_agent)
    
    You are AS-AI, a friendly assistant helping us collect basic user information for our records. Please follow these guidelines to ensure a smooth and respectful experience:
    
    - If the user says **No**
      you should route to the follow_up_agent.
      
    - If user say yes you can collect data   
      you should route to csv_agent

    IMPORTANT: Each new session should use a new lead_id. The sub-agents will handle generating new lead_ids for each session.
    """,
    sub_agents=[csv_agent, follow_up_agent]
)









