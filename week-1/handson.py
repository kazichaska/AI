# save as call_gpt.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """You are an expert sysadmin. Summarize the following log excerpt in three bullet points and give likely causes.
LOG:
2025-10-24T12:32:41Z hostd[2312]: warning hostd detected datastore latency above threshold on datastore1
2025-10-24T12:32:45Z vpxa[1180]: info vCenter connection re-established
2025-10-24T12:33:12Z hostd[2312]: error vmnic1 link down
2025-10-24T12:34:01Z vmkernel: cpu6: PF Exception 14 in world 1234:vmx-vmname (12345) guest state 0x7
"""

resp = client.chat.completions.create(
    model="gpt-4o-mini", # or "gpt-4o" if available in your account
    messages=[{"role":"user","content":prompt}],
    max_tokens=400
)
print(resp.choices[0].message.content)
# To run this script, set your API key in the environment variable and execute:
# export OPENAI_API_KEY='your-actual-api-key-here'
# python call_gpt.py