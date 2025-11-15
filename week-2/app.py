# week-2/app.py
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template_string, request
from openai import OpenAI
from pattern_parser import parse_logs

client = OpenAI()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Log Pattern Analyzer</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f8ff;
            padding: 30px;
            max-width: 1000px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        form {
            background: lightgray;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        input[type="file"] {
            display: block;
            margin: 10px 0;
            width: 100%;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
        pre {
            background: #f7f7f7;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 100%;
        }
    </style>
</head>
<body>
    <h1>AI Log Pattern Analyzer</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="log_files" multiple>
        <button type="submit">Analyze Logs</button>
    </form>

    {% if summary %}
    <hr>
    <h2>AI + Regex Summary</h2>
    <pre>{{ summary }}</pre>
    {% endif %}
</body>
</html>
"""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_files():
    summary = None

    if request.method == "POST":
        uploaded_files = request.files.getlist("log_files")
        combined_logs = ""

        # Read multiple files and combine safely
        for file in uploaded_files:
            if file and file.filename:
                try:
                    text = file.read().decode("utf-8", errors="ignore")
                    combined_logs += f"\n\n--- FILE: {file.filename} ---\n{text}"
                except Exception as e:
                    combined_logs += f"\n\n[Error reading {file.filename}: {e}]"

        # Parse with regex pattern analyzer
        parsed = parse_logs(combined_logs)

        # Summarize using GPT
        prompt = f"""
You are a senior system log analyst.
Below are log entries parsed from multiple files.

Entries (sample of first 20):
{parsed[:20]}

Analyze and summarize key patterns, repeated errors, and potential root causes.
Provide your response in Markdown with sections:
- Pattern Overview
- Common Error Sources
- Recommendations
"""

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=900
            )
            summary = resp.choices[0].message.content
        except Exception as e:
            summary = f"⚠️ Error during GPT processing: {e}"

    return render_template_string(HTML_TEMPLATE, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
