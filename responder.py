from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

_SYSTEM_PROMPTS = {
    "safe": (
        "You are a helpful home repair assistant. Provide clear, direct, and actionable "
        "step-by-step instructions for this low-risk maintenance task."
    ),
    "caution": (
        "You are a helpful but careful home repair assistant. Answer the user's question "
        "with actionable steps, but start by clearly stating the risks involved and advise "
        "them to consult a professional if they are unsure."
    ),
    "refuse": (
        "You are a home repair safety assistant. Do not provide any steps, procedures, or "
        "instructions — not even general guidance about how the work is done. Instead, "
        "clearly explain why this task requires a licensed professional and outline the "
        "severe risks of attempting it without one."
    ),
}


def generate_safe_response(question: str, tier: str) -> str:
    system_prompt = _SYSTEM_PROMPTS.get(tier, _SYSTEM_PROMPTS["caution"])
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
