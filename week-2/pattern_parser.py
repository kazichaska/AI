# week-2/pattern_parser.py

import re

def parse_logs(log_text):
    patterns = {
        "timestamp": r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b",  # ISO style
        "error": r"\b(ERROR|WARN|WARNING|CRITICAL|FATAL)\b",
        "ip": r"\b\d{1,3}(?:\.\d{1,3}){3}\b",
        "module": r"\b(?:vpxd|sshd|nginx|systemd|kernel|apache)\b",
        "username": r"user\s+(\w+)",
        "disk": r"(sda\d+|nvme\d+)",
        "vm_name": r"vmx-([\w-]+)",
    }

    results = []
    for line in log_text.splitlines():
        entry = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                entry[key] = match.group()
        if entry:
            entry["raw"] = line.strip()
            results.append(entry)
    return results