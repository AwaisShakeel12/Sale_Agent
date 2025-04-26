from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from app.ag import root_agent

# db_url = "sqlite:///./agentic.sqlite3"
db_url = "sqlite:///./testdb.sqlite3"
session_service = DatabaseSessionService(db_url=db_url)

APP_NAME = "app1"
USER_ID = "user_3"
SESSION_ID = "session_003"

# get session 
session = session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID)


runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
print(f"Session ready: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
