from django.shortcuts import render, redirect
from django.shortcuts import render
from google.genai import types
import os
from app.session_1 import runner, USER_ID, SESSION_ID




def external_trigger_start_conversation():
    print("[Trigger] Starting agent conversation...")

    initial_message = types.Content(
        role="user",
        parts=[types.Part(text="Hello, I just entered the app!")]
    )

    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=initial_message)

    for event in events:
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print("Agent says:", response_text)
            return response_text  # return to use in session
    return ""




def external_trigger_followup_conversation():
    print("[Trigger] follow up agent conversation...")

    initial_message = types.Content(
        role="user",
        parts=[types.Part(text="Just checking in to see if you're still interested. Let me know when you're ready to continue.")]
    )

    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=initial_message)

    for event in events:
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print("Agent says:", response_text)

            #  Save to a file 
            with open("followup_message.txt", "w", encoding="utf-8") as f:
                f.write(response_text)

            return response_text
    return ""




def first(request):
    if request.method == 'POST':
        from google.adk.sessions import DatabaseSessionService
        from google.adk.agents import Agent
        from google.adk.runners import Runner
        from app.ag import root_agent
        
        # db_url = "sqlite:///./agentic.sqlite3"
        db_url = "sqlite:///./testdb.sqlite3"
        session_service = DatabaseSessionService(db_url=db_url)
        
        
        APP_NAME = "app1"
        USER_ID = "user_3"
        SESSION_ID = "session_003"
        
        session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID)

        runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
        print(f"Session ready: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
        ai_response = external_trigger_start_conversation()
        request.session['ai_first_message'] = ai_response  # store it temporarily
        return redirect('home')

    return render(request, 'first.html')






def home(request):
    # Initialize conversation if not present
    if 'conversation' not in request.session:
        request.session['conversation'] = []

        # Add AI's first message if it exists
        if 'ai_first_message' in request.session:
            ai_first = request.session.pop('ai_first_message')
            request.session['conversation'].append({'sender': 'AI', 'message': ai_first})

    conversation = request.session['conversation']

    # if follow-up message was triggered 

    followup_path = "followup_message.txt"
    if os.path.exists(followup_path):
        with open(followup_path, "r", encoding="utf-8") as f:
            followup_msg = f.read()

        if followup_msg:
            conversation.append({"sender": "AI", "message": followup_msg})
            os.remove(followup_path)  # Prevent showing again
            request.session['conversation'] = conversation
            request.session.modified = True

    if request.method == "POST":
        user_message = request.POST.get("message", "")

        if user_message:
            conversation.append({"sender": "User", "message": user_message})

            # Send to AI
            content = types.Content(role="user", parts=[types.Part(text=user_message)])
            events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

            for event in events:
                if event.is_final_response():
                    ai_response = event.content.parts[0].text
                    conversation.append({"sender": "AI", "message": ai_response})
                    break

            request.session['conversation'] = conversation
            request.session.modified = True

    return render(request, "chat.html", {"conversation": conversation})
