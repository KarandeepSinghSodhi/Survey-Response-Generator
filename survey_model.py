from __future__ import annotations
import random
from dataclasses import dataclass
from typing import List
import numpy as np

CATEGORIES = ["Electronics", "Clothing", "Home", "Other"]
AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
INCOME_LEVELS = ["low", "medium", "high"]
SHOPPING_FREQUENCIES = ["low", "medium", "high"]
PERSONA_SEGMENTS = [
    "Value Seeker",
    "Trend Seeker",
    "Home Comfort Shopper",
    "Delivery-Sensitive Shopper",
]


@dataclass
class CustomerProfile:
    customer_id: int
    age_group: str
    income_level: str
    shopping_frequency: str
    delivery_sensitivity: float
    price_sensitivity: float
    brand_loyalty: float
    tech_savviness: float
    persona: str


@dataclass
class LatentState:
    category: str
    delivery_on_time: bool
    delivery_experience: float
    product_experience: float
    price_perception: float
    overall_true_satisfaction: float


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return float(max(minimum, min(maximum, value)))


def weighted_choice(options: List[str], weights: List[float]) -> str:
    return random.choices(options, weights=weights, k=1)[0]


def choose_persona(age_group: str, income_level: str, shopping_frequency: str, tech_savviness: float) -> str:
    # Persona distribution is grounded in common e-commerce shopper archetypes,
    # with a momentum toward younger, high-income trend buyers and older, value-oriented shoppers.
    base_weights = [0.30, 0.25, 0.25, 0.20]
    if income_level == "high":
        base_weights = [0.20, 0.35, 0.22, 0.23]
    elif income_level == "low":
        base_weights = [0.40, 0.15, 0.30, 0.15]

    if tech_savviness > 0.70:
        base_weights[1] += 0.10
        base_weights[0] -= 0.05
    if shopping_frequency == "high":
        base_weights[3] += 0.08
        base_weights[2] -= 0.03

    base_weights = [max(0.01, w) for w in base_weights]
    total = sum(base_weights)
    normalized = [w / total for w in base_weights]
    return weighted_choice(PERSONA_SEGMENTS, normalized)


def generate_customer_profile(customer_id: int) -> CustomerProfile:
    age_group = weighted_choice(AGE_GROUPS, [0.15, 0.30, 0.25, 0.18, 0.12])
    income_level = weighted_choice(INCOME_LEVELS, [0.30, 0.45, 0.25])
    shopping_frequency = weighted_choice(SHOPPING_FREQUENCIES, [0.22, 0.48, 0.30])

    tech_base = {
        "18-24": 0.75,
        "25-34": 0.70,
        "35-44": 0.60,
        "45-54": 0.50,
        "55+": 0.40,
    }
    tech_savviness = clamp(np.random.normal(tech_base[age_group], 0.15))

    price_base = {
        "low": 0.75,
        "medium": 0.50,
        "high": 0.30,
    }
    price_sensitivity = clamp(np.random.normal(price_base[income_level], 0.15))

    loyalty_base = {
        "low": 0.40,
        "medium": 0.60,
        "high": 0.75,
    }
    brand_loyalty = clamp(np.random.normal(loyalty_base[shopping_frequency], 0.16))

    delivery_sensitivity = clamp(np.random.normal(0.55 + 0.15 * (shopping_frequency == "high"), 0.18))
    persona = choose_persona(age_group, income_level, shopping_frequency, tech_savviness)

    return CustomerProfile(
        customer_id=customer_id,
        age_group=age_group,
        income_level=income_level,
        shopping_frequency=shopping_frequency,
        delivery_sensitivity=delivery_sensitivity,
        price_sensitivity=price_sensitivity,
        brand_loyalty=brand_loyalty,
        tech_savviness=tech_savviness,
        persona=persona,
    )


