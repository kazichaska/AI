import re
from collections import Counter

def parse_logs(log_text):
    patterns = {
        "timestamp": r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\b",
        "error": r"\b(ERROR|WARN|WARNING|CRITICAL|FATAL)\b",
        "ip": r"\b\d{1,3}(?:\.\d{1,3}){3}\b",
        "module": r"\b(?:vpxd|sshd|nginx|systemd|kernel|apache|vmkernel)\b"
    }

    results, error_levels, modules = [], [], []

    for line in log_text.splitlines():
        entry = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                entry[key] = match.group()
        if entry:
            entry["raw"] = line.strip()
            results.append(entry)
            if "error" in entry: error_levels.append(entry["error"])
            if "module" in entry: modules.append(entry["module"])

    summary = {
        "total_lines": len(log_text.splitlines()),
        "parsed_entries": len(results),
        "error_distribution": dict(Counter(error_levels)),
        "module_distribution": dict(Counter(modules))
    }

    return results, summary
