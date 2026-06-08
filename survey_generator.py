import os
from typing import Dict
import pandas as pd
from survey_model import generate_population, simulate_latent_state, map_latent_to_response
from survey_open_text import generate_feedback
from survey_validator import validate_response, critic_evaluate
from survey_analysis import (
    correlation_matrix,
    conditional_probabilities,
    distribution_metrics,
    text_diversity_metrics,
    persona_recovery,
)
from report_builder import (
    make_correlation_heatmap,
    make_satisfaction_distribution,
    make_nps_distribution,
    make_category_distribution,
    make_delivery_pie,
    make_persona_distribution,
    make_funnel_chart,
    make_confusion_matrix,
    build_html_report,
)

OUTPUT_CSV = "responses.csv"
OUTPUT_REPORT = "quality_report.html"
TARGET_COUNT = 200


def create_synthetic_dataset(target_count: int = TARGET_COUNT, delivery_rate: float = 0.8, sentiment_bias: float = 0.0) -> Dict[str, object]:
    profiles = generate_population(target_count)
    records = []
    persona_counts: Dict[str, int] = {}
    total_attempts = 0
    rejected = 0

    for profile in profiles:
        persona_counts[profile.persona] = persona_counts.get(profile.persona, 0) + 1
        latent = simulate_latent_state(profile, delivery_rate=delivery_rate, sentiment_bias=sentiment_bias)
        response = map_latent_to_response(latent)
        response["persona"] = profile.persona
        accepted = False

        for attempt in range(6):
            total_attempts += 1
            response["feedback"] = generate_feedback(response)
            validation = validate_response(response)
            if not validation["valid"]:
                rejected += 1
                continue

            critic = critic_evaluate(response)
            if critic["decision"] == "reject":
                rejected += 1
                continue

            records.append({
                "satisfaction": int(response["satisfaction"]),
                "nps": int(response["nps"]),
                "category": response["category"],
                "delivery": response["delivery"],
                "feedback": response["feedback"],
                "persona": response["persona"],
            })
            accepted = True
            break

        if not accepted:
            records.append({
                "satisfaction": int(response["satisfaction"]),
                "nps": int(response["nps"]),
                "category": response["category"],
                "delivery": response["delivery"],
                "feedback": response["feedback"],
                "persona": response["persona"],
            })

    df = pd.DataFrame(records)
    summary = {
        "responses": len(df),
        "attempts": total_attempts,
        "rejected": rejected,
        "accepted": len(df),
        "acceptance_rate": len(df) / max(1, total_attempts),
        "rejection_rate": rejected / max(1, total_attempts),
    }
    return {"df": df, "summary": summary, "persona_counts": persona_counts}


def build_report(results: Dict[str, object]) -> None:
    df = results["df"]
    summary = results["summary"]
    persona_counts = results.get("persona_counts", {})

    corr_matrix = correlation_matrix(df)
    distributions = distribution_metrics(df)
    conditional_probs = conditional_probabilities(df)
    text_metrics = text_diversity_metrics(df)
    persona_results = persona_recovery(df)

    positive_sample = df[df["satisfaction"] >= 4].sort_values("satisfaction", ascending=False).head(1)
    neutral_sample = df[df["satisfaction"] == 3].head(1)
    negative_sample = df[df["satisfaction"] <= 2].sort_values("satisfaction", ascending=True).head(1)

    feedback_samples = []
    if not positive_sample.empty:
        row = positive_sample.iloc[0]
        feedback_samples.append({
            "label": "Positive example",
            "feedback": row["feedback"],
            "satisfaction": int(row["satisfaction"]),
            "nps": int(row["nps"]),
            "category": row["category"],
            "delivery": row["delivery"],
        })
    if not neutral_sample.empty:
        row = neutral_sample.iloc[0]
        feedback_samples.append({
            "label": "Neutral example",
            "feedback": row["feedback"],
            "satisfaction": int(row["satisfaction"]),
            "nps": int(row["nps"]),
            "category": row["category"],
            "delivery": row["delivery"],
        })
    elif len(df) > 0:
        row = df.sample(1).iloc[0]
        feedback_samples.append({
            "label": "Representative example",
            "feedback": row["feedback"],
            "satisfaction": int(row["satisfaction"]),
            "nps": int(row["nps"]),
            "category": row["category"],
            "delivery": row["delivery"],
        })
    if not negative_sample.empty:
        row = negative_sample.iloc[0]
        feedback_samples.append({
            "label": "Negative example",
            "feedback": row["feedback"],
            "satisfaction": int(row["satisfaction"]),
            "nps": int(row["nps"]),
            "category": row["category"],
            "delivery": row["delivery"],
        })

    correlation_score = float(corr_matrix.loc["satisfaction", "nps"])
    insights = [
        f"Satisfaction and NPS correlate at {correlation_score:.2f}, indicating the response model preserves consistent customer sentiment.",
        f"{conditional_probs['p_nps_high_given_satisfaction_high'] * 100:.1f}% of high-satisfaction responses also score NPS ≥ 8.",
        f"Delivery influences satisfaction: {conditional_probs['p_satisfaction_high_given_delivery_no'] * 100:.1f}% of non-delivery responses still score satisfaction ≥ 4.",
    ]

    charts = {
        "correlation_heatmap": make_correlation_heatmap(corr_matrix),
        "persona_distribution": make_persona_distribution(persona_counts),
        "satisfaction_distribution": make_satisfaction_distribution(df),
        "nps_distribution": make_nps_distribution(df),
        "category_distribution": make_category_distribution(df),
        "delivery_pie": make_delivery_pie(df),
        "funnel_chart": make_funnel_chart(summary["accepted"], summary["rejected"]),
        "confusion_matrix": make_confusion_matrix(persona_results["confusion_matrix"], persona_results["labels"]),
    }

    context = {
        "total_responses": summary["responses"],
        "acceptance_rate": summary["acceptance_rate"],
        "rejection_rate": summary["rejection_rate"],
        "text_metrics": text_metrics,
        "conditional_probabilities": conditional_probs,
        "distributions": distributions,
        "persona_results": persona_results,
        "charts": charts,
        "insights": insights,
        "feedback_samples": feedback_samples,
    }

    build_html_report(context, OUTPUT_REPORT)


def main() -> None:
    print("Generating synthetic survey responses...")
    results = create_synthetic_dataset(TARGET_COUNT)
    results["df"].to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {results['summary']['responses']} responses to {OUTPUT_CSV}.")
    build_report(results)
    print(f"Saved quality report to {OUTPUT_REPORT}.")
    print(f"Acceptance rate: {results['summary']['acceptance_rate']:.1%}")
    print(f"Rejection rate: {results['summary']['rejection_rate']:.1%}")


if __name__ == "__main__":
    main()
