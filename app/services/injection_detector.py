import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignora\s+(todas\s+)?las\s+instrucciones",
    r"system\s+prompt",
    r"prompt\s+del\s+sistema",
    r"developer\s+message",
    r"mensaje\s+del\s+desarrollador",
    r"reveal\s+your\s+instructions",
    r"muestra\s+tus\s+instrucciones",
    r"forget\s+all\s+rules",
    r"olvida\s+todas\s+las\s+reglas",
    r"act\s+as\s+",
    r"hazte\s+pasar\s+por",
    r"jailbreak",
    r"bypass",
    r"override",
    r"run\s+sql",
    r"execute\s+sql",
    r"mu[eé]strame\s+las\s+tablas",
    r"mu[eé]strame\s+tu\s+prompt",
    # SQL Injection patterns
    r"\bselect\s+.*\s+from\s+",
    r"\binsert\s+into\s+",
    r"\bupdate\s+.*\s+set\s+",
    r"\bdelete\s+from\s+",
    r"\bdrop\s+(table|database)\s+",
    r"\btruncate\s+table\s+",
    r"\balter\s+table\s+",
    r"\bcreate\s+(table|database)\s+",
    r"\bunion\s+(all\s+)?select\s+",
    r";\s*(select|insert|update|delete|drop)",
    r"--\s*$",
    r"/\*.*\*/",
    r"\bor\s+1\s*=\s*1",
    r"\band\s+1\s*=\s*1",
    r"'\s*or\s+'1'\s*=\s*'1",
    r"'\s*or\s+1\s*=\s*1",
    r"\bexec\s*\(",
    r"\bexecute\s*\(",
]


def detect_prompt_injection(text: str) -> dict:
    text = text.lower().strip()
    matches = []

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(pattern)

    return {
        "is_injection": len(matches) > 0,
        "score": len(matches),
        "patterns": matches
    }
