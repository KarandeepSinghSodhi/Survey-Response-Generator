import re
import os
from typing import Dict, List

SEVERE_COMPLAINT_KEYWORDS = [
    "never", "broken", "terrible", "awful", "horrible", "useless", "refund", "return", "damage", "late", "delay"
]
POSITIVE_KEYWORDS = [
    "smooth", "excellent", "perfect", "great", "wonderful", "wonderfully", "easy", "on time", "fast", "love"
]


def _contains_keywords(text: str, keywords: List[str]) -> bool:
    text_lower = text.lower()
    return any(re.search(r"\b" + re.escape(word) + r"\b", text_lower) for word in keywords)


def validate_response(response: Dict[str, str]) -> Dict[str, object]:
    satisfaction = int(response["satisfaction"])
    nps = int(response["nps"])
    delivery = response["delivery"]
    feedback = response["feedback"].strip()

    invalid = False
    low_confidence = False
    reasons = []

    if satisfaction <= 2 and nps >= 9:
        invalid = True
        reasons.append("Low satisfaction with a very high NPS score.")

    if satisfaction == 5 and nps <= 2:
        invalid = True
        reasons.append("High satisfaction with an extremely low NPS score.")

    if delivery == "No" and satisfaction == 5:
        low_confidence = True
        reasons.append("Late delivery with perfect satisfaction is unlikely.")

    if satisfaction >= 4 and _contains_keywords(feedback, SEVERE_COMPLAINT_KEYWORDS):
        invalid = True
        reasons.append("Positive satisfaction but feedback contains severe complaint language.")

    if satisfaction <= 2 and _contains_keywords(feedback, POSITIVE_KEYWORDS):
        invalid = True
        reasons.append("Negative satisfaction but feedback sounds too positive.")

    if len(feedback) < 12:
        low_confidence = True
        reasons.append("Feedback is too short to be realistic.")

    return {
        "valid": not invalid,
        "low_confidence": low_confidence,
        "reasons": reasons,
    }


def _make_critic_prompt(response: Dict[str, str]) -> str:
    return (
        "You are a survey quality evaluator. Evaluate whether the feedback is consistent with the structured survey answers.\n"
        f"Satisfaction: {response['satisfaction']}\n"
        f"NPS: {response['nps']}\n"
        f"Delivery: {response['delivery']}\n"
        f"Category: {response['category']}\n"
        f"Feedback: {response['feedback']}\n\n"
        "Rate:\n"
        "1. Consistency (1-10)\n"
        "2. Realism (1-10)\n\n"
        "Provide a JSON object only with the fields:\n"
        "{\n"
        "  \"consistency_score\": x,\n"
        "  \"realism_score\": y,\n"
        "  \"decision\": \"accept\" or \"reject\"\n"
        "}\n"
        "Reject the response if it is clearly inconsistent or unrealistic."
    )


def _heuristic_critic(response: Dict[str, str]) -> Dict[str, object]:
    satisfaction = int(response["satisfaction"])
    nps = int(response["nps"])
    delivery = response["delivery"]
    feedback = response["feedback"].lower()

    consistency = 5
    realism = 5

    if abs(nps - (satisfaction * 2)) <= 2:
        consistency += 3
    if satisfaction >= 4 and nps >= 7:
        consistency += 2
    if satisfaction <= 2 and nps <= 4:
        consistency += 2

    if delivery == "No" and any(word in feedback for word in ["late", "delay", "slow", "longer"]):
        consistency += 2
    if delivery == "Yes" and any(word in feedback for word in ["on time", "arrived when", "quickly", "prompt"]):
        consistency += 2
    if satisfaction <= 2 and any(word in feedback for word in ["disappoint", "poor", "bad", "not good"]):
        realism += 2
    if satisfaction >= 4 and any(word in feedback for word in ["excellent", "smooth", "great", "perfect"]):
        realism += 2

    length = len(feedback.split())
    if 8 <= length <= 30:
        realism += 2
    elif length > 40:
        realism -= 1

    consistency = max(1, min(10, consistency))
    realism = max(1, min(10, realism))
    decision = "accept" if consistency >= 8 and realism >= 7 else "reject"

    return {
        "consistency_score": consistency,
        "realism_score": realism,
        "decision": decision,
    }


def critic_evaluate(response: Dict[str, str]) -> Dict[str, object]:
    if os.getenv("OPENAI_API_KEY"):
        try:
            import openai
            import json
            openai.api_key = os.environ["OPENAI_API_KEY"]
            prompt = _make_critic_prompt(response)
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=120,
            )
            raw = completion.choices[0].message.content.strip()
            parsed = json.loads(raw)
            if (
                isinstance(parsed, dict)
                and "consistency_score" in parsed
                and "realism_score" in parsed
                and "decision" in parsed
            ):
                return parsed
        except Exception:
            pass
    return _heuristic_critic(response)
