# Save as windows_log_analyzer.py
import os
import pandas as pd
from openai import OpenAI

# 1. Load the client and API key from the environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Ingest the CSV file using the pandas library
# Note: You may need to install pandas if you haven't already: pip install pandas
try:
    df = pd.read_csv("../ai/week-2/events.csv")
    
    # Convert the DataFrame to a simple string for the LLM
    # We use .to_string() for a clean, non-CSV format
    log_content = df.to_string(index=False)

except FileNotFoundError:
    print("Error: events.csv not found. Make sure the file is in the same directory.")
    exit()

# --- START OF PROMPT TUNING EXERCISE: THE BLUNT PROMPT ---
# This is our first prompt style (blunt: "Summarize.")
prompt = f"""You are an expert Windows Sysadmin. 
Summarize the following Windows Event log data concisely.

LOG DATA (in table format):
{log_content}
"""

print("--- Running Log Analysis (Blunt Prompt) ---")

try:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=400
    )
    # Print the raw response
    summary_output = resp.choices[0].message.content
    print(summary_output)
    
except Exception as e:
    print(f"\nAPI Error: {e}")
    print("Please check your OPENAI_API_KEY environment variable and internet connection.")


# Deliverable Check: Did you run a simple script and get a summary?
# Next step will be the 'structured' and 'few-shot' prompts.