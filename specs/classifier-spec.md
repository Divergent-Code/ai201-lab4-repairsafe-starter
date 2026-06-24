---
{
  "id": "file_vg8yj5sh",
  "filetype": "document",
  "filename": "classifier-spec",
  "created_at": "2026-06-24T01:23:08.518Z",
  "updated_at": "2026-06-24T01:23:09.835Z",
  "meta": {
    "location": "/",
    "tags": [],
    "categories": [],
    "description": "",
    "source": "markdown"
  }
}
---
# Spec: `classify_safety_tier()`

**File:** `safety.py`**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**

```
Routine maintenance and low-risk repairs where mistakes cause only cosmetic damage,
without requiring professional licenses or permits.
```

**caution:**

```
Repairs doable for a homeowner, but where mistakes carry real cost or mild risk,
often involving swapping existing water/electrical components at the same location.
```

**refuse:**

```
High-risk repairs where a mistake can cause fire, flooding, structural failure,
injury, or death, or where a permit/licensed professional is required
(e.g., adding new electrical circuits, gas line work).
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
Use tier definitions + step-by-step reasoning (chain-of-thought). The LLM reasons
through the repair before assigning a tier, which handles ambiguous edge cases like
"replace an outlet" (caution — swapping existing) vs. "add an outlet" (refuse —
new circuit). Few-shot examples are omitted to keep the prompt concise; the
definitions + reasoning chain are sufficient for this domain.
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (*`Label: X / Reasoning: Y`*) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
JSON object enforced via response_format={"type": "json_object"}:
  {"reasoning": "<step-by-step explanation>", "tier": "<safe|caution|refuse>"}

The Groq JSON mode guarantees parseable output. After parsing, "reasoning" is
returned as "reason" in the Python dict to match the key app.py expects.
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**

```
You are a home repair safety classifier. Classify each repair question into exactly
one of three tiers using these definitions:

- safe: Routine maintenance and low-risk repairs where mistakes cause only cosmetic
  damage, without requiring professional licenses or permits.
- caution: Repairs doable for a homeowner, but where mistakes carry real cost or
  mild risk, often involving swapping existing water/electrical components at the
  same location.
- refuse: High-risk repairs where a mistake can cause fire, flooding, structural
  failure, injury, or death, or where a permit/licensed professional is required.

Key boundary rule: If the repair going wrong can cause fire, flooding, structural
failure, injury, or death — classify as "refuse". If it only causes cosmetic or
recoverable damage — classify as "caution".

Think step by step about what the repair involves, what can go wrong, and how
severe the consequences are. Then output ONLY valid JSON in this exact format:
{"reasoning": "<your step-by-step reasoning>", "tier": "<safe|caution|refuse>"}
```

**User message:**

```
Classify this home repair question: {question}
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
Rule: If the worst-case outcome is fire, flooding, structural failure, injury, or
death — refuse; if it's only cosmetic or financially recoverable — caution.

Example 1: "Can I replace an electrical outlet that stopped working?"
→ caution. Swapping an existing outlet at the same location is recoverable; a
mistake (wiring it wrong) might trip a breaker or fail to work, not cause a fire.

Example 2: "Can I add a new electrical outlet to my garage?"
→ refuse. Adding a new circuit involves running wire through walls, connecting to
the panel, and potentially overloading circuits — a fire hazard.
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against* `VALID_TIERS` *fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
On any exception (JSON parse error, key error, API failure) or when the returned
tier is not in VALID_TIERS, return:
  {"tier": "caution", "reason": "Classification failed"}

Failing closed to "caution" (not "safe") is correct here: a user still gets a
response but with a warning, rather than a false assurance that a potentially
dangerous task is safe to DIY. "refuse" would be too aggressive for a parse error
since the question itself may be genuinely benign.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
[your answer here]
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
[your answer here]
```