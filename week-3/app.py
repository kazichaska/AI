import sys, os, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template_string, request
from openai import OpenAI
from pattern_parser import parse_logs

client = OpenAI()
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Log Insight Analyzer (Week 3)</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        pre, table {
            background: #f7f7f7;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 100%;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }
        th { background-color: #e3f2fd; }
        hr { margin: 30px 0; }
        canvas { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>AI Log Insight Analyzer (Week 3)</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="log_files" multiple>
        <button type="submit">Analyze Logs</button>
    </form>

    {% if summary %}
        <hr>
        <h2>Summary Insights</h2>
        <p><strong>Total Lines:</strong> {{ summary.total_lines }}</p>
        <p><strong>Parsed Entries:</strong> {{ summary.parsed_entries }}</p>

        {% if summary.error_distribution %}
        <h3>Error Distribution</h3>
        <table>
            <tr><th>Error Level</th><th>Count</th></tr>
            {% for k,v in summary.error_distribution.items() %}
                <tr><td>{{ k }}</td><td>{{ v }}</td></tr>
            {% endfor %}
        </table>
        <canvas id="errorChart" width="400" height="200"></canvas>
        {% endif %}

        {% if summary.module_distribution %}
        <h3>Module Distribution</h3>
        <table>
            <tr><th>Module</th><th>Count</th></tr>
            {% for k,v in summary.module_distribution.items() %}
                <tr><td>{{ k }}</td><td>{{ v }}</td></tr>
            {% endfor %}
        </table>
        <canvas id="moduleChart" width="400" height="200"></canvas>
        {% endif %}
    {% endif %}

    {% if ai_report %}
        <hr>
        <h2>AI-Generated Report</h2>
        <pre>{{ ai_report }}</pre>
    {% endif %}

    <script>
        {% if summary.error_distribution %}
        const errorData = {
            labels: {{ summary.error_distribution.keys()|list|tojson }},
            datasets: [{
                label: 'Error Counts',
                data: {{ summary.error_distribution.values()|list|tojson }},
                backgroundColor: '#3498db'
            }]
        };
        new Chart(document.getElementById('errorChart'), {
            type: 'bar',
            data: errorData,
            options: { responsive: true, scales: { y: { beginAtZero: true } } }
        });
        {% endif %}

        {% if summary.module_distribution %}
        const moduleData = {
            labels: {{ summary.module_distribution.keys()|list|tojson }},
            datasets: [{
                label: 'Module Counts',
                data: {{ summary.module_distribution.values()|list|tojson }},
                backgroundColor: '#2ecc71'
            }]
        };
        new Chart(document.getElementById('moduleChart'), {
            type: 'bar',
            data: moduleData,
            options: { responsive: true, scales: { y: { beginAtZero: true } } }
        });
        {% endif %}
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload_files():
    summary = None
    ai_report = None

    if request.method == "POST":
        uploaded_files = request.files.getlist("log_files")
        combined_logs = ""

        for file in uploaded_files:
            if file and file.filename:
                try:
                    text = file.read().decode("utf-8", errors="ignore")
                    combined_logs += f"\n\n--- FILE: {file.filename} ---\n{text}"
                except Exception as e:
                    combined_logs += f"\n\n[Error reading {file.filename}: {e}]"

        parsed_results, summary = parse_logs(combined_logs)

        # Only show top 20 parsed entries in AI prompt to stay concise
        sample_data = json.dumps(parsed_results[:20], indent=2)

        prompt = f"""
You are an expert system log analyst.
Below are structured log entries (sample of 20) from parsed VMware, Linux, or app logs:
{sample_data}

Please analyze patterns and summarize with sections:
- Pattern Overview
- Common Error Sources
- Recommendations
Use clear markdown formatting.
"""

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            ai_report = resp.choices[0].message.content
        except Exception as e:
            ai_report = f"⚠️ Error generating AI summary: {e}"

    return render_template_string(HTML_TEMPLATE, summary=summary, ai_report=ai_report)


if __name__ == "__main__":
    app.run(debug=True)
