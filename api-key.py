from openai import OpenAI
import os

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")  # Get API key from environment variable
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(response.choices[0].message.content);

