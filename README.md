# AI Lead Collector Agent
This project is an AI-powered lead collection system built using Google ADK and Django. It automates user interaction and data collection via a conversational agent triggered by form submission.

🔧 Features
Form-Triggered AI Agent: The conversation begins automatically when a user submits a form.

Consent-Based Interaction: The AI asks for permission to collect user details.

Smart Data Collection:

If the user agrees, the agent collects:

Name

Country

Interest

The data is stored in a CSV file with status done.

If the user declines, an empty row with status no is stored.

Follow-Up System:

Sends a follow-up message after a few minutes if the user declined or didn’t respond.

Session & History Storage:

Uses SQLite for permanent session and message history storage.

📦 Tech Stack
Google ADK (Agent Development Kit)

Django (Backend Framework)

SQLite (Session & History DB)

CSV (Lead Data Storage)



## Video demo

[Video Demo](https://drive.google.com/file/d/1RLKXWndZKrPt6hRMoO3dbmBHicFeN8Yi/view?usp=sharing)


## Documentation

[Documentation](https://drive.google.com/file/d/1t80F2TbtprwVtgsexI-gGm2TFy9C88Vm/view?usp=sharing)

## Activate Env

## Virtaul ENV

Virtaul Env

```bash
  virtualenv env
```
## Activate Env



```bash
  env/Scripts/activate
```    

## Installation 

Install Django

```bash
  pip install django
```    


Install Google ADK

```bash
  pip install google-adk
```    



Install Pandas

```bash
  pip install pandas
```

Install dotenv

```bash
  pip install dotenv
```    

## RUN

For Django project

```bash
  python manage.py runserver
```


## RUN Seprate Followup_trigger.py



```bash
  python -m app.followup_trigger
```


## 🚀 About Me
AI Developer
[Website](https://awaisshakeel12.pythonanywhere.com/)


