# week-1/app.py
from flask import Flask, render_template_string, request, send_file
from openai import OpenAI
import os
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>AI Log Analyzer</title>
  <style>
    body { font-family: Arial; margin: 50px; background: #f7f7f7; }
    h1 { color: #333; }
    form { margin-bottom: 20px; }
    textarea { width: 100%; height: 150px; }
    .result { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .download-btn { margin-top: 10px; }
  </style>
</head>
<body>
  <h1>AI Log Analyzer</h1>
  <form method="POST" enctype="multipart/form-data">
    <input type="file" name="logfile" accept=".log,.txt" required><br><br>
    <button type="submit">Analyze Log</button>
  </form>

  {% if summary %}
    <div class="result">
      <h2>Analysis Result:</h2>
      <pre>{{ summary }}</pre>
      <form method="POST" action="/download">
        <input type="hidden" name="summary" value="{{ summary }}">
        <button type="submit" class="download-btn">Download Summary (.txt)</button>
      </form>
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    summary = None
    if request.method == "POST":
        file = request.files["logfile"]
        log_data = file.read().decode("utf-8")

        prompt = f"""
        You are a senior VMware and Linux system administrator.
        Analyze the following log data and summarize the key issues, warnings, and possible root causes.
        Include a short list of recommendations at the end.
        LOG:
        {log_data[:5000]}
        """

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
            )
            summary = resp.choices[0].message.content
        except Exception as e:
            summary = f"Error analyzing log: {e}"

    return render_template_string(HTML_TEMPLATE, summary=summary)

@app.route("/download", methods=["POST"])
def download_summary():
    summary_text = request.form["summary"]
    buffer = BytesIO(summary_text.encode("utf-8"))
    return send_file(buffer, as_attachment=True, download_name="log_summary.txt", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
