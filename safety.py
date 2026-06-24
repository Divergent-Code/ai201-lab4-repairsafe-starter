import json

from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)

_SYSTEM_PROMPT = """You are a home repair safety classifier. Classify each repair question into exactly one of three tiers using these definitions:

- safe: Routine maintenance and low-risk repairs where mistakes cause only cosmetic damage, without requiring professional licenses or permits.
- caution: Repairs doable for a homeowner, but where mistakes carry real cost or mild risk, often involving swapping existing water/electrical components at the same location.
- refuse: High-risk repairs where a mistake can cause fire, flooding, structural failure, injury, or death, or where a permit/licensed professional is required.

Key boundary rule: If the repair going wrong can cause fire, flooding, structural failure, injury, or death — classify as "refuse". If it only causes cosmetic or recoverable damage — classify as "caution".

Critical distinction for electrical work:
- REPLACING an existing outlet/switch at the same location (no new wiring to the panel) = "caution" — a wiring mistake trips a breaker, it does not cause a fire.
- ADDING a new outlet or circuit (requires running new wire to the panel) = "refuse" — introduces fire and overload risk.

Think step by step about what the repair involves, what can go wrong, and how severe the consequences are. Then output ONLY valid JSON in this exact format:
{"reasoning": "<your step-by-step reasoning>", "tier": "<safe|caution|refuse>"}"""

_FALLBACK = {"tier": "caution", "reason": "Classification failed"}


def classify_safety_tier(question: str) -> dict:
    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Classify this home repair question: {question}"},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        tier = data.get("tier", "")
        if tier not in VALID_TIERS:
            return _FALLBACK
        return {"tier": tier, "reason": data.get("reasoning", "")}
    except Exception:
        return _FALLBACK
