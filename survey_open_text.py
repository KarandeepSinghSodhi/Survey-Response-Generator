import os
import random
from typing import Dict

TRANSFORMER_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
OPENAI_MODEL = "gpt-3.5-turbo"


def _make_prompt(context: Dict[str, str]) -> str:
    persona = context.get("persona", "General online shopper")
    return (
        "You are generating customer feedback for an e-commerce satisfaction survey.\n"
        f"Customer persona: {persona}.\n"
        f"Category purchased: {context['category']}.\n"
        f"Delivery outcome: {context['delivery']}.\n"
        f"Satisfaction: {context['satisfaction']}\n"
        f"NPS: {context['nps']}\n\n"
        "Write one realistic, specific customer comment in the voice of this persona.\n"
        "Requirements:\n"
        "- Must be consistent with the survey answers.\n"
        "- Must sound like a real customer with a distinct personality.\n"
        "- Keep it between 1-2 sentences.\n"
        "- Avoid generic phrases and marketing language.\n"
        "- Do not mention numeric scores or NPS directly.\n"
        "- Refer to delivery, product quality, price, or value when appropriate.\n"
        "Return only the comment."
    )


def _fallback_feedback(context: Dict[str, str]) -> str:
    templates = []
    if context["satisfaction"] >= 4:
        if context["delivery"] == "Yes":
            templates = [
                "The order arrived on time and the product quality matched my expectations.",
                "Delivery was smooth and the item was exactly what I wanted.",
                "Everything worked out well and the package came when promised.",
            ]
        else:
            templates = [
                "The item was good, but the delivery arrived later than expected.",
                "Product quality held up, though shipping took too long.",
                "I liked the item, but the late delivery was disappointing.",
            ]
    elif context["satisfaction"] == 3:
        if context["delivery"] == "Yes":
            templates = [
                "The purchase was average; delivery was okay, but the item did not wow me.",
                "It arrived as scheduled, yet the experience felt fairly ordinary.",
                "Delivery was fine, but the product only met my expectations halfway.",
            ]
        else:
            templates = [
                "The product was acceptable, though delivery delays hurt the overall experience.",
                "The order arrived late, and that made the experience more frustrating.",
                "I got what I ordered, but the shipping took longer than it should have.",
            ]
    else:
        if context["delivery"] == "No":
            templates = [
                "The product was disappointing and the late delivery made it worse.",
                "Shipping was late, and the whole experience felt poorly managed.",
                "I had high hopes, but the late delivery left a bad impression.",
            ]
        else:
            templates = [
                "The item arrived on time, but the product quality did not meet my expectations.",
                "Delivery was okay, yet the experience still felt underwhelming.",
                "It showed up when expected, but the purchase was not very satisfying.",
            ]

    return random.choice(templates)


def _generate_with_transformer(context: Dict[str, str]) -> str:
    try:
        from transformers import pipeline
        import torch

        device = 0 if torch.cuda.is_available() else -1
        pipe = pipeline(
            "text-generation",
            model=TRANSFORMER_MODEL,
            trust_remote_code=True,
            device=device,
        )
        prompt = _make_prompt(context)
        result = pipe(
            prompt,
            max_new_tokens=110,
            temperature=0.8,
            top_p=0.92,
            do_sample=True,
        )
        if isinstance(result, list) and result:
            text = result[0].get("generated_text", "")
            if text.startswith(prompt):
                text = text[len(prompt) :]
            return text.strip().replace("\n", " ")
    except Exception:
        pass
    return ""


def generate_feedback(context: Dict[str, str]) -> str:
    text = _generate_with_transformer(context)
    if text:
        return text

    if os.getenv("OPENAI_API_KEY"):
        try:
            import openai

            openai.api_key = os.environ["OPENAI_API_KEY"]
            prompt = _make_prompt(context)
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=80,
            )
            text = response.choices[0].message.content.strip()
            if text:
                return text.replace("\n", " ").strip()
        except Exception:
            pass
    return _fallback_feedback(context)
