# save as smb_content.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- NEW SMB-FOCUSED PROMPT ---
prompt = """You are an expert social media and marketing assistant for a local, family-owned pizza shop.
The pizza shop is running a '2 Large Pizzas for $30' special this weekend.

Generate three distinct pieces of content for this special:
1. A short, punchy Instagram caption with 3 relevant emojis.
2. A 3-sentence script for a 15-second TikTok video.
3. A brief, polite email subject and body text for their email newsletter.
"""

resp = client.chat.completions.create(
    model="gpt-4o-mini", # or "gpt-4o" if available in your account
    messages=[{"role":"user","content":prompt}],
    max_tokens=400
)
print(resp.choices[0].message.content)