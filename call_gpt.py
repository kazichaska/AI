from openai import OpenAI
client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"Say hi from my Mac"}]
)
print(resp.choices[0].message.content)