import pandas as pd
from datetime import datetime, timedelta
import time
from app.views import external_trigger_followup_conversation



CSV_FILE_PATH = r'E:\django\djang x gen\sale_agent\project\app\lead.csv'


def trigger_follow_up():
    print("[Trigger] Checking for unresponsive leads...")
    
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        now = datetime.now()

        # check for both condition true  
        for index, row in df[(df["status"] == "no") & (df["follow_up_sent"] != "yes")].iterrows():

            lead_time = datetime.fromisoformat(row["timestamp"])
            if now >= lead_time + timedelta(minutes=1):
                print(f"[Follow-up] Triggering follow-up for lead_id: {row['lead_id']}")
                external_trigger_followup_conversation()
                
                # update the no to yes after followup
                df.at[index, "follow_up_sent"] = "yes"
                df.to_csv(CSV_FILE_PATH, index=False)

    except Exception as e:
        print("Error in follow-up trigger:", str(e))



def run_follow_up_checker(interval_seconds=10):
    print("[System] Starting automatic follow-up checker...")
    while True:
        trigger_follow_up()
        time.sleep(interval_seconds)
run_follow_up_checker()