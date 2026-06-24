import json
import os
from datetime import datetime, timezone
from config import LOG_FILE, LLM_MODEL


def log_interaction(question: str, tier: str, response: str) -> None:
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    truncated_question = question[:300]
    response_length = len(response)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tier": tier,
        "question": truncated_question,
        "response_preview": response[:200],
        "model": LLM_MODEL,
        "response_length": response_length,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f'[LOGGED] tier={tier} | "{truncated_question[:50]}" -> {response_length} chars')