def sample_category(profile: CustomerProfile) -> str:
    weights = [0.15, 0.20, 0.25, 0.40]
    if profile.tech_savviness > 0.7:
        weights[0] += 0.15
        weights[3] -= 0.05
    if profile.income_level == "high":
        weights[0] += 0.10
        weights[1] -= 0.05
    if profile.shopping_frequency == "high":
        weights[2] += 0.05

    if profile.persona == "Trend Seeker":
        weights = [w + delta for w, delta in zip(weights, [0.18, -0.02, -0.05, -0.11])]
    elif profile.persona == "Value Seeker":
        weights = [w - 0.06 if i == 0 else w + 0.10 if i == 1 else w for i, w in enumerate(weights)]
    elif profile.persona == "Home Comfort Shopper":
        weights = [w - 0.08 if i == 0 else w + 0.12 if i == 2 else w for i, w in enumerate(weights)]
    elif profile.persona == "Delivery-Sensitive Shopper":
        weights = [w + delta for w, delta in zip(weights, [0.06, 0.00, 0.08, -0.14])]

    weights = [max(0.01, w) for w in weights]
    total = sum(weights)
    normalized = [w / total for w in weights]
    return weighted_choice(CATEGORIES, normalized)


def simulate_latent_state(profile: CustomerProfile, delivery_rate: float = 0.8, sentiment_bias: float = 0.0) -> LatentState:
    category = sample_category(profile)

    category_bias = {
        "Electronics": 0.08,
        "Clothing": 0.00,
        "Home": 0.05,
        "Other": -0.03,
    }
    persona_product_bias = {
        "Value Seeker": -0.03,
        "Trend Seeker": 0.10,
        "Home Comfort Shopper": 0.05,
        "Delivery-Sensitive Shopper": 0.02,
    }
    persona_price_bias = {
        "Value Seeker": -0.06,
        "Trend Seeker": 0.04,
        "Home Comfort Shopper": 0.01,
        "Delivery-Sensitive Shopper": -0.02,
    }

    product_experience = clamp(
        0.42
        + 0.28 * profile.brand_loyalty
        + 0.22 * profile.tech_savviness
        + category_bias[category]
        + persona_product_bias[profile.persona]
        + np.random.normal(0, 0.07)
    )

    delivery_prob = clamp(delivery_rate - 0.15 * profile.delivery_sensitivity + 0.05 * (profile.shopping_frequency == "low"))
    delivery_on_time = random.random() < delivery_prob
    delivery_experience = clamp(
        0.82
        if delivery_on_time
        else 0.38 - 0.18 * profile.delivery_sensitivity - 0.05 * (profile.persona == "Delivery-Sensitive Shopper")
        + np.random.normal(0, 0.06)
    )

    price_perception = clamp(
        0.40
        + 0.28 * (1 - profile.price_sensitivity)
        + 0.18 * profile.brand_loyalty
        + persona_price_bias[profile.persona]
        + np.random.normal(0, 0.07)
    )

    overall_true_satisfaction = clamp(
        0.5 * product_experience
        + 0.3 * delivery_experience
        + 0.2 * price_perception
        + sentiment_bias
        + np.random.normal(0, 0.04)
    )

    return LatentState(
        category=category,
        delivery_on_time=delivery_on_time,
        delivery_experience=delivery_experience,
        product_experience=product_experience,
        price_perception=price_perception,
        overall_true_satisfaction=overall_true_satisfaction,
    )


def map_latent_to_response(latent: LatentState) -> dict:
    score = latent.overall_true_satisfaction
    if score > 0.80:
        satisfaction = 5
        nps = random.randint(8, 10)
    elif score > 0.60:
        satisfaction = 4
        nps = random.randint(7, 9)
    elif score > 0.40:
        satisfaction = 3
        nps = random.randint(5, 7)
    elif score > 0.20:
        satisfaction = 2
        nps = random.randint(2, 5)
    else:
        satisfaction = 1
        nps = random.randint(0, 3)

    if latent.delivery_experience < 0.45 and satisfaction == 5:
        satisfaction = 4

    nps = int(
        max(
            0,
            min(
                10,
                nps
                + (1 if latent.delivery_experience > 0.75 else -1 if latent.delivery_experience < 0.45 else 0),
            ),
        )
    )

    if satisfaction == 5 and nps < 8:
        nps = random.randint(8, 10)
    if satisfaction == 1 and nps > 3:
        nps = random.randint(0, 3)

    delivery = "Yes" if latent.delivery_on_time else "No"
    return {
        "satisfaction": satisfaction,
        "nps": nps,
        "category": latent.category,
        "delivery": delivery,
    }


def generate_population(count: int = 200) -> List[CustomerProfile]:
    return [generate_customer_profile(i + 1) for i in range(count)]
